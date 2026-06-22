#!/usr/bin/env python3
import json
import re
from collections import Counter
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
QUESTIONS_PATH = ROOT / "data" / "practical-questions.json"
ANSWER_BANK_PATH = ROOT / "data" / "practical-answer-bank.json"
AUDIT_JSON_PATH = ROOT / "data" / "verification" / "practical-question-extraction-audit.json"
PLAN_DOC_PATH = ROOT / "docs" / "ios-app-plan" / "12-question-answer-bank-plan.md"
AUDIT_DOC_PATH = ROOT / "docs" / "ios-app-plan" / "13-question-extraction-audit.md"
CHECKED_AT = "2026-06-22"


PRIORITY_SUBJECT_PATTERNS = {
    "건강·체력측정평가": [
        "위험군",
        "혈압",
        "대사증후군",
        "PAR-Q",
        "PAP-Q",
        "공복혈당",
        "콜레스테롤",
    ],
    "트레이닝방법론": [
        "저항",
        "근력",
        "RM",
        "세트",
        "반복",
        "트레이닝",
    ],
    "운동손상평가 및 재활": [
        "평가",
        "검사",
        "재활",
        "손상",
        "테스트",
    ],
}

REFERENCE_SOURCES = {
    "건강·체력측정평가": [
        {
            "title": "ACSM Physical Activity Guidelines",
            "url": "https://acsm.org/education-resources/trending-topics-resources/physical-activity-guidelines/",
            "type": "official",
            "checkedAt": CHECKED_AT,
        },
        {
            "title": "CDC High Blood Pressure",
            "url": "https://www.cdc.gov/high-blood-pressure/",
            "type": "official",
            "checkedAt": CHECKED_AT,
        },
    ],
    "트레이닝방법론": [
        {
            "title": "ACSM Resistance Training Guidelines Update",
            "url": "https://acsm.org/resistance-training-guidelines-update-2026/",
            "type": "official",
            "checkedAt": CHECKED_AT,
        },
        {
            "title": "CDC Adult Physical Activity Guidelines",
            "url": "https://www.cdc.gov/physical-activity-basics/guidelines/adults.html",
            "type": "official",
            "checkedAt": CHECKED_AT,
        },
    ],
    "운동손상평가 및 재활": [
        {
            "title": "Merck Manual Professional - Sports Injuries",
            "url": "https://www.merckmanuals.com/professional/injuries-poisoning/sports-injury",
            "type": "trusted_web",
            "checkedAt": CHECKED_AT,
        },
        {
            "title": "NATA Position Statements",
            "url": "https://www.nata.org/practice-patient-care/health-issues",
            "type": "trusted_web",
            "checkedAt": CHECKED_AT,
        },
    ],
}

