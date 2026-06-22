#!/usr/bin/env python3
import argparse
from collections import Counter, defaultdict
from datetime import date
import html
import json
import re
import shutil
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PDF = ROOT.parent / "건강운동관리사 취득 기초 길잡이v.2026.pdf"
DATA_PATH = ROOT / "data" / "practical-questions.json"
QUIZ_DATA_PATH = ROOT / "data" / "quizzes" / "today-practical.json"
QUIZ_HTML_PATH = ROOT / "quizzes" / "quiz-today.html"
INDEX_PATH = ROOT / "index.html"
WRONG_NOTE_PATH = ROOT / "wrong-note.html"
TMP_DIR = ROOT / "tmp"

START_TITLE = "09. 건강운동관리사 실기 · 구술시험 기출문제 분석"
STOP_TITLE = "10. 건강운동관리사 실기 · 구술시험 준비 꿀팁"
RECORD_KEY = "health-exercise-practical-records"

SUBJECT_RE = re.compile(r"^\s*(\d+)\.\s+(.+?)\s+실기/구술 기출문제")
SECTION_RE = re.compile(r"^\s*\((\d+)\)\s+(.+?)\s*$")
TYPE_RE = re.compile(r"^\s*<\s*(실기|구술|공통)\s*>\s*$")
QUESTION_RE = re.compile(r"^\s*(\d+)\.\s+(.+)")
YEAR_RE = re.compile(r"\((20\d{2}|201\d)\)")
FOOTER_RE = re.compile(r"무단 전재|Yang 건운사|-+\d+p-+|^\s*\f\s*$")

CONTEXT_GUIDES = {
    "실기": {
        "methodGuide": "추후 입력: 실제 수행 순서, 검사 환경, 대상자 안내 멘트, 안전 확인 순서까지 확인 후 작성",
        "memoryTip": "동작은 준비-설명-시범-수행-기록 순서로 떠올리기",
    },
    "구술": {
        "methodGuide": "추후 입력: 정의, 기준, 적용 대상, 주의사항 순서로 답변 구성",
        "memoryTip": "답변은 핵심어 3개를 먼저 말하고 한 문장씩 설명하기",
    },
    "공통": {
        "methodGuide": "추후 입력: 장비 준비, 자세, 시선, 호흡, 강도 설정, 안전 확인을 함께 점검",
        "memoryTip": "공통 문항은 장비-자세-호흡-안전-기록 순서",
    },
}

GENERAL_SOURCE_REFS = [
    {
        "title": "ACSM Guidelines for Exercise Testing and Prescription",
        "url": "https://www.acsm.org/education-resources/books/guidelines-exercise-testing-prescription",
    },
    {
        "title": "ACSM Physical Activity Guidelines",
        "url": "https://acsm.org/education-resources/trending-topics-resources/physical-activity-guidelines/",
    },
]


def run_pdftotext(pdf_path):
    TMP_DIR.mkdir(exist_ok=True)
    text_path = TMP_DIR / "practical-pages22-end.txt"
    subprocess.run(
        ["pdftotext", "-f", "22", "-layout", "-enc", "UTF-8", str(pdf_path), str(text_path)],
        check=True,
    )
    return text_path.read_text(encoding="utf-8")


def clean_line(line):
    line = line.replace("\u2013", "-").replace("\u2014", "-")
    line = re.sub(r"\s+", " ", line.strip())
    return line


def normalize_question(text):
    text = clean_line(text)
    text = re.sub(r"\s+\((20\d{2}|201\d)\)\s*$", r"(\1)", text)
    return text


def body_slice(text):
    start = text.find(START_TITLE)
    if start < 0:
        raise RuntimeError(f"start title not found: {START_TITLE}")
    stop = text.find(STOP_TITLE, start)
    return text[start: stop if stop > start else len(text)]


def is_boundary(line):
    return SUBJECT_RE.match(line) or SECTION_RE.match(line) or TYPE_RE.match(line) or QUESTION_RE.match(line)


