import requests
import json

# URL for the Ollama server
url = "http://192.168.0.101:10000/api/generate"

def runlocallm():
    # Read the input from the text file
    with open('static/transcription', 'r') as file:
        transcription = file.read()

    with open('static/context', 'r') as file:
        context = file.read()

    print("User:" + transcription)

    base_instruction = "keep the response under 20 words"
    # Input data (e.g., a text prompt)
    data = {
        "model": "llama3.2-vision:latest",
        "prompt": context + "\n" + transcription + "\n" + base_instruction,
    }

    # Make a POST request to the server
    response = requests.post(url, json=data)

    # Check if the request was successful
    if response.status_code == 200:
        # Process the response
        response_text = response.text

        # Convert each line to json
        response_lines = response_text.splitlines()
        response_json = [json.loads(line) for line in response_lines]
        with open('static/generation', 'w') as file:
            for line in response_json:
                file.write(line["response"])

        with open('static/context', 'a') as file:
            for line in response_json:
                file.write(line["response"])

        print("LLM Processing successful")
            
    elif response.status_code == 404:
        print(response.text)
    else:
        print("Error:", response.status_code)
    return()


#runllm()