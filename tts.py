from openai import OpenAI
from playsound import playsound
import os

client = OpenAI(
            base_url="http://localhost:8880/v1",
            api_key="not-needed")

#Read text from transcription file


def clear_transcription():
    #Remove transcription file if exists
    if os.path.exists('generation'):
        open('generation', 'w').close()
        print("Transcription file cleared")

def textToSpeech(async_play=False):
    # Ensure the 'static' directory exists
    if not os.path.exists('static'):
        os.makedirs('static')

    with open('static/generation', 'r', encoding='utf-8') as f:
        generation = f.read()
    
    output_file = 'static/output.mp3'
    
    # Check if the file already exists and remove it
    if os.path.exists(output_file):
        try:
            os.remove(output_file)
        except PermissionError as e:
            print(f"PermissionError: Unable to remove existing file {output_file}: {e}")
            return
        except Exception as e:
            print(f"An error occurred while removing existing file {output_file}: {e}")
            return

    try:
        with client.audio.speech.with_streaming_response.create(
            model="kokoro", 
            voice="af_sky+af_bella", #single or multiple voicepack combo
            input=generation,
            response_format="mp3"
        ) as response:
            response.stream_to_file(output_file)
            print("Audio Output ready...")
            if async_play:
                import threading
                threading.Thread(target=playsound, args=(output_file,)).start()
            else:
                playsound(output_file)
    except PermissionError as e:
        print(f"PermissionError: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

    print("Text to Speech successful")
































'''
def textToSpeech():
    # Ensure the 'static' directory exists
    if not os.path.exists('static'):
        os.makedirs('static')

    with open('static/generation', 'r', encoding='utf-8') as f:
        generation = f.read()
    
    output_file = 'static/output.mp3'
    
    # Check if the file already exists and remove it
    if os.path.exists(output_file):
        try:
            os.remove(output_file)
        except PermissionError as e:
            print(f"PermissionError: Unable to remove existing file {output_file}: {e}")
            return
        except Exception as e:
            print(f"An error occurred while removing existing file {output_file}: {e}")
            return

    try:
        with client.audio.speech.with_streaming_response.create(
            model="kokoro", 
            voice="af_sky+af_bella", #single or multiple voicepack combo
            input=generation,
            response_format="mp3"
        ) as response:
            response.stream_to_file(output_file)
            print("Audio Output playing...")
            playsound(output_file)
    except PermissionError as e:
        print(f"PermissionError: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

    print("Text to Speech successful")
'''