TODAY_DRAFTS = {
    "practical-010": {
        "modelAnswer": "검증 전 초안: 30초 의자 앉았다 일어서기 검사는 노인의 하지 근지구력을 평가하는 검사다. 팔은 가슴 앞에 교차하고 의자에 앉은 자세에서 시작해, 30초 동안 완전히 일어섰다가 다시 앉은 횟수를 센다.",
        "performanceSteps": [
            "등받이가 있는 안정된 의자를 벽에 고정하거나 미끄러지지 않게 둔다.",
            "대상자는 의자 중앙에 앉고 발은 바닥에 평평하게 둔다.",
            "팔은 가슴 앞에서 교차해 손으로 밀고 일어서지 않게 한다.",
            "시작 신호 후 완전히 일어섰다가 다시 앉는 동작을 30초 동안 반복하게 한다.",
            "30초 동안 완전한 일어서기 횟수만 기록하고 통증, 어지러움, 균형 상실 시 중지한다.",
        ],
        "oralAnswerStructure": [
            "검사 목적",
            "준비 자세",
            "시범과 안전 주의",
            "30초 측정과 기록 기준",
        ],
        "keyPoints": ["노인 하지 근지구력", "팔 가슴 앞 교차", "30초", "완전한 일어서기 횟수"],
        "commonMistakes": ["팔로 허벅지나 의자를 밀게 하는 것", "반쯤 일어난 동작까지 횟수로 세는 것", "균형/어지러움 확인 없이 진행하는 것"],
        "memoryTip": "의자-팔교차-30초-완전기립 순서로 말한다.",
    },
    "practical-055": {
        "modelAnswer": "검증 전 초안: 램프 프로토콜은 운동부하검사에서 운동 강도를 계단식으로 크게 올리지 않고 일정한 기울기로 연속 증가시키는 방식이다. 대상자의 능력에 맞춰 목표 검사 시간이 되도록 증가율을 정하고, 심박수, 혈압, 심전도, 자각운동강도, 증상을 관찰한다.",
        "performanceSteps": [
            "대상자 상태와 예상 운동능력을 확인한다.",
            "목표 검사 시간에 맞춰 부하 증가율을 정한다.",
            "낮은 부하에서 시작해 매분 또는 연속적으로 부하를 점진 증가시킨다.",
            "심박수, 혈압, 심전도, RPE, 증상을 반복 확인한다.",
            "종료 기준에 도달하면 회복기 관찰을 진행한다.",
        ],
        "oralAnswerStructure": ["정의", "부하 증가 방식", "관찰 항목", "종료/회복기 관리"],
        "keyPoints": ["연속적 점진 증가", "개인 능력 맞춤", "심전도/혈압/심박수/RPE 관찰", "종료 기준"],
        "commonMistakes": ["계단식 프로토콜과 혼동하는 것", "증상 및 심전도 관찰을 빼는 것"],
        "memoryTip": "Ramp는 계단이 아니라 경사로다.",
    },
    "practical-068": {
        "modelAnswer": "검증 전 초안: 장시간 유산소 운동 또는 지구성 훈련 후 최대산소섭취량 증가는 심박출량 증가, 활동근의 모세혈관화 증가, 미토콘드리아와 산화효소 활성 증가처럼 산소 운반과 이용 능력이 함께 좋아지기 때문이다.",
        "performanceSteps": [],
        "oralAnswerStructure": ["중심성 적응", "말초성 적응", "산소 이용 능력"],
        "keyPoints": ["심박출량 증가", "모세혈관 밀도 증가", "미토콘드리아 증가", "산화효소 활성 증가"],
        "commonMistakes": ["폐 환기만 원인으로 말하는 것", "심혈관 적응과 근육 적응을 구분하지 않는 것"],
        "memoryTip": "VO2max는 운반(심장·혈액) + 이용(근육·미토콘드리아)이다.",
    },
    "practical-143": {
        "modelAnswer": "검증 전 초안: 패트릭 테스트는 FABER 자세로 고관절과 천장관절 통증 유발 여부를 보는 검사다. 피검자의 오른쪽 다리를 굽혀 발목을 반대쪽 무릎 위에 놓고, 검사자는 반대쪽 골반을 고정한 뒤 오른쪽 무릎을 아래로 부드럽게 눌러 통증과 가동범위를 확인한다.",
        "performanceSteps": [
            "대상자를 바로 눕힌다.",
            "오른쪽 고관절을 굴곡, 외전, 외회전해 오른쪽 발목을 왼쪽 무릎 위에 둔다.",
            "반대쪽 골반을 손으로 고정한다.",
            "오른쪽 무릎을 검사대 방향으로 천천히 눌러 통증 위치와 제한을 확인한다.",
            "고관절 전방 통증과 천장관절 주변 통증을 구분해 기록한다.",
        ],
        "oralAnswerStructure": ["검사 목적", "FABER 자세 만들기", "골반 고정", "통증 위치 해석"],
        "keyPoints": ["FABER", "골반 고정", "무릎 하방 압박", "고관절/천장관절 통증 구분"],
        "commonMistakes": ["골반을 고정하지 않는 것", "강하게 눌러 통증을 과도하게 유발하는 것", "통증 위치를 묻지 않는 것"],
        "memoryTip": "FABER 만든 뒤 골반 고정, 무릎은 천천히.",
    },
}


def load_questions():
    with QUESTIONS_PATH.open("r", encoding="utf-8") as file:
        return json.load(file)


def normalize(text):
    return re.sub(r"\s+", " ", text or "").strip()


def date_seed(value):
    return value.year * 10000 + value.month * 100 + value.day


def positive_mod(value, divisor):
    return value % divisor if divisor else 0


def score(question, index, seed, count, subjects, sections):
    duplicate_subject = 10.0 if question["subject"] in subjects else 0.0
    duplicate_section = 4.0 if question["section"] in sections else 0.0
    rotation = positive_mod(index - seed, count) / max(count, 1)
    return duplicate_subject + duplicate_section + rotation


def pick_diverse(pool, seed, selected, used):
    candidates = [question for question in pool if question["id"] not in used]
    if not candidates:
        return None
    subjects = {question["subject"] for question in selected}
    sections = {question["section"] for question in selected}
    return min(
        enumerate(candidates),
        key=lambda item: score(item[1], item[0], seed, len(candidates), subjects, sections),
    )[1]


