# Google Sheets 실시간 동기화

## 목적

GitHub Pages 퀴즈 결과를 Google Apps Script Web App으로 제출하고, Google Sheets에 즉시 저장한다. OpenClaw는 Sheets 데이터를 읽어 메인 대시보드와 오답노트를 재생성한다.

## 구성

```text
퀴즈 HTML
  -> 결과 제출
Google Apps Script Web App
  -> attempts 시트 appendRow
Google Sheets
  -> OpenClaw 동기화
GitHub Pages 재배포
```

## 설정 순서

1. Google Sheets 파일을 만든다.
2. 확장 프로그램 > Apps Script를 연다.
3. `apps-script/Code.gs` 내용을 붙여넣는다.
4. `setup()`을 1회 실행해 `attempts` 시트와 헤더를 만든다.
5. 배포 > 새 배포 > 웹 앱을 선택한다.
6. 실행 사용자: 본인
7. 액세스 권한: 링크가 있는 모든 사용자
8. 생성된 Web App URL을 `config/sync.json`의 `submitUrl`에 넣고 `enabled`를 `true`로 바꾼다.
9. 퀴즈 HTML을 다시 생성하고 GitHub Pages에 배포한다.

## OpenClaw 동기화 명령

Sheets에 쌓인 제출 결과를 읽어 로컬 오답노트와 공개 페이지를 갱신한다.

```bash
python3 scripts/sync_google_sheet_results.py
```

`config/sync.json`의 `csvUrl`이 비어 있으면 아래처럼 직접 넘길 수 있다.

```bash
python3 scripts/sync_google_sheet_results.py --csv-url "https://docs.google.com/spreadsheets/d/SPREADSHEET_ID/export?format=csv&gid=0"
```

## 현재 한계

- 제출은 즉시 Google Sheets에 저장된다.
- 메인 대시보드와 오답노트 반영은 OpenClaw가 Sheets 데이터를 읽어 재빌드한 뒤 반영된다.
- 따라서 화면 반영은 완전 실시간이 아니라, 수동 실행 또는 cron 주기에 따라 몇 분 안에 반영되는 구조다.
