from flask import Flask, render_template, request, jsonify
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process_speech', methods=['POST'])
def process_speech():
    data = request.json
    input_text = data.get('inputText', '')
    spoken_text = data.get('spokenText', '')
    # Add your speech comparison logic here
    return jsonify({
        'score': 90,  # Placeholder
        'accuracy': 'Good',
        'completeness': 'Complete',
        'pronunciation': 'Clear'
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))  # Use PORT env or 5000
    app.run(host='0.0.0.0', port=port)