def pick_from(pool, start, used):
    if not pool:
        return None
    for offset in range(len(pool)):
        item = pool[(start + offset) % len(pool)]
        if item["id"] not in used:
            return item
    return pool[start % len(pool)]


def select_today_questions(questions, today=date(2026, 6, 22)):
    seed = date_seed(today)
    practical = [question for question in questions if question["type"] == "실기"]
    oral = [question for question in questions if question["type"] == "구술"]
    pools = [practical, oral, practical, oral]
    selected = []
    used = set()
    for offset, pool in enumerate(pools):
        item = pick_diverse(pool, seed + offset * 17, selected, used)
        if item:
            selected.append(item)
            used.add(item["id"])
    while len(selected) < 4:
        item = pick_from(questions, seed + len(selected), used)
        if not item:
            break
        selected.append(item)
        used.add(item["id"])
    return {question["id"] for question in selected[:4]}


def priority_reasons(question, today_ids):
    reasons = []
    text = f"{question['section']} {question['question']}"
    if question["id"] in today_ids:
        reasons.append("today_2026-06-22")
    if question.get("year") == 2025:
        reasons.append("year_2025")
    for subject, patterns in PRIORITY_SUBJECT_PATTERNS.items():
        if question["subject"] == subject and any(pattern in text for pattern in patterns):
            reasons.append("topic_priority")
            break
    return reasons


def answer_entry(question, today_ids):
    reasons = priority_reasons(question, today_ids)
    draft = TODAY_DRAFTS.get(question["id"])
    review_notes = [
        "공식 원문/답안 근거 대조 전까지 앱에서 확정 답안으로 노출하지 않는다.",
    ]
    if draft:
        review_notes.append("오늘 출제 4문제용 검증 전 초안이다. sourceVerified true로 승격하려면 공식/전문 출처 대조가 필요하다.")
    else:
        review_notes.append("modelAnswer는 다음 단계에서 출처 확인 후 채운다.")
    if reasons:
        review_notes.append(f"1차 우선순위: {', '.join(reasons)}")

    return {
        "questionId": question["id"],
        "answerStatus": "draft" if draft else "needs_review",
        "modelAnswer": draft["modelAnswer"] if draft else "",
        "performanceSteps": draft["performanceSteps"] if draft else [],
        "oralAnswerStructure": draft["oralAnswerStructure"] if draft else [],
        "keyPoints": draft["keyPoints"] if draft else [],
        "commonMistakes": draft["commonMistakes"] if draft else [],
        "memoryTip": draft["memoryTip"] if draft else question.get("memoryTip", ""),
        "sourceRefs": REFERENCE_SOURCES.get(question["subject"], []),
        "sourceVerified": False,
        "needsReview": True,
        "reviewNotes": review_notes,
    }


def suspicious_terms(question):
    text = question["question"]
    flags = []
    if "mmg" in text:
        flags.append({"term": "mmg", "suggested": "mmHg", "reason": "혈압 단위 오타 의심"})
    if "PAP-Q" in text:
        flags.append({"term": "PAP-Q", "suggested": "PAR-Q", "reason": "신체활동 준비 설문 약어 오타 의심"})
    if "  " in text or "\ufffd" in text:
        flags.append({"term": "broken_spacing_or_char", "suggested": None, "reason": "공백/깨진 문자 확인 필요"})
    return flags


def corrected_question(question, flags):
    corrected = question["question"]
    for flag in flags:
        if flag["term"] == "mmg":
            corrected = corrected.replace("mmg", "mmHg")
        if flag["term"] == "PAP-Q":
            corrected = corrected.replace("PAP-Q", "PAR-Q")
    return corrected if corrected != question["question"] else None


