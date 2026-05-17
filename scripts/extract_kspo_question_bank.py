#!/usr/bin/env python3
import argparse
import json
import re
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT = ROOT / "data" / "question-bank" / "kspo-2023-a.jsonl"

SESSION_SUBJECTS = {
    1: [
        ("운동생리학", 70),
        ("건강·체력평가", 71),
        ("운동처방론", 72),
        ("운동부하검사", 73),
    ],
    2: [
        ("운동상해", 74),
        ("기능해부학", 75),
        ("병태생리학", 76),
        ("스포츠심리학", 77),
    ],
}

CIRCLED_TO_INDEX = {"①": 0, "②": 1, "③": 2, "④": 3, "⑤": 4}
INDEX_TO_CIRCLED = ["①", "②", "③", "④", "⑤"]


def run_pdftotext(path):
    result = subprocess.run(
        ["pdftotext", "-raw", str(path), "-"],
        check=True,
        text=True,
        capture_output=True,
    )
    return result.stdout


def normalize_subject_text(text):
    return re.sub(r"[\s･·\(\)（）]", "", text)


def compact_spaces(text):
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def parse_answer_rows(answer_pdf):
    text = run_pdftotext(answer_pdf)
    rows = []
    for line in text.splitlines():
        answers = re.findall(r"[①②③④⑤]", line)
        if len(answers) == 20:
            rows.append([CIRCLED_TO_INDEX[value] for value in answers])
    if len(rows) < 16:
        raise ValueError(f"정답 행을 충분히 찾지 못했습니다: {answer_pdf} ({len(rows)}행)")

    return {
        (1, "A"): rows[0:4],
        (1, "B"): rows[4:8],
        (2, "A"): rows[8:12],
        (2, "B"): rows[12:16],
    }


def find_subject_ranges(text, session):
    ranges = []
    line_start = 0
    lines = []
    for line in text.splitlines(keepends=True):
        lines.append((line_start, line))
        line_start += len(line)

    for subject, code in SESSION_SUBJECTS[session]:
        normalized_subject = normalize_subject_text(subject)
        position = None
        for start, line in lines:
            normalized_line = normalize_subject_text(line)
            if "(" in line and ")" in line and normalized_subject in normalized_line and str(code) in normalized_line:
                position = start
                break
        if position is None:
            raise ValueError(f"과목 위치를 찾지 못했습니다: {subject}")
        ranges.append((position, subject, code))

    ranges.sort()
    sections = []
    for idx, (start, subject, code) in enumerate(ranges):
        end = ranges[idx + 1][0] if idx + 1 < len(ranges) else len(text)
        sections.append((subject, code, text[start:end]))
    return sections


def split_question_blocks(section_text):
    matches = list(re.finditer(r"(?m)^(\d{1,2})\.\s+", section_text))
    blocks = []
    for idx, match in enumerate(matches):
        question_no = int(match.group(1))
        start = match.start()
        end = matches[idx + 1].start() if idx + 1 < len(matches) else len(section_text)
        if 1 <= question_no <= 20:
            blocks.append((question_no, section_text[start:end]))
    return blocks


def parse_question_block(block):
    block = compact_spaces(block)
    choice_matches = list(re.finditer(r"[①②③④⑤]", block))
    if len(choice_matches) < 4:
        return None

    first_choice = choice_matches[0].start()
    stem = re.sub(r"^\d{1,2}\.\s*", "", block[:first_choice]).strip()
    choices = []
    selected_choice_matches = choice_matches[:4]
    for idx, match in enumerate(selected_choice_matches):
        start = match.end()
        end = selected_choice_matches[idx + 1].start() if idx + 1 < len(selected_choice_matches) else len(block)
        choice_text = block[start:end].strip()
        choice_text = re.sub(r"\s+", " ", choice_text)
        choices.append(choice_text)

    if not stem or any(not choice for choice in choices):
        return None
    return stem, choices


def infer_type(stem):
    if "계산" in stem or "추정" in stem or "구하" in stem:
        return "계산"
    if "옳은 것으로만" in stem or "모두 고른" in stem:
        return "보기조합"
    if "괄호" in stem:
        return "빈칸"
    if "옳지 않은" in stem:
        return "부정형"
    return "개념구분"


