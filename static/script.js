// Variables to handle media recording
let mediaRecorder;
let audioChunks = [];
const recordButton = document.getElementById('recordButton');
let isRecording = false;

// Function to set up the media recorder
async function setupRecorder() {
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    mediaRecorder = new MediaRecorder(stream);

    // Event listener for when data is available
    mediaRecorder.ondataavailable = (event) => {
        audioChunks.push(event.data);
    };

    // Event listener for when recording stops
    mediaRecorder.onstop = async () => {
        const audioBlob = new Blob(audioChunks, { type: 'audio/wav' });
        const formData = new FormData();
        formData.append('audio', audioBlob);
    
        // Send the recorded audio to the server
        const response = await fetch('/record-audio', {
            method: 'POST',
            body: formData
        });
        const data = await response.json();
        audioChunks = [];
    
        // Append the transcription to the message box
        const messageBox = document.getElementById('message-box');
        const userMessage = document.createElement('div');
        userMessage.classList.add('message', 'user-message');
        userMessage.innerHTML = `<span class="user">USER:</span> <span class="text">${data.transcription}</span>`;
        messageBox.appendChild(userMessage);
    
        // Process the transcription to get the assistant's response
        const transcriptionFormData = new URLSearchParams();
        transcriptionFormData.append('transcription', data.transcription);
    
        const response2 = await fetch('/process-transcription', {
            method: 'POST',
            body: transcriptionFormData
        });
        const data2 = await response2.json();
    
        // Append the assistant's response to the message box
        const assistantMessage = document.createElement('div');
        assistantMessage.classList.add('message', 'assistant-message');
        assistantMessage.innerHTML = `<span class="assistant">FRIDAY:</span> <span class="text">${data2.assistant_response}</span>`;
        messageBox.appendChild(assistantMessage);
    };
}

// Event listener for the record button
recordButton.addEventListener('click', async () => {
    if (!mediaRecorder) {
        await setupRecorder();
    }

    if (!isRecording) {
        mediaRecorder.start();
        recordButton.classList.add('recording');
    } else {
        mediaRecorder.stop();
        recordButton.classList.remove('recording');
    }
    isRecording = !isRecording;
});

// Function to send a message
function sendMessage(event) {
    event.preventDefault();
    const message = document.getElementById('user-input').value;
    const messageBox = document.getElementById('message-box');

    // Display user's message
    const userMessage = document.createElement('div');
    userMessage.classList.add('message', 'user-message');
    userMessage.innerHTML = `<span class="user">USER:</span> <span class="text">${message}</span>`;
    messageBox.appendChild(userMessage);

    // Send the message to the server
    fetch('/chat-input', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: new URLSearchParams({
            'message': message
        })
    })
    .then(response => response.text())
    .then(data => {
        // Display assistant's message
        const assistantMessage = document.createElement('div');
        assistantMessage.classList.add('message', 'assistant-message');
        assistantMessage.innerHTML = `<span class="assistant">FRIDAY:</span> <span class="text">${data}</span>`;
        messageBox.appendChild(assistantMessage);
    });
    // Clear the input field
    document.getElementById('user-input').value = '';
}