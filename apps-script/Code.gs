const SHEET_NAME = 'attempts';

const HEADERS = [
  'receivedAt',
  'date',
  'quizId',
  'subject',
  'score',
  'total',
  'answered',
  'unansweredCount',
  'payloadJson',
  'resultText',
  'userAgent'
];

function setup() {
  const sheet = getSheet_();
  if (sheet.getLastRow() === 0) {
    sheet.appendRow(HEADERS);
  }
}

function doGet() {
  setup();
  return json_({ ok: true, service: 'so0258house-sync' });
}

function doPost(e) {
  setup();
  const payload = parsePayload_(e);
  const result = parseResultText_(payload.resultText || '');
  getSheet_().appendRow([
    new Date().toISOString(),
    result.date || payload.date || '',
    result.quizId || payload.quizId || '',
    result.subject || payload.subject || '',
    result.score || '',
    result.total || '',
    result.answered || '',
    result.unansweredCount || '',
    JSON.stringify(payload),
    payload.resultText || '',
    payload.userAgent || ''
  ]);
  return json_({ ok: true });
}

function getSheet_() {
  const spreadsheet = SpreadsheetApp.getActiveSpreadsheet();
  return spreadsheet.getSheetByName(SHEET_NAME) || spreadsheet.insertSheet(SHEET_NAME);
}

function parsePayload_(e) {
  if (!e || !e.postData || !e.postData.contents) {
    return {};
  }
  try {
    return JSON.parse(e.postData.contents);
  } catch (error) {
    return { resultText: e.postData.contents };
  }
}

function parseResultText_(text) {
  const result = {};
  String(text || '').split('\\n').forEach((line) => {
    const index = line.indexOf('=');
    if (index === -1 || line.startsWith('wrong=') || line.startsWith('review=') || line.startsWith('answerLog=') || line.startsWith('unanswered=')) {
      return;
    }
    result[line.slice(0, index)] = line.slice(index + 1);
  });
  return result;
}

function json_(payload) {
  return ContentService
    .createTextOutput(JSON.stringify(payload))
    .setMimeType(ContentService.MimeType.JSON);
}
