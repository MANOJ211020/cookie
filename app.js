const chatContainer = document.getElementById('chat-container');
const userInput = document.getElementById('user-input');
const sendBtn = document.getElementById('send-btn');
const loadingIndicator = document.getElementById('loading-indicator');

const API_URL = 'https://obscure-tribble-46j56qwwj7qf99-5000.app.github.dev/generate';

// Function to create and append a message bubble
function appendMessage(content, isUser) {
    const messageWrapper = document.createElement('div');
    messageWrapper.className = `flex ${isUser ? 'justify-end' : 'justify-start'}`;

    const messageBubble = document.createElement('div');
    messageBubble.className = `max-w-xl p-4 rounded-lg shadow-md ${
        isUser ? 'bg-blue-500 text-white' : 'bg-gray-200 text-gray-800'
    }`;

    // Render Markdown for AI responses
    if (!isUser) {
        messageBubble.innerHTML = marked.parse(content);
    } else {
        messageBubble.textContent = content;
    }

    messageWrapper.appendChild(messageBubble);
    chatContainer.appendChild(messageWrapper);

    // Scroll to the latest message
    chatContainer.scrollTop = chatContainer.scrollHeight;
}

// Function to show the loading spinner
function showLoading() {
    loadingIndicator.classList.remove('hidden');
}

// Function to hide the loading spinner
function hideLoading() {
    loadingIndicator.classList.add('hidden');
}

// Function to send a message to the bot
async function sendMessageToBot() {
    const inputText = userInput.value.trim();
    if (!inputText) return;

    // Append user message
    appendMessage(inputText, true);

    // Clear input field
    userInput.value = '';

    // Show loading indicator
    showLoading();

    try {
        // Send POST request to backend
        const response = await fetch(API_URL, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ user_input: inputText }),
        });

        if (!response.ok) {
            throw new Error('Failed to fetch response from server');
        }

        const data = await response.json();

        // Append AI response
        appendMessage(data.response, false);
    } catch (error) {
        console.error('Error:', error);
        appendMessage('Sorry, something went wrong. Please try again later.', false);
    } finally {
        // Hide loading indicator
        hideLoading();
    }
}

// Attach event listener to send button
sendBtn.addEventListener('click', sendMessageToBot);

// Allow sending message by pressing Enter
userInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        sendMessageToBot();
    }
});
