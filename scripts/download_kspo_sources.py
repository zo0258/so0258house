#!/usr/bin/env python3
import json
import re
import time
from pathlib import Path
from urllib.parse import parse_qs, urljoin, urlparse
from urllib.request import Request, urlopen


BASE_URL = "https://sqms.kspo.or.kr"
LIST_URL = f"{BASE_URL}/exam/wrQnaList.kspo"
VIEW_URL = f"{BASE_URL}/exam/wrQnaView.kspo"
DOWNLOAD_URL = f"{BASE_URL}/file/downloadFile.kspo?type=board&BRD_FILE_SN={{file_id}}"

ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "materials" / "raw" / "kspo"
MANIFEST_PATH = OUT_DIR / "manifest.json"

TARGETS = [
    {"year": 2025, "kind": "final_answer", "view_id": "7763"},
    {"year": 2025, "kind": "draft_answer", "view_id": "7742"},
    {"year": 2025, "kind": "questions", "view_id": "7741"},
    {"year": 2024, "kind": "final_answer", "view_id": "7550"},
    {"year": 2024, "kind": "draft_answer", "view_id": "7539"},
    {"year": 2024, "kind": "questions", "view_id": "7538"},
    {"year": 2023, "kind": "final_answer", "view_id": "7250"},
    {"year": 2023, "kind": "draft_answer", "view_id": "7217"},
    {"year": 2023, "kind": "questions", "view_id": "7216"},
    {"year": 2022, "kind": "final_answer", "view_id": "7027"},
    {"year": 2022, "kind": "draft_answer", "view_id": "6982"},
    {"year": 2022, "kind": "questions", "view_id": "6981"},
    {"year": 2021, "kind": "final_answer", "view_id": "6619"},
    {"year": 2021, "kind": "questions", "view_id": "6623"},
    {"year": 2021, "kind": "draft_answer", "view_id": "6625"},
    {"year": 2020, "kind": "final_answer", "view_id": "6620"},
    {"year": 2020, "kind": "questions_and_draft_answer", "view_id": "6618"},
    {"year": 2019, "kind": "final_answer", "view_id": "6604"},
    {"year": 2019, "kind": "questions_and_draft_answer", "view_id": "6603"},
    {"year": 2018, "kind": "final_answer", "view_id": "6592"},
    {"year": 2018, "kind": "questions_and_draft_answer", "view_id": "6591"},
    {"year": 2017, "kind": "final_answer", "view_id": "6589"},
    {"year": 2017, "kind": "questions_and_draft_answer", "view_id": "6588"},
    {"year": 2016, "kind": "final_answer_notice", "view_id": "6583"},
    {"year": 2016, "kind": "questions_and_draft_answer", "view_id": "6582"},
    {"year": 2015, "kind": "questions_and_draft_answer", "view_id": "6575"},
]


def fetch(url, data=None):
    body = data.encode("utf-8") if data is not None else None
    req = Request(
        url,
        data=body,
        headers={
            "User-Agent": "Mozilla/5.0",
            "Content-Type": "application/x-www-form-urlencoded",
        },
    )
    with urlopen(req, timeout=30) as response:
        return response.read(), response.headers


def post_view(view_id):
    raw, _ = fetch(VIEW_URL, f"BRD_CON_SN={view_id}")
    return raw.decode("utf-8", errors="replace")


def clean_filename(name):
    name = re.sub(r"[\\/:*?\"<>|]+", "_", name).strip()
    name = re.sub(r"\s+", " ", name)
    return name or "downloaded-file"


def parse_files(html):
    pattern = re.compile(
        r"fnDownloadFile\('(?P<id>\d+)'\)\">(?P<name>[^<]+)</a>",
        re.MULTILINE,
    )
    return [
        {"file_id": match.group("id"), "name": clean_filename(match.group("name"))}
        for match in pattern.finditer(html)
    ]


def content_disposition_filename(headers):
    value = headers.get("Content-Disposition") or headers.get("content-disposition") or ""
    parsed = re.search(r"filename\\*=UTF-8''([^;]+)", value)
    if parsed:
        return clean_filename(urlparse(parsed.group(1)).path)
    parsed = re.search(r'filename="?([^";]+)"?', value)
    if parsed:
        return clean_filename(parsed.group(1))
    return None


def download_file(file_id, fallback_name, target_dir):
    url = DOWNLOAD_URL.format(file_id=file_id)
    raw, headers = fetch(url)
    filename = content_disposition_filename(headers) or fallback_name
    path = target_dir / clean_filename(filename)
    path.write_bytes(raw)
    return {
        "file_id": file_id,
        "source_url": url,
        "path": str(path.relative_to(ROOT)),
        "bytes": len(raw),
    }


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    manifest = {
        "source": "KSPO 체육지도자 자격검정 및 연수 - 필기시험 문제ㆍ정답",
        "list_url": LIST_URL,
        "downloaded_at": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
        "items": [],
    }

    for target in TARGETS:
        html = post_view(target["view_id"])
        files = parse_files(html)
        target_dir = OUT_DIR / str(target["year"]) / target["kind"]
        target_dir.mkdir(parents=True, exist_ok=True)
        downloaded = []
        for file in files:
            downloaded.append(download_file(file["file_id"], file["name"], target_dir))
            time.sleep(0.2)
        manifest["items"].append(
            {
                **target,
                "view_url": VIEW_URL,
                "files": downloaded,
                "file_count": len(downloaded),
            }
        )
        print(f"{target['year']} {target['kind']}: {len(downloaded)} files")

    MANIFEST_PATH.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"manifest: {MANIFEST_PATH.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