def build_audit(questions, answer_bank):
    ids = [question["id"] for question in questions]
    normalized_questions = [normalize(question["question"]) for question in questions]
    duplicate_ids = sorted([item for item, count in Counter(ids).items() if count > 1])
    duplicate_texts = [
        {"question": item, "count": count}
        for item, count in Counter(normalized_questions).items()
        if count > 1
    ]

    suspicious = []
    corrected = []
    for question in questions:
        flags = suspicious_terms(question)
        if not flags:
            continue
        item = {
            "questionId": question["id"],
            "year": question.get("year"),
            "subject": question["subject"],
            "section": question["section"],
            "flags": flags,
        }
        suspicious.append(item)
        proposed = corrected_question(question, flags)
        if proposed:
            corrected.append({
                **item,
                "correctedQuestion": proposed,
                "correctionReason": "; ".join(flag["reason"] for flag in flags),
                "needsReview": True,
            })

    return {
        "checkedAt": CHECKED_AT,
        "totalQuestions": len(questions),
        "answerBankEntries": len(answer_bank),
        "subjectCounts": dict(sorted(Counter(question["subject"] for question in questions).items())),
        "typeCounts": dict(sorted(Counter(question["type"] for question in questions).items())),
        "yearCounts": dict(sorted(Counter(str(question.get("year")) for question in questions).items())),
        "duplicateIds": duplicate_ids,
        "duplicateQuestionTexts": duplicate_texts,
        "suspiciousExtractionIssues": suspicious,
        "correctedQuestionProposals": corrected,
        "needsReviewQuestionIds": [entry["questionId"] for entry in answer_bank if entry["needsReview"]],
        "sourceVerifiedCount": sum(1 for entry in answer_bank if entry["sourceVerified"]),
        "notes": [
            "PDF 원문은 materials/raw/kspo 아래에 보존되어 있으나, 이번 1차에서는 자동 원문 대조 확정 판정을 하지 않았다.",
            "문제 원문 수정은 data/practical-questions.json에 직접 반영하지 않고 correctedQuestion 제안으로만 남긴다.",
        ],
    }


def write_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as file:
        json.dump(value, file, ensure_ascii=False, indent=2)
        file.write("\n")


def write_plan_doc():
    PLAN_DOC_PATH.write_text(
        """# Question Answer Bank Plan

## 왜 Answer Bank가 먼저인가

iOS MVP는 199개 문제 로딩, 오늘 4문제 선택, 기록 저장까지 동작한다. 다음 품질 병목은 화면이 아니라 답안 데이터다. 문제 원문과 답안/수행방법/암기팁이 검증되지 않으면 앱은 매일 열 수 있어도 학습 신뢰도가 낮다. 그래서 실기기 UI QA 전에 정적 answer bank를 먼저 분리한다.

## 문제 발췌 검증 기준

- `data/practical-questions.json` 원문은 직접 수정하지 않는다.
- PDF 원문과 대조해 오탈자나 추출 오류가 확인된 경우에만 별도 `correctedQuestion` 제안으로 기록한다.
- 점검 항목은 총 문제 수, 중복 ID, 중복 문장, 연도 누락/오인식, 과목/section/type 분류, 깨진 문자, 단위 오타, PAR-Q 등 용어 오타다.
- 이번 1차에서는 자동 확정 판정 대신 의심 항목을 audit로 분리한다.

## Answer Bank 필드 구조

`data/practical-answer-bank.json`은 앱 번들에 넣을 정적 답안 후보 파일이다.

```json
{
  "questionId": "practical-001",
  "answerStatus": "draft | verified | needs_review",
  "modelAnswer": "",
  "performanceSteps": [],
  "oralAnswerStructure": [],
  "keyPoints": [],
  "commonMistakes": [],
  "memoryTip": "",
  "sourceRefs": [],
  "sourceVerified": false,
  "needsReview": true,
  "reviewNotes": []
}
```

## 출처 검증 기준

출처 우선순위는 공식 시험 시행기관/자격 자료, ACSM, NSCA, AHA/CDC/WHO, 국내 대학·학회·공공기관, 전문서적·교육자료 순서다. 일반 블로그/카페는 보조 참고로만 쓰고 `sourceVerified: true`로 두지 않는다.

의학·운동처방 수치가 포함된 문제는 `checkedAt`을 남긴다. ACSM 구버전 기준과 최신 기준이 충돌하면 `reviewNotes`에 `기출 당시 기준 확인 필요`를 남긴다.

## 199개 전체 구축 전략

1. 모든 `questionId`에 answer bank 엔트리를 먼저 만든다.
2. 출처가 확인되지 않은 항목은 `answerStatus: needs_review`, `sourceVerified: false`로 둔다.
3. 우선순위 문제군부터 `modelAnswer`, `performanceSteps`, `oralAnswerStructure`, `keyPoints`, `commonMistakes`를 채운다.
4. 검증 완료 항목만 `answerStatus: verified`로 승격한다.
5. 앱은 answer bank가 없어도 문제 로딩이 되도록 하고, answer bank가 있으면 보조 답안으로 붙인다.

## 1차 우선순위 문제군

- 2026-06-22 오늘 출제 4문제
- 2025년 문제
- 건강·체력측정평가: 위험군 분류, 혈압, 대사증후군, PAR-Q 관련 문항
- 트레이닝방법론: 저항성 트레이닝, RM, 세트/반복 관련 문항
- 운동손상평가 및 재활: 반복 출제되는 평가/검사/재활 문항

## 수동 검수 필요 기준

- PDF 원문 대조가 끝나지 않은 문제
- 단위/약어 오타 의심 문제
- 기준 연도에 따라 답이 달라질 수 있는 문제
- 출처가 블로그/카페 수준에 그치는 문제
- `modelAnswer`를 채우려면 전문서적 확인이 필요한 문제

## 앱 반영 계획

이번 단계에서는 `AnswerBankModels.swift`와 `AnswerBankRepository.swift`만 추가한다. `PracticeView`에서 answer bank를 실제 표시하는 작업은 다음 단계로 둔다. 반영 시에는 `questionId`로 문제와 답안 엔트리를 매칭하고, 누락된 답안은 화면에서 조용히 숨긴다.

끝.
""",
        encoding="utf-8",
    )


