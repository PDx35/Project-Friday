from stt import speechtotext
from tts import textToSpeech
from llm import runlocallm
from flask import Flask, request, render_template

app = Flask(__name__)

# Route for the home page
@app.route('/')
def index():
    return render_template('index.html')

# Route to handle audio recording
@app.route('/record-audio', methods=['POST'])
def record_audio():
    audio_data = request.files['audio']
    audio_data.save('static/input.mp3')
    transcription = speechtotext()
    
    return {
        'transcription': transcription
    }

# Route to process the transcription
@app.route('/process-transcription', methods=['POST'])
def process_transcription():
    transcription = request.form['transcription']
    with open('static/transcription', 'w') as file:
        file.write(transcription)
    runlocallm()
    with open('static/generation', 'r') as file:
        assistant_response = file.read()
    textToSpeech(async_play=True)
    
    return {
        'assistant_response': assistant_response
    }

# Route to handle chat input
@app.route('/chat-input', methods=['POST'])
def chat_input():
    user_input = request.form['message']
    print(user_input)
    with open('static/transcription', 'w') as file:
        file.write(user_input)
    runlocallm()
    with open('static/generation', 'r') as file:
        assistant_response = file.read()
    textToSpeech(async_play=True)
    return assistant_response

if __name__ == '__main__':
    app.run(host='0.0.0.0', threaded=True, debug=True)