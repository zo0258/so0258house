#!/usr/bin/env python3
import argparse
import json
import re
import sys
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RESULTS_PATH = ROOT / "results" / "attempts.jsonl"
NOTE_PATH = ROOT / "notes" / "wrong-note.md"


def parse_result(text):
    start = "[HEALTH_EXERCISE_RESULT]"
    end = "[/HEALTH_EXERCISE_RESULT]"
    if start not in text or end not in text:
        raise ValueError("결과 블록을 찾지 못했습니다.")

    body = text.split(start, 1)[1].split(end, 1)[0].strip()
    attempt = {"wrong": [], "review": []}
    for raw_line in body.splitlines():
        line = raw_line.strip()
        if not line:
            continue
        if line.startswith("wrong="):
            payload = line.removeprefix("wrong=")
            parts = payload.split("|")
            wrong_item = {"questionId": parts[0]}
            for part in parts[1:]:
                if "=" not in part:
                    continue
                key, value = part.split("=", 1)
                wrong_item[key] = value
            attempt["wrong"].append(wrong_item)
            continue
        if line.startswith("review="):
            payload = line.removeprefix("review=")
            parts = payload.split("|")
            review_item = {"questionId": parts[0]}
            for part in parts[1:]:
                if "=" not in part:
                    continue
                key, value = part.split("=", 1)
                review_item[key] = value
            attempt["review"].append(review_item)
            continue
        if "=" in line:
            key, value = line.split("=", 1)
            attempt[key] = value

    for number_key in ("score", "total", "answered"):
        if number_key in attempt:
            attempt[number_key] = int(attempt[number_key])

    attempt["recordedAt"] = datetime.now().isoformat(timespec="seconds")
    return attempt


def load_attempts():
    if not RESULTS_PATH.exists():
        return []
    attempts = []
    with RESULTS_PATH.open("r", encoding="utf-8") as file:
        for line in file:
            if line.strip():
                attempts.append(json.loads(line))
    return attempts


def append_attempt(attempt):
    RESULTS_PATH.parent.mkdir(parents=True, exist_ok=True)
    with RESULTS_PATH.open("a", encoding="utf-8") as file:
        file.write(json.dumps(attempt, ensure_ascii=False) + "\n")


def render_wrong_note(attempts):
    subject_counter = Counter()
    topic_counter = Counter()
    question_counter = Counter()
    reason_counter = Counter()
    review_counter = Counter()
    total_score = 0
    total_questions = 0

    recent_wrong = []
    recent_review = []
    for attempt in attempts:
        total_score += int(attempt.get("score", 0))
        total_questions += int(attempt.get("total", 0))
        subject = attempt.get("subject", "미분류")
        for wrong in attempt.get("wrong", []):
            subject_counter[subject] += 1
            topic = wrong.get("topic", "미분류")
            topic_counter[topic] += 1
            question_counter[wrong.get("questionId", "unknown")] += 1
            reason = wrong.get("wrongReason")
            if reason and reason != "미선택":
                reason_counter[reason] += 1
            recent_wrong.append((attempt.get("date", ""), subject, topic, wrong))
        for review in attempt.get("review", []):
            topic = review.get("topic", "미분류")
            review_counter[topic] += 1
            recent_review.append((attempt.get("date", ""), subject, topic, review))

    accuracy = (total_score / total_questions * 100) if total_questions else 0
    lines = [
        "# 건강운동관리사 오답노트",
        "",
        f"- 갱신: {datetime.now().isoformat(timespec='seconds')}",
        f"- 누적 풀이: {len(attempts)}회",
        f"- 누적 정답률: {accuracy:.1f}%",
        "",
        "## 반복 오답 TOP 10",
        ""
    ]

    if topic_counter:
        for topic, count in topic_counter.most_common(10):
            lines.append(f"- {topic}: {count}회")
    else:
        lines.append("- 아직 누적 오답이 없습니다.")

    lines += ["", "## 과목별 오답 수", ""]
    if subject_counter:
        for subject, count in subject_counter.most_common():
            lines.append(f"- {subject}: {count}개")
    else:
        lines.append("- 아직 누적 오답이 없습니다.")

    lines += ["", "## 오답 원인", ""]
    if reason_counter:
        for reason, count in reason_counter.most_common():
            lines.append(f"- {reason}: {count}회")
    else:
        lines.append("- 아직 선택된 오답 원인이 없습니다.")

    lines += ["", "## 최근 오답", ""]
    if recent_wrong:
        for date, subject, topic, wrong in recent_wrong[-20:]:
            selected = wrong.get("selected", "none")
            answer = wrong.get("answer", "")
            reason = wrong.get("wrongReason", "미선택")
            bookmarked = wrong.get("bookmarked", "no")
            lines.append(f"- {date} | {subject} | {topic} | 내 답 {selected} / 정답 {answer} | 이유 {reason} | 다시보기 {bookmarked} | {wrong.get('questionId')}")
    else:
        lines.append("- 아직 누적 오답이 없습니다.")

    lines += ["", "## 다시 볼 문제", ""]
    if recent_review:
        for date, subject, topic, review in recent_review[-20:]:
            lines.append(f"- {date} | {subject} | {topic} | {review.get('questionId')}")
    else:
        lines.append("- 아직 표시된 다시 볼 문제가 없습니다.")

    lines += [
        "",
        "## 다음 퀴즈 반영 규칙",
        "",
        "- 반복 오답 TOP 5 topic은 다음 퀴즈 후보에 우선 포함한다.",
        "- 오답 원인이 '문제 잘못 읽음'이면 같은 개념보다 짧은 판별형 문항을 먼저 배정한다.",
        "- 오답 원인이 '계산 실수'이면 같은 공식의 다른 숫자 문제를 배정한다.",
        "- 과목별 오답 수가 많은 과목은 `config/daily-selection-policy.json` 기준으로 추가 배정한다.",
        "- 다시 볼 문제로 표시된 topic은 다음 퀴즈 또는 주간 복습 후보에 포함한다.",
        "- 같은 questionId가 반복되면 같은 문항보다 같은 topic의 유사 문항을 우선 배정한다."
    ]

    NOTE_PATH.parent.mkdir(parents=True, exist_ok=True)
    NOTE_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description="Record a copied quiz result block and update wrong-note.md.")
    parser.add_argument("input", nargs="?", type=Path, help="Text file containing HEALTH_EXERCISE_RESULT block. Reads stdin when omitted.")
    args = parser.parse_args()

    text = args.input.read_text(encoding="utf-8") if args.input else sys.stdin.read()
    attempt = parse_result(text)
    append_attempt(attempt)
    attempts = load_attempts()
    render_wrong_note(attempts)
    print(f"recorded: {RESULTS_PATH}")
    print(f"wrong-note: {NOTE_PATH}")


if __name__ == "__main__":
    main()
