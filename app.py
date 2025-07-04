from flask import Flask, request, jsonify, render_template
import difflib
import unicodedata
import os

app = Flask(__name__)

def compare_sentences(expected, actual):
    expected = unicodedata.normalize('NFKC', expected.lower().strip())
    actual = unicodedata.normalize('NFKC', actual.lower().strip())
    matcher = difflib.SequenceMatcher(None, expected, actual)
    accuracy_score = matcher.ratio() * 100
    expected_len = len(expected)
    actual_len = len(actual)
    matched_chars = sum(n for i, j, n in matcher.get_matching_blocks())
    completeness_score = (matched_chars / expected_len * 100) if expected_len > 0 else 0
    length_diff = abs(expected_len - actual_len) / max(expected_len, actual_len) if max(expected_len, actual_len) > 0 else 0
    pronunciation_score = max(0, 100 - (length_diff * 50))
    final_score = (0.4 * accuracy_score) + (0.3 * completeness_score) + (0.3 * pronunciation_score)
    feedback = (
        f"Score: {round(final_score, 2)}%\n"
        f"Accuracy: {round(accuracy_score, 2)}%\n"
        f"Completeness: {round(completeness_score, 2)}%\n"
        f"Pronunciation: {round(pronunciation_score, 2)}%"
    )
    return final_score, feedback

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process_speech', methods=['POST'])
def process_speech():
    data = request.get_json()
    expected_sentence = data.get('expected_sentence', '')
    recognized_text = data.get('recognized_text', '')
    if not expected_sentence or not recognized_text:
        return jsonify({
            'error': 'Missing expected or recognized text',
            'transcription': 'Please provide both sentences.'
        }), 400
    score, feedback = compare_sentences(expected_sentence, recognized_text)
    result = {
        'transcription': f"You said: {recognized_text}",
        'result': f"{'✅ Well done!' if score >= 90 else '⚠️ Good try!'}\n{feedback}"
    }
    return jsonify(result)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