def write_audit_doc(audit):
    corrected_lines = "\n".join(
        f"- `{item['questionId']}`: {item['correctionReason']}"
        for item in audit["correctedQuestionProposals"]
    ) or "- 없음"
    duplicate_text_lines = "\n".join(
        f"- {item['count']}회: {item['question'][:120]}"
        for item in audit["duplicateQuestionTexts"]
    ) or "- 없음"
    subject_lines = "\n".join(f"- {key}: {value}" for key, value in audit["subjectCounts"].items())
    type_lines = "\n".join(f"- {key}: {value}" for key, value in audit["typeCounts"].items())
    year_lines = "\n".join(f"- {key}: {value}" for key, value in audit["yearCounts"].items())

    AUDIT_DOC_PATH.write_text(
        f"""# Question Extraction Audit

## 요약

- 점검일: {audit['checkedAt']}
- 총 문제 수: {audit['totalQuestions']}
- answer bank 엔트리 수: {audit['answerBankEntries']}
- 중복 ID: {len(audit['duplicateIds'])}
- 중복 의심 문장: {len(audit['duplicateQuestionTexts'])}
- 추출 오류 의심 문제: {len(audit['suspiciousExtractionIssues'])}
- correctedQuestion 제안 문제: {len(audit['correctedQuestionProposals'])}
- needsReview 문제: {len(audit['needsReviewQuestionIds'])}
- sourceVerified 문제: {audit['sourceVerifiedCount']}

## 과목별 문제 수

{subject_lines}

## Type별 문제 수

{type_lines}

## 연도별 문제 수

{year_lines}

## 중복 의심 문제

{duplicate_text_lines}

## 추출 오류 의심 문제

{corrected_lines}

## correctedQuestion 필요 문제

{corrected_lines}

## needsReview 기준

1차 answer bank는 199개 전체를 포함하지만, 공식 원문/답안/전문 출처 대조가 끝나지 않은 항목은 모두 `needsReview: true`로 유지했다. 앱에서 확정 답안처럼 노출하기 전 수동 검수가 필요하다.

## 다음 액션

1. correctedQuestion 제안 항목을 PDF 원문과 수동 대조한다.
2. 오늘 출제 4문제와 2025년 문제부터 공식/전문 출처를 붙인다.
3. 검증 완료 항목만 `answerStatus: verified`로 승격한다.

끝.
""",
        encoding="utf-8",
    )


def main():
    questions = load_questions()
    today_ids = select_today_questions(questions)
    answer_bank = [answer_entry(question, today_ids) for question in questions]
    audit = build_audit(questions, answer_bank)

    write_json(ANSWER_BANK_PATH, answer_bank)
    write_json(AUDIT_JSON_PATH, audit)
    write_plan_doc()
    write_audit_doc(audit)

    print(f"questions={len(questions)}")
    print(f"answer_bank_entries={len(answer_bank)}")
    print(f"today_priority={','.join(sorted(today_ids))}")
    print(f"suspicious={len(audit['suspiciousExtractionIssues'])}")
    print(f"corrected_proposals={len(audit['correctedQuestionProposals'])}")
    print(ANSWER_BANK_PATH)
    print(AUDIT_DOC_PATH)


if __name__ == "__main__":
    main()
