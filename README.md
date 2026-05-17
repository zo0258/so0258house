# 건강운동관리사 데일리 퀴즈

건강운동관리사 필기시험 준비용 모바일 퀴즈 생성 프로젝트입니다.

## 바로 풀기

GitHub Pages 배포 후 `index.html`에서 일자별 퀴즈를 선택합니다.

## 매일 생성

```bash
python3 scripts/generate_daily_quiz.py --date YYYY-MM-DD --html
python3 scripts/build_static_site.py --site-dir .
```

## 주요 경로

- `materials/raw/kspo/`: 공식 기출 PDF 원본
- `data/question-bank/`: 추출된 문제은행
- `data/quizzes/`: 일자별 퀴즈 JSON
- `quizzes/`: GitHub Pages용 HTML
- `scripts/`: 다운로드, 추출, 생성, 검증 스크립트
