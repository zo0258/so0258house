#!/usr/bin/env python3
import argparse
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SOURCE = ROOT / "data" / "quizzes" / "2026-05-18-daily.json"
DEFAULT_OUTPUT = ROOT / "data" / "question-bank" / "seed.jsonl"


def read_json(path):
    with path.open("r", encoding="utf-8") as file:
        return json.load(file)


def main():
    parser = argparse.ArgumentParser(description="Build a JSONL question bank from verified quiz JSON files.")
    parser.add_argument("--source", type=Path, default=DEFAULT_SOURCE, help="Verified quiz JSON to import.")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT, help="Question bank JSONL path.")
    parser.add_argument("--replace", action="store_true", help="Replace the output file instead of appending new IDs.")
    args = parser.parse_args()

    source_path = args.source if args.source.is_absolute() else ROOT / args.source
    output_path = args.output if args.output.is_absolute() else ROOT / args.output

    quiz = read_json(source_path)
    existing_ids = set()
    if output_path.exists() and not args.replace:
        with output_path.open("r", encoding="utf-8") as file:
            for line in file:
                if line.strip():
                    existing_ids.add(json.loads(line)["id"])

    imported = 0
    output_path.parent.mkdir(parents=True, exist_ok=True)
    mode = "w" if args.replace else "a"
    with output_path.open(mode, encoding="utf-8") as file:
        for question in quiz.get("questions", []):
            if question["id"] in existing_ids:
                continue
            item = dict(question)
            item.setdefault("verified", True)
            item.setdefault("bankSource", str(source_path.relative_to(ROOT)))
            file.write(json.dumps(item, ensure_ascii=False) + "\n")
            imported += 1

    print(f"imported={imported}")
    print(output_path)


if __name__ == "__main__":
    main()