def infer_difficulty(stem, qtype):
    score = 3
    if qtype in {"보기조합", "계산"}:
        score += 1
    if len(stem) > 160:
        score += 1
    return min(score, 5)


def infer_topic(subject, stem):
    text = re.sub(r"<[^>]+>", "", stem)
    text = re.sub(r"\([^)]*\)", "", text)
    text = re.sub(r"에서|으로|에 대한|에 관한|의 |가 |은 |는 |을 |를 ", " ", text)
    text = re.sub(r"[^0-9A-Za-z가-힣·･\s]", " ", text)
    words = [word for word in text.split() if len(word) > 1]
    if not words:
        return subject
    return " ".join(words[:2])[:24]


def build_question(year, session, form, subject, code, question_no, stem, choices, answer_index, question_pdf, answer_pdf):
    qtype = infer_type(stem)
    topic = infer_topic(subject, stem)
    answer_label = INDEX_TO_CIRCLED[answer_index]
    return {
        "id": f"{year}-{session}{form}-{code}-{question_no:02d}",
        "year": year,
        "subject": subject,
        "topic": topic,
        "type": qtype,
        "difficulty": infer_difficulty(stem, qtype),
        "trap": f"{topic} 관련 조건과 보기 표현을 섞어 판단하는 문항",
        "question": stem,
        "choices": choices,
        "answerIndex": answer_index,
        "explanation": f"최종정답 기준 정답은 {answer_label}입니다. 해설 보강 전 기본 문항이므로, 틀린 경우 문제 조건과 각 보기의 핵심 용어를 원문 기준으로 다시 확인하세요.",
        "source": {
            "file": str(question_pdf.relative_to(ROOT)),
            "answerFile": str(answer_pdf.relative_to(ROOT)),
            "questionNo": question_no,
            "session": session,
            "form": form,
            "subjectCode": code,
        },
        "wrongRateBasis": "고오답 추정",
        "verified": True,
        "bankSource": "pdftotext 자동 추출 후 최종정답 매칭",
    }


def extract_session(year, session, form, question_pdf, answer_pdf, answers):
    text = run_pdftotext(question_pdf)
    extracted = []
    answer_rows = answers[(session, form)]

    for subject_index, (subject, code, section) in enumerate(find_subject_ranges(text, session)):
        subject_answers = answer_rows[subject_index]
        for question_no, block in split_question_blocks(section):
            parsed = parse_question_block(block)
            if not parsed:
                continue
            stem, choices = parsed
            answer_index = subject_answers[question_no - 1]
            extracted.append(build_question(year, session, form, subject, code, question_no, stem, choices, answer_index, question_pdf, answer_pdf))
    return extracted


def main():
    parser = argparse.ArgumentParser(description="Extract KSPO health exercise question bank from text-readable PDFs.")
    parser.add_argument("--year", type=int, default=2023)
    parser.add_argument("--form", default="A", choices=["A", "B"])
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()

    base = ROOT / "materials" / "raw" / "kspo" / str(args.year)
    question_pdfs = {
        1: base / "questions" / f"{args.year} 건강운동관리사 필기시험 1교시 {args.form}형kspo.pdf",
        2: base / "questions" / f"{args.year} 건강운동관리사 필기시험 2교시 {args.form}형kspo.pdf",
    }
    answer_pdf = base / "final_answer" / f"{args.year} 건강운동관리사 필기시험 최종정답.pdf"

    for path in [*question_pdfs.values(), answer_pdf]:
        if not path.exists():
            raise SystemExit(f"파일을 찾지 못했습니다: {path}")

    answers = parse_answer_rows(answer_pdf)
    questions = []
    for session, question_pdf in question_pdfs.items():
        questions.extend(extract_session(args.year, session, args.form, question_pdf, answer_pdf, answers))

    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", encoding="utf-8") as file:
        for question in questions:
            file.write(json.dumps(question, ensure_ascii=False) + "\n")

    subject_counts = {}
    for question in questions:
        subject_counts[question["subject"]] = subject_counts.get(question["subject"], 0) + 1

    print(args.output)
    print(f"questions={len(questions)}")
    for subject, _code in SESSION_SUBJECTS[1] + SESSION_SUBJECTS[2]:
        print(f"{subject}={subject_counts.get(subject, 0)}")


if __name__ == "__main__":
    main()
