#!/usr/bin/env python3
import argparse
import json
import re
import subprocess
import tempfile
import xml.etree.ElementTree as ET
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BANK_DIR = ROOT / "data" / "question-bank"
IMAGE_DIR = ROOT / "assets" / "question-images"

NS = {"x": "http://www.w3.org/1999/xhtml"}
FIGURE_MARKERS = ("<그림>", "그림>", "<표>", "분포도", "그래프")
CHOICE_ARTIFACT_RE = re.compile(r"\s*(?:[AB]형\s*)?건강운동관리사\s+필기시험.*$")


def read_jsonl(path):
    rows = []
    if not path.exists():
        return rows
    with path.open("r", encoding="utf-8") as file:
        for line in file:
            if line.strip():
                rows.append(json.loads(line))
    return rows


def write_jsonl(path, rows):
    with path.open("w", encoding="utf-8") as file:
        for row in rows:
            file.write(json.dumps(row, ensure_ascii=False) + "\n")


def has_figure_marker(question):
    text = " ".join([question.get("question", ""), *question.get("choices", [])])
    return any(marker in text for marker in FIGURE_MARKERS)


def clean_choices(question):
    cleaned = []
    changed = False
    for choice in question.get("choices", []):
        value = CHOICE_ARTIFACT_RE.sub("", str(choice)).strip()
        cleaned.append(value)
        changed = changed or value != choice
    if changed:
        question["choices"] = cleaned
    return changed


def pdf_layout(pdf_path):
    result = subprocess.run(["pdftotext", "-bbox-layout", str(pdf_path), "-"], check=True, text=True, capture_output=True)
    return ET.fromstring(result.stdout)


def question_anchors(page, page_index):
    page_width = float(page.attrib["width"])
    anchors = []
    for word in page.findall(".//x:word", NS):
        text = "".join(word.itertext()).strip()
        if re.fullmatch(r"\d{1,2}\.", text):
            x = float(word.attrib["xMin"])
            anchors.append({
                "no": int(text[:-1]),
                "x": x,
                "y": float(word.attrib["yMin"]),
                "page": page_index,
                "column": 0 if x < page_width / 2 else 1,
            })
    return anchors


def ordered_question_anchors(layout):
    anchors = []
    for page_index, page in enumerate(layout.findall(".//x:page", NS), start=1):
        if page_index == 1:
            continue
        anchors.extend(question_anchors(page, page_index))
    return sorted(anchors, key=lambda item: (item["page"], item["column"], item["y"], item["x"]))


def find_question_region(layout, subject_code, question_no):
    subject_order = {
        70: 0,
        71: 1,
        72: 2,
        73: 3,
        74: 0,
        75: 1,
        76: 2,
        77: 3,
    }
    order_index = subject_order.get(int(subject_code))
    if order_index is None:
        return None
    anchors = ordered_question_anchors(layout)
    ordinal = order_index * 20 + int(question_no) - 1
    if ordinal < 0 or ordinal >= len(anchors):
        return None
    anchor = anchors[ordinal]
    if anchor["no"] != int(question_no):
        fallback = [
            item for item in anchors[order_index * 20:(order_index + 1) * 20]
            if item["no"] == int(question_no)
        ]
        if not fallback:
            return None
        anchor = fallback[0]

    pages = layout.findall(".//x:page", NS)
    page_index = anchor["page"]
    page = pages[page_index - 1]
    page_width = float(page.attrib["width"])
    page_height = float(page.attrib["height"])
    left_column = anchor["x"] < page_width / 2
    x_min = 18 if left_column else page_width / 2 + 8
    x_max = page_width / 2 - 8 if left_column else page_width - 18
    same_page_column = [
        other for other in anchors
        if other["page"] == page_index
        and other["y"] > anchor["y"] + 8
        and (other["x"] < page_width / 2) == left_column
    ]
    y_min = max(0, anchor["y"] - 18)
    y_max = min(page_height - 28, min((other["y"] for other in same_page_column), default=page_height - 28) - 8)
    if y_max <= y_min + 80:
        y_max = min(page_height - 28, y_min + 260)
    return {"page": page_index, "pageWidth": page_width, "pageHeight": page_height, "xMin": x_min, "yMin": y_min, "xMax": x_max, "yMax": y_max}


def render_page(pdf_path, page, tmp_dir, dpi):
    prefix = tmp_dir / "page"
    subprocess.run(["pdftoppm", "-f", str(page), "-l", str(page), "-singlefile", "-png", "-r", str(dpi), str(pdf_path), str(prefix)], check=True, text=True, capture_output=True)
    return prefix.with_suffix(".png")


def image_size(path):
    result = subprocess.run(["magick", "identify", "-format", "%w %h", str(path)], check=True, text=True, capture_output=True)
    width, height = result.stdout.split()
    return int(width), int(height)


def crop_region(source_image, region, output_path):
    width, height = image_size(source_image)
    scale_x = width / region["pageWidth"]
    scale_y = height / region["pageHeight"]
    x = max(0, round(region["xMin"] * scale_x))
    y = max(0, round(region["yMin"] * scale_y))
    crop_w = min(width - x, round((region["xMax"] - region["xMin"]) * scale_x))
    crop_h = min(height - y, round((region["yMax"] - region["yMin"]) * scale_y))
    output_path.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(["magick", str(source_image), "-crop", f"{crop_w}x{crop_h}+{x}+{y}", "+repage", "-trim", "+repage", "-resize", "1100x>", str(output_path)], check=True, text=True, capture_output=True)


def process_bank(path, dpi):
    rows = read_jsonl(path)
    layout_cache = {}
    changed = 0
    with tempfile.TemporaryDirectory() as tmp:
        tmp_dir = Path(tmp)
        for question in rows:
            if not has_figure_marker(question):
                continue
            if clean_choices(question):
                changed += 1
            source = question.get("source") or {}
            pdf_rel = source.get("file")
            question_no = source.get("questionNo")
            subject_code = source.get("subjectCode")
            if not pdf_rel or not question_no or not subject_code:
                continue
            pdf_path = ROOT / pdf_rel
            if not pdf_path.exists() or pdf_path.suffix.lower() != ".pdf":
                continue
            if pdf_path not in layout_cache:
                layout_cache[pdf_path] = pdf_layout(pdf_path)
            region = find_question_region(layout_cache[pdf_path], int(subject_code), int(question_no))
            if not region:
                continue
            image_path = IMAGE_DIR / f"{question['id']}.png"
            crop_region(render_page(pdf_path, region["page"], tmp_dir, dpi), region, image_path)
            question["images"] = [{"src": str(image_path.relative_to(ROOT)), "alt": f"{question['id']} 원본 그림 문항", "sourcePage": region["page"]}]
            changed += 1
    if changed:
        write_jsonl(path, rows)
    return changed


def main():
    parser = argparse.ArgumentParser(description="Extract source PDF crops for figure-dependent question-bank items.")
    parser.add_argument("--bank", type=Path, help="Single question-bank JSONL file. Defaults to all banks.")
    parser.add_argument("--dpi", type=int, default=180)
    args = parser.parse_args()

    paths = [args.bank] if args.bank else sorted(BANK_DIR.glob("*.jsonl"))
    total = 0
    for path in paths:
        path = path if path.is_absolute() else ROOT / path
        changed = process_bank(path, args.dpi)
        total += changed
        print(f"{path.relative_to(ROOT)} images={changed}")
    print(f"total_images={total}")


if __name__ == "__main__":
    main()
