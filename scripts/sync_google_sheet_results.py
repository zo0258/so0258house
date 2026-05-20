#!/usr/bin/env python3
import argparse
import csv
import json
import subprocess
import sys
import tempfile
import urllib.parse
import urllib.request
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ATTEMPTS_PATH = ROOT / "results" / "attempts.jsonl"
CONFIG_PATH = ROOT / "config" / "sync.json"


def run(command, check=True):
    result = subprocess.run(command, cwd=ROOT, text=True, capture_output=True)
    if result.stdout:
        print(result.stdout, end="")
    if result.stderr:
        print(result.stderr, end="", file=sys.stderr)
    if check and result.returncode != 0:
        raise SystemExit(result.returncode)
    return result


def read_json(path):
    with path.open("r", encoding="utf-8") as file:
        return json.load(file)


def read_jsonl(path):
    if not path.exists():
        return []
    rows = []
    with path.open("r", encoding="utf-8") as file:
        for line in file:
            if line.strip():
                rows.append(json.loads(line))
    return rows


def parse_key(result_text):
    data = {}
    for line in str(result_text or "").splitlines():
        if "=" not in line or line.startswith(("wrong=", "review=", "answerLog=", "unanswered=")):
            continue
        key, value = line.split("=", 1)
        data[key] = value
    return data.get("date", ""), data.get("quizId", "")


def load_existing_keys():
    return {(row.get("date", ""), row.get("quizId", "")) for row in read_jsonl(ATTEMPTS_PATH)}


def fetch_csv_rows(csv_url):
    with urllib.request.urlopen(csv_url, timeout=30) as response:
        text = response.read().decode("utf-8-sig")
    return list(csv.DictReader(text.splitlines()))


def fetch_web_app_rows(submit_url):
    query = urllib.parse.urlencode({"action": "rows"})
    separator = "&" if "?" in submit_url else "?"
    url = f"{submit_url}{separator}{query}"
    with urllib.request.urlopen(url, timeout=30) as response:
        payload = json.loads(response.read().decode("utf-8"))
    if not payload.get("ok"):
        raise SystemExit(f"Apps Script rows 조회 실패: {payload}")
    return payload.get("rows", [])


def fetch_rows(config, csv_url=None, web_app_url=None):
    if csv_url:
        return fetch_csv_rows(csv_url)
    submit_url = web_app_url or config.get("submitUrl")
    if submit_url:
        return fetch_web_app_rows(submit_url)
    raise SystemExit("csvUrl 또는 submitUrl이 없습니다. config/sync.json 설정을 확인해주세요.")


def has_staged_changes():
    return run(["git", "diff", "--cached", "--quiet"], check=False).returncode != 0


def main():
    parser = argparse.ArgumentParser(description="Import submitted quiz results from Google Sheets or Apps Script and republish static pages.")
    parser.add_argument("--csv-url", help="Google Sheets CSV export URL. Defaults to config/sync.json csvUrl.")
    parser.add_argument("--web-app-url", help="Apps Script Web App URL. Defaults to config/sync.json submitUrl.")
    parser.add_argument("--no-push", action="store_true")
    args = parser.parse_args()

    config = read_json(CONFIG_PATH) if CONFIG_PATH.exists() else {}
    csv_url = args.csv_url or config.get("csvUrl")

    existing = load_existing_keys()
    imported_dates = set()
    for row in fetch_rows(config, csv_url=csv_url, web_app_url=args.web_app_url):
        result_text = row.get("resultText", "")
        key = parse_key(result_text)
        if not all(key) or key in existing:
            continue
        with tempfile.NamedTemporaryFile("w", encoding="utf-8", delete=False) as temp:
            temp.write(result_text)
            temp_path = Path(temp.name)
        try:
            run([sys.executable, "scripts/record_attempt.py", str(temp_path)])
        finally:
            temp_path.unlink(missing_ok=True)
        existing.add(key)
        imported_dates.add(key[0])

    for quiz_date in sorted(imported_dates):
        quiz_json = ROOT / "data" / "quizzes" / f"{quiz_date}-daily.json"
        if quiz_json.exists():
            run([sys.executable, "scripts/generate_quiz_html.py", str(quiz_json)])

    if imported_dates:
        run([sys.executable, "scripts/build_static_site.py", "--site-dir", "."])
        paths = ["index.html", "wrong-note.html", "data/review/wrong-note.json"]
        paths.extend(f"quizzes/quiz-{quiz_date}.html" for quiz_date in sorted(imported_dates) if (ROOT / "quizzes" / f"quiz-{quiz_date}.html").exists())
        run(["git", "add", *paths])
        if has_staged_changes():
            run(["git", "commit", "-m", "Sync Google Sheets quiz results"])
        if not args.no_push:
            run(["git", "push"])
    print(f"imported={len(imported_dates)}")


if __name__ == "__main__":
    main()