def flush_question(rows, state, questions):
    if not rows:
        return
    raw = normalize_question(" ".join(rows))
    year_match = YEAR_RE.search(raw)
    year = int(year_match.group(1)) if year_match else None
    guide = CONTEXT_GUIDES.get(state["type"] or "공통", CONTEXT_GUIDES["공통"])
    needs_review = False
    reasons = []
    if year is None:
        needs_review = True
        reasons.append("연도 추출 실패")
    for key, label in (("subject", "과목"), ("section", "section"), ("type", "type")):
        if not state.get(key):
            needs_review = True
            reasons.append(f"{label} 불명확")
    if "�" in raw or len(raw) < 8:
        needs_review = True
        reasons.append("PDF 텍스트 추출 확인 필요")
    if guide["methodGuide"].startswith("추후 입력"):
        needs_review = True
        reasons.append("methodGuide 추후 입력")
    qid = f"practical-{len(questions) + 1:03d}"
    questions.append({
        "id": qid,
        "subject": state.get("subject", ""),
        "section": state.get("section", ""),
        "type": state.get("type", ""),
        "year": year,
        "question": raw,
        "methodGuide": guide["methodGuide"],
        "memoryTip": guide["memoryTip"],
        "answerGuide": "",
        "sourceRefs": GENERAL_SOURCE_REFS if state.get("type") in ("실기", "구술", "공통") else [],
        "sourceVerified": False,
        "needsReview": needs_review,
        "reviewReasons": reasons,
    })


def extract_questions(text):
    sliced = body_slice(text)
    state = {"subject": "", "section": "", "type": ""}
    questions = []
    current = []

    for raw_line in sliced.splitlines():
        if FOOTER_RE.search(raw_line):
            continue
        line = clean_line(raw_line)
        if not line:
            continue
        subject_match = SUBJECT_RE.match(line)
        section_match = SECTION_RE.match(line)
        type_match = TYPE_RE.match(line)
        question_match = QUESTION_RE.match(line)

        if subject_match:
            flush_question(current, state, questions)
            current = []
            state["subject"] = subject_match.group(2).strip()
            state["section"] = ""
            state["type"] = ""
            continue
        if section_match:
            flush_question(current, state, questions)
            current = []
            state["section"] = section_match.group(2).strip()
            state["type"] = ""
            continue
        if type_match:
            flush_question(current, state, questions)
            current = []
            state["type"] = type_match.group(1)
            continue
        if question_match and state.get("type"):
            flush_question(current, state, questions)
            current = [question_match.group(2)]
            continue
        if current and not is_boundary(line):
            current.append(line)

    flush_question(current, state, questions)
    return questions


def date_index(day):
    digits = re.sub(r"\D", "", day)
    return int(digits)


def pick_from(pool, start, used):
    if not pool:
        return None
    for offset in range(len(pool)):
        item = pool[(start + offset) % len(pool)]
        if item["id"] not in used:
            return item
    return pool[start % len(pool)]


def select_daily_questions(questions, day):
    by_subject = defaultdict(list)
    for item in questions:
        by_subject[item["subject"]].append(item)
    subjects = sorted(by_subject)
    seed = date_index(day)
    subject = subjects[seed % len(subjects)]
    subject_pool = by_subject[subject]
    used = set()
    practical = [item for item in subject_pool if item["type"] == "실기"]
    oral = [item for item in subject_pool if item["type"] == "구술"]
    selected = []
    first = pick_from(practical, seed, used) or pick_from(subject_pool, seed, used)
    if first:
        selected.append(first)
        used.add(first["id"])
    second = pick_from(oral, seed // 7, used) or pick_from(subject_pool, seed // 7, used)
    if second:
        selected.append(second)
        used.add(second["id"])
    while len(selected) < 2:
        fallback = pick_from(questions, seed + len(selected), used)
        if not fallback:
            break
        selected.append(fallback)
        used.add(fallback["id"])
    return selected[:2]


def safe_json(data):
    return (
        json.dumps(data, ensure_ascii=False)
        .replace("<", "\\u003c")
        .replace(">", "\\u003e")
        .replace("&", "\\u0026")
        .replace("</script", "\\u003c/script")
    )


def render_index(quiz):
    today = html.escape(quiz["displayDate"])
    return f"""<!doctype html>
<html lang="ko">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
  <title>So02 House DashBoard</title>
  <style>
    :root {{ --bg:#f8f4f1; --surface:#fff; --ink:#242522; --muted:#6e746d; --line:#ddd7ca; --accent:#66735d; --accent-strong:#2f3d32; --accent-soft:#e9eee4; --radius:8px; }}
    * {{ box-sizing:border-box; }}
    body {{ margin:0; background:linear-gradient(180deg,#f8f4f1 0%,#f3eee7 100%); color:var(--ink); font-family:-apple-system,BlinkMacSystemFont,"Apple SD Gothic Neo","Noto Sans KR","Segoe UI",sans-serif; line-height:1.5; letter-spacing:0; }}
    main {{ width:min(760px,100%); min-height:100svh; margin:0 auto; padding:18px 14px 34px; }}
    .dashboard-hero {{ display:flex; align-items:center; justify-content:space-between; gap:12px; margin:2px 0 18px; }}
    .brand-lockup {{ display:flex; align-items:center; gap:12px; min-width:0; }}
    .logo-plate {{ width:58px; height:58px; border-radius:16px; overflow:hidden; background:#fff; border:1px solid rgba(102,115,93,.18); }}
    .logo-plate img {{ width:100%; height:100%; object-fit:cover; display:block; }}
    h1 {{ margin:0; color:var(--accent-strong); font-size:30px; line-height:1.05; font-weight:950; }}
    .today-chip {{ flex:0 0 auto; border:1px solid rgba(102,115,93,.2); border-radius:999px; background:#fff; color:var(--accent-strong); min-height:38px; padding:7px 12px; font:inherit; font-size:12px; font-weight:950; }}
    .module,.daily-word,.history-wrap {{ border:1px solid rgba(102,115,93,.18); border-radius:16px; background:rgba(255,255,255,.78); padding:14px; box-shadow:0 8px 22px rgba(36,37,34,.04); }}
    .section-head h2 {{ margin:0 0 11px; color:var(--accent-strong); font-size:21px; font-weight:950; }}
    .quick {{ display:grid; grid-template-columns:1fr 1fr; gap:9px; }}
    a {{ color:inherit; text-decoration:none; }}
    .quick a {{ display:block; min-height:74px; padding:13px; border:1px solid rgba(102,115,93,.18); border-radius:13px; background:#fbfcfa; }}
    .quick strong {{ display:block; color:var(--accent-strong); font-size:17px; font-weight:950; }}
    .quick small {{ display:block; margin-top:4px; color:var(--muted); font-size:12px; font-weight:800; }}
    .trust-note {{ margin-top:11px; padding:10px 11px; border-radius:12px; background:var(--accent-soft); color:var(--accent-strong); font-size:12.5px; font-weight:800; }}
    .daily-word {{ margin-top:14px; }}
    .daily-word-title,.history-title {{ color:var(--accent-strong); font-size:15px; font-weight:950; }}
    .daily-word p {{ margin:6px 0 0; color:#40483f; font-size:14px; font-weight:800; word-break:keep-all; }}
    .history-wrap {{ margin-top:14px; }}
    .history-bar {{ display:flex; align-items:center; justify-content:space-between; gap:10px; margin-bottom:10px; }}
    .history-summary {{ display:flex; gap:6px; flex-wrap:wrap; justify-content:flex-end; }}
    .history-summary span,.badge {{ display:inline-flex; align-items:center; min-height:25px; padding:4px 8px; border-radius:999px; background:#f3f5f0; color:var(--muted); font-size:11px; font-weight:850; }}
    .history-summary strong {{ color:var(--accent-strong); margin-left:3px; }}
    ul {{ list-style:none; padding:0; margin:0; display:grid; gap:8px; }}
    .quiz-row {{ display:flex; align-items:center; justify-content:space-between; gap:10px; padding:13px; border:1px solid rgba(102,115,93,.16); border-radius:13px; background:#fff; }}
    .date {{ color:var(--accent-strong); font-size:17px; font-weight:950; }}
    .row-meta {{ color:var(--muted); font-size:12px; font-weight:850; text-align:right; }}
    @media (max-width:520px) {{ main {{ padding:14px 10px 28px; }} h1 {{ font-size:25px; }} .quick {{ gap:7px; }} .quick a {{ min-height:66px; padding:10px; }} .quick strong {{ font-size:16px; }} .quick small {{ font-size:10.5px; }} }}
  </style>
</head>
<body>
  <main>
    <header class="dashboard-hero">
      <div class="brand-lockup">
        <div class="logo-plate"><img src="assets/soo2-logo.png" alt="So02 House"></div>
        <h1>DashBoard</h1>
      </div>
      <button class="today-chip" type="button" aria-label="오늘 날짜">{today}</button>
    </header>
    <section class="module">
      <div class="section-head"><h2>건강운동관리사 실기 대비</h2></div>
      <section class="quick" aria-label="빠른 이동">
        <a href="quizzes/quiz-today.html"><strong>오늘 실기 2문제</strong><small>미풀이 · 2문항 남음</small></a>
        <a href="wrong-note.html"><strong>오답노트 보기</strong><small>어려움·다시 볼 문제</small></a>
      </section>
      <div class="trust-note"><strong>출제 기준</strong> 기출문제 분석 자료 기준 과목별 순환 출제</div>
    </section>
    <section class="daily-word" aria-label="오늘의 한 문장">
      <div class="daily-word-title">오늘의 한 문장</div>
      <p>동작은 말로 정리하고, 말은 순서로 기억한다. 오늘은 두 문제만 정확히 끝낸다.</p>
    </section>
    <div class="history-wrap">
      <div class="history-bar">
        <div class="history-title">학습 기록</div>
        <div class="history-summary" aria-label="학습 현황">
          <span>오늘 <strong>2</strong></span>
          <span>다시 보기 <strong id="reviewCount">0</strong></span>
          <span>어려움 <strong id="hardCount">0</strong></span>
        </div>
      </div>
      <ul>
        <li><a class="quiz-row" href="quizzes/quiz-today.html"><span class="date">{today}</span><span class="row-meta"><span class="badge pending">미풀이 · 2문항</span></span></a></li>
      </ul>
    </div>
  </main>
  <script>
    (function() {{
      const key = '{RECORD_KEY}';
      let records = {{}};
      try {{ records = JSON.parse(localStorage.getItem(key) || '{{}}'); }} catch (error) {{ records = {{}}; }}
      const values = Object.values(records);
      const review = values.filter(item => item && item.status === 'review').length;
      const hard = values.filter(item => item && item.status === 'hard').length;
      const reviewCount = document.getElementById('reviewCount');
      const hardCount = document.getElementById('hardCount');
      if (reviewCount) reviewCount.textContent = review;
      if (hardCount) hardCount.textContent = hard;
    }})();
  </script>
</body>
</html>
"""


def question_card(item, index):
    q = html.escape(item["question"])
    meta = " / ".join(html.escape(str(value)) for value in (item["subject"], item["section"], item["type"], item["year"]) if value)
    method = html.escape(item.get("methodGuide", ""))
    tip = html.escape(item.get("memoryTip", ""))
    return f"""<article class="question-card" data-question-id="{html.escape(item['id'])}">
      <div class="q-head"><span class="q-count">{index + 1}/2</span><span class="topic">{meta}</span></div>
      <p class="question">{q}</p>
      <details class="guide"><summary>수행·답변 가이드</summary><p>{method}</p><p>{tip}</p></details>
      <div class="actions">
        <button type="button" data-status="done">완료</button>
        <button type="button" data-status="review">다시 보기</button>
        <button type="button" data-status="hard">어려움</button>
      </div>
    </article>"""


def render_quiz(quiz):
    cards = "\n".join(question_card(item, index) for index, item in enumerate(quiz["questions"]))
    return f"""<!doctype html>
<html lang="ko">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
  <title>건강운동관리사 실기 대비 | 오늘 실기 2문제</title>
  <style>
    :root {{ --bg:#f8f4f1; --surface:#fff; --ink:#242522; --muted:#6e746d; --line:#ddd7ca; --accent:#66735d; --accent-strong:#2f3d32; --accent-soft:#e9eee4; --danger:#b64032; --warn:#a16b18; --ok:#287a4b; }}
    * {{ box-sizing:border-box; }}
    body {{ margin:0; background:linear-gradient(180deg,#f8f4f1 0%,#f3eee7 100%); color:var(--ink); font-family:-apple-system,BlinkMacSystemFont,"Apple SD Gothic Neo","Noto Sans KR","Segoe UI",sans-serif; line-height:1.5; letter-spacing:0; }}
    .app {{ width:min(760px,100%); min-height:100svh; margin:0 auto; }}
    .topbar {{ position:sticky; top:0; z-index:10; background:rgba(248,244,241,.94); border-bottom:1px solid rgba(102,115,93,.16); backdrop-filter:blur(14px); }}
    .topbar-inner {{ padding:14px 14px 10px; }}
    .title-row {{ display:flex; align-items:center; justify-content:space-between; gap:12px; }}
    h1 {{ margin:0; color:var(--accent-strong); font-size:21px; font-weight:950; }}
    .progress-chip {{ min-width:58px; padding:8px 11px; border-radius:999px; background:var(--accent-soft); color:var(--accent-strong); text-align:center; font-size:12px; font-weight:950; }}
    .progress-track {{ height:5px; margin-top:10px; overflow:hidden; border-radius:999px; background:#e8ece6; }}
    .progress-bar {{ width:0%; height:100%; border-radius:inherit; background:var(--accent); transition:width .25s ease; }}
    main {{ padding:16px 14px 26px; }}
    .question-card {{ display:none; padding:16px; border:1px solid rgba(102,115,93,.18); border-radius:14px; background:rgba(255,255,255,.78); }}
    .question-card.active {{ display:block; }}
    .q-head {{ display:flex; align-items:center; justify-content:space-between; gap:12px; margin-bottom:14px; }}
    .q-count {{ color:var(--accent-strong); font-size:13px; font-weight:900; padding:6px 10px; border-radius:999px; background:var(--accent-soft); }}
    .topic {{ color:var(--muted); font-size:12px; font-weight:800; text-align:right; }}
    .question {{ margin:0 0 14px; font-size:20px; font-weight:900; line-height:1.48; word-break:keep-all; overflow-wrap:anywhere; white-space:pre-line; }}
    .guide {{ margin:12px 0; border:1px solid rgba(102,115,93,.16); border-radius:12px; background:#fbfcfa; padding:10px 12px; }}
    .guide summary {{ cursor:pointer; color:var(--accent-strong); font-size:13px; font-weight:950; }}
    .guide p {{ margin:8px 0 0; color:var(--muted); font-size:13px; font-weight:750; }}
    .actions {{ display:grid; grid-template-columns:1fr 1fr 1fr; gap:8px; margin-top:15px; }}
    button {{ min-height:46px; border:1px solid rgba(102,115,93,.2); border-radius:12px; background:#fff; color:var(--accent-strong); font:inherit; font-size:14px; font-weight:950; }}
    button[data-status="done"] {{ background:var(--accent); color:#fff; }}
    button[data-status="review"] {{ background:#fff8e8; color:#7d5113; }}
    button[data-status="hard"] {{ background:#fff0ed; color:#953428; }}
    .nav {{ display:flex; justify-content:space-between; gap:8px; margin-top:13px; }}
    .nav a,.nav button {{ display:inline-flex; align-items:center; justify-content:center; min-height:42px; padding:8px 12px; border-radius:999px; text-decoration:none; }}
    .nav a {{ color:var(--accent-strong); background:var(--accent-soft); font-size:13px; font-weight:950; }}
    .result {{ display:none; padding:16px; border:1px solid rgba(102,115,93,.18); border-radius:14px; background:#fff; }}
    .result.active {{ display:block; }}
    .result h2 {{ margin:0 0 8px; color:var(--accent-strong); font-size:22px; }}
    .result p {{ margin:0; color:var(--muted); font-weight:800; }}
    @media (max-width:520px) {{ main {{ padding:12px 10px 24px; }} .question {{ font-size:18px; }} .actions {{ grid-template-columns:1fr; }} }}
  </style>
</head>
<body>
  <script id="quiz-data" type="application/json">{safe_json(quiz)}</script>
  <div class="app">
    <header class="topbar">
      <div class="topbar-inner">
        <div class="title-row"><h1>건강운동관리사 실기 대비</h1><div class="progress-chip" id="position">1/2</div></div>
        <div class="progress-track"><div class="progress-bar" id="progress"></div></div>
      </div>
    </header>
    <main>
      <section id="cards">{cards}</section>
      <section id="result" class="result"><h2>오늘 2문제 기록 완료</h2><p>다시 보기와 어려움으로 표시한 문제는 오답노트에서 확인할 수 있습니다.</p></section>
      <div class="nav"><a href="../index.html">DashBoard</a><a href="../wrong-note.html">오답노트 보기</a><button type="button" id="nextBtn">다음</button></div>
    </main>
  </div>
  <script>
    (function() {{
      const key = '{RECORD_KEY}';
      const quiz = JSON.parse(document.getElementById('quiz-data').textContent);
      const cards = Array.from(document.querySelectorAll('.question-card'));
      const position = document.getElementById('position');
      const progress = document.getElementById('progress');
      const result = document.getElementById('result');
      const nextBtn = document.getElementById('nextBtn');
      let current = 0;
      let records = {{}};
      try {{ records = JSON.parse(localStorage.getItem(key) || '{{}}'); }} catch (error) {{ records = {{}}; }}
      function save(id, status) {{
        records[id] = {{ status, quizId: quiz.quizId, date: quiz.date, updatedAt: new Date().toISOString() }};
        localStorage.setItem(key, JSON.stringify(records));
      }}
      function render() {{
        cards.forEach((card, index) => card.classList.toggle('active', index === current));
        const done = Math.min(current + 1, cards.length);
        position.textContent = current < cards.length ? done + '/' + cards.length : '완료';
        progress.style.width = Math.min(current, cards.length) / cards.length * 100 + '%';
        result.classList.toggle('active', current >= cards.length);
        nextBtn.textContent = current >= cards.length - 1 ? '완료 보기' : '다음';
      }}
      document.querySelectorAll('.actions button').forEach(button => {{
        button.addEventListener('click', function() {{
          const card = button.closest('.question-card');
          save(card.dataset.questionId, button.dataset.status);
          current = Math.min(current + 1, cards.length);
          render();
        }});
      }});
      nextBtn.addEventListener('click', function() {{
        current = Math.min(current + 1, cards.length);
        render();
      }});
      render();
    }})();
  </script>
</body>
</html>
"""


def render_wrong_note(questions):
    return f"""<!doctype html>
<html lang="ko">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
  <title>소빵이의 오답노트</title>
  <style>
    :root {{ --bg:#f3f5f0; --surface:#fff; --ink:#17201a; --muted:#69736c; --line:#dfe5dc; --accent:#2f6b4f; --accent-dark:#214735; --danger:#b64032; --warn:#a16b18; --sage:#e9eee4; }}
    * {{ box-sizing:border-box; }}
    body {{ margin:0; background:var(--bg); color:var(--ink); font-family:-apple-system,BlinkMacSystemFont,"Apple SD Gothic Neo","Noto Sans KR",sans-serif; line-height:1.5; letter-spacing:0; }}
    main {{ width:min(820px,100%); min-height:100svh; margin:0 auto; padding:22px 16px 32px; background:var(--surface); }}
    .topline {{ display:flex; align-items:flex-start; justify-content:space-between; gap:14px; margin-bottom:16px; }}
    .back {{ color:var(--accent); font-size:13px; font-weight:950; text-decoration:none; white-space:nowrap; }}
    h1 {{ margin:0; color:var(--accent-dark); font-size:28px; line-height:1.15; font-weight:950; }}
    .subtitle {{ margin:4px 0 0; color:var(--muted); font-size:13px; font-weight:800; }}
    .stats {{ display:flex; flex-wrap:wrap; gap:7px; margin:2px 0 16px; }}
    .stat {{ display:inline-flex; align-items:center; gap:5px; min-height:29px; padding:5px 9px; border:1px solid rgba(102,115,93,.18); border-radius:999px; background:#fbfcfa; }}
    .stat span {{ color:var(--muted); font-size:11.5px; font-weight:850; }}
    .stat strong {{ color:var(--accent-dark); font-size:12.5px; font-weight:950; }}
    .list {{ display:grid; gap:12px; }}
    .empty {{ padding:18px; border:1px solid var(--line); border-radius:13px; background:#fbfcfa; color:var(--muted); font-weight:850; }}
    .card {{ border:1px solid var(--line); border-radius:13px; background:#fff; overflow:hidden; }}
    .card-head {{ padding:14px; border-bottom:1px solid var(--line); background:#fbfcfa; }}
    .topic {{ font-size:15px; font-weight:950; }}
    .sub {{ margin-top:3px; color:var(--muted); font-size:13px; font-weight:700; }}
    .body {{ padding:14px; }}
    .question {{ margin:0 0 11px; font-size:15.2px; font-weight:850; line-height:1.46; white-space:pre-line; word-break:keep-all; overflow-wrap:anywhere; }}
    .pill {{ display:inline-flex; min-height:25px; align-items:center; padding:4px 8px; border-radius:999px; background:var(--sage); color:var(--accent-dark); font-size:12px; font-weight:950; }}
    .pill.hard {{ background:#fff0ed; color:#953428; }}
    .pill.review {{ background:#fff8e8; color:#7d5113; }}
  </style>
</head>
<body>
  <script id="question-data" type="application/json">{safe_json(questions)}</script>
  <main>
    <div class="topline"><div><h1>소빵이의 오답노트</h1><p class="subtitle">어려움·다시 볼 문제</p></div><a class="back" href="index.html">DashBoard</a></div>
    <div class="stats">
      <div class="stat"><span>다시 보기</span><strong id="reviewCount">0</strong></div>
      <div class="stat"><span>어려움</span><strong id="hardCount">0</strong></div>
    </div>
    <section class="list" id="list"></section>
  </main>
  <script>
    (function() {{
      const key = '{RECORD_KEY}';
      const questions = JSON.parse(document.getElementById('question-data').textContent);
      const byId = new Map(questions.map(item => [item.id, item]));
      let records = {{}};
      try {{ records = JSON.parse(localStorage.getItem(key) || '{{}}'); }} catch (error) {{ records = {{}}; }}
      const items = Object.entries(records).filter(([, record]) => record && (record.status === 'review' || record.status === 'hard'));
      const reviewCount = items.filter(([, record]) => record.status === 'review').length;
      const hardCount = items.filter(([, record]) => record.status === 'hard').length;
      document.getElementById('reviewCount').textContent = reviewCount;
      document.getElementById('hardCount').textContent = hardCount;
      const list = document.getElementById('list');
      function escapeHtml(value) {{
        return String(value == null ? '' : value).replace(/[&<>"']/g, ch => ({{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}}[ch]));
      }}
      if (!items.length) {{
        list.innerHTML = '<div class="empty">아직 다시 볼 문제로 표시한 항목이 없습니다.</div>';
        return;
      }}
      list.innerHTML = items.map(([id, record]) => {{
        const q = byId.get(id);
        if (!q) return '';
        const label = record.status === 'hard' ? '어려움' : '다시 보기';
        const cls = record.status === 'hard' ? 'hard' : 'review';
        return '<article class="card"><div class="card-head"><div class="topic">' + escapeHtml(q.subject) + ' / ' + escapeHtml(q.section) + '</div><div class="sub">' + escapeHtml(q.type) + ' · ' + escapeHtml(q.year || '') + ' · <span class="pill ' + cls + '">' + label + '</span></div></div><div class="body"><p class="question">' + escapeHtml(q.question) + '</p></div></article>';
      }}).join('');
    }})();
  </script>
</body>
</html>
"""


def clean_old_outputs():
    for directory in (ROOT / "quizzes", ROOT / "data" / "quizzes"):
        directory.mkdir(parents=True, exist_ok=True)
        for path in directory.glob("*"):
            if path.is_file():
                path.unlink()
    bank_dir = ROOT / "data" / "question-bank"
    if bank_dir.exists():
        for path in bank_dir.glob("*.jsonl"):
            path.unlink()
    image_dir = ROOT / "assets" / "question-images"
    if image_dir.exists():
        shutil.rmtree(image_dir)


def write_json(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_text(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def summarize(questions):
    return {
        "total": len(questions),
        "bySubject": dict(Counter(item["subject"] for item in questions)),
        "byType": dict(Counter(item["type"] for item in questions)),
        "sourceVerified": dict(Counter(str(bool(item["sourceVerified"])).lower() for item in questions)),
        "needsReview": dict(Counter(str(bool(item["needsReview"])).lower() for item in questions)),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--pdf", type=Path, default=DEFAULT_PDF)
    parser.add_argument("--date", default=date.today().isoformat())
    parser.add_argument("--keep-old", action="store_true")
    args = parser.parse_args()

    text = run_pdftotext(args.pdf)
    questions = extract_questions(text)
    if not questions:
        raise RuntimeError("no questions extracted")
    daily = {
        "quizId": f"{args.date}-practical-daily",
        "date": args.date,
        "displayDate": args.date,
        "title": "건강운동관리사 실기 대비",
        "questionCount": 2,
        "questions": select_daily_questions(questions, args.date),
    }
    if not args.keep_old:
        clean_old_outputs()
    write_json(DATA_PATH, questions)
    write_json(QUIZ_DATA_PATH, daily)
    write_text(INDEX_PATH, render_index(daily))
    write_text(QUIZ_HTML_PATH, render_quiz(daily))
    write_text(WRONG_NOTE_PATH, render_wrong_note(questions))
    print(json.dumps(summarize(questions), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
