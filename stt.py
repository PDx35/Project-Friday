import whisper
import warnings

warnings.filterwarnings("ignore", category=UserWarning)
warnings.filterwarnings("ignore", category=FutureWarning)

def speechtotext():
    model = whisper.load_model("base")
    result = model.transcribe("static/input.mp3")

    with open("static/transcription", "w") as file:
        file.write(result["text"])
        print("User:" + result["text"])
        print("Speech to text successful")
        
    with open("static/context", "a") as file:
        file.write(result["text"])
        
    return result["text"]

# speechtotext()