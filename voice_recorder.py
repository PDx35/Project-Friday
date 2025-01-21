from flask import request

def record_audio():
    audio_data = request.files['audio']
    audio_data.save('static/input.mp3')
    return 'Audio saved'