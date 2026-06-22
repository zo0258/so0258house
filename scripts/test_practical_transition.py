#!/usr/bin/env python3
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(path):
    return path.read_text(encoding="utf-8")


def assert_true(condition, message):
    if not condition:
        raise AssertionError(message)


def main():
    data_path = ROOT / "data" / "practical-questions.json"
    index_path = ROOT / "index.html"
    quiz_path = ROOT / "quizzes" / "quiz-today.html"
    wrong_path = ROOT / "wrong-note.html"

    assert_true(data_path.exists(), "data/practical-questions.json missing")
    questions = json.loads(read(data_path))
    assert_true(isinstance(questions, list) and questions, "practical question data is empty")
    for item in questions:
        for key in ("id", "subject", "section", "type", "year", "question", "methodGuide", "memoryTip", "answerGuide", "sourceRefs", "sourceVerified", "needsReview"):
            assert_true(key in item, f"missing key {key} in {item.get('id')}")
        assert_true(item["type"] in ("실기", "구술", "공통"), f"unexpected type {item['type']}")
        assert_true(item["question"].strip(), f"empty question in {item['id']}")
    assert_true(any(item["type"] == "실기" for item in questions), "no practical questions")
    assert_true(any(item["type"] == "구술" for item in questions), "no oral questions")

    index = read(index_path)
    assert_true("건강운동관리사 실기 대비" in index, "index title text not converted")
    assert_true("오늘 실기 2문제" in index, "today CTA text not converted")
    assert_true("미풀이 · 2문항 남음" in index, "2-question pending copy missing")
    assert_true("10문항" not in index, "old 10-question copy remains in index")

    quiz = read(quiz_path)
    match = re.search(r'<script id="quiz-data" type="application/json">(.*?)</script>', quiz, re.S)
    assert_true(match, "quiz data script missing")
    payload = json.loads(match.group(1))
    assert_true(len(payload["questions"]) == 2, "today quiz does not contain exactly 2 questions")
    types = {item["type"] for item in payload["questions"]}
    assert_true("실기" in types and "구술" in types, "today quiz is not practical + oral")
    assert_true("data-choice" not in quiz, "choice buttons remain in quiz page")
    for label in ("완료", "다시 보기", "어려움"):
        assert_true(label in quiz, f"{label} action missing")

    wrong = read(wrong_path)
    assert_true("어려움·다시 볼 문제" in wrong, "wrong-note meaning not converted")
    assert_true("health-exercise-practical-records" in quiz, "record localStorage key missing in quiz")
    assert_true("health-exercise-practical-records" in wrong, "record localStorage key missing in wrong-note")


if __name__ == "__main__":
    main()
