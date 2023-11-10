const chatMessages = document.getElementById('chat-messages');
const userInput = document.getElementById('user-input');
const sendButton = document.getElementById('send-button');

function appendUserMessage(message) {
    const userMessageDiv = document.createElement('div');
    userMessageDiv.className = 'user-message';
    userMessageDiv.textContent = message;
    chatMessages.appendChild(userMessageDiv);
}

function appendBotMessage(message) {
    const botMessageDiv = document.createElement('div');
    botMessageDiv.className = 'bot-message';
    botMessageDiv.textContent = message;
    chatMessages.appendChild(botMessageDiv);
}

function sendMessage() {
    const userMessage = userInput.value;
    if (userMessage.trim() !== '') {
        if (userMessage.trim().toLowerCase() == 'clear') {
            clearChat();
        }
        else{
            setTimeout(() => {
                appendUserMessage(userMessage);
            }, 300);
            setTimeout(() => {
                simulateBotTyping();
            }, 1300);
        }
        }
        userInput.value = '';
}

function simulateBotTyping(selectedLanguage, selectedLanguageStyle) {
    // Add "typing" indicator message to chat messages
    const typingIndicator = 'typing...';
    const typingIndicatorDiv = document.createElement('div');
    const chatHeader = document.querySelector('.chat-header');
    const typingDuration = 1500;
    let botResponse = "";

    typingIndicatorDiv.className = 'bot-message typing-indicator';
    typingIndicatorDiv.textContent = typingIndicator;
    chatMessages.appendChild(typingIndicatorDiv);

    // Add typing class to trigger animation
    chatMessages.classList.add('typing');

    setTimeout(() => {
        // Remove typing class and typing indicator message to stop animation
        chatMessages.classList.remove('typing');
        typingIndicatorDiv.remove();

        if (chatHeader.textContent.trim() === 'choose the language you want to learn') {
            botResponse = 'Please select a language and style you want to learn';
        } else {
            botResponse = 'Hello, I am X and I will help you learn ' + selectedLanguageStyle + ' ' + selectedLanguage + '!';
        }

        appendBotMessage(botResponse);

        // Scroll chat messages container to the bottom to show the new message
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }, typingDuration);
}


// Clear all chat messages
function clearChat() {
    chatMessages.innerHTML = '';
}

// Event listeners for sending messages
sendButton.addEventListener('click', sendMessage);

userInput.addEventListener('keydown', function(event) {
    if (event.key === 'Enter') {
        sendMessage();
    }
});

//Get Input from Buttons (Language, Style and Difficulty) to use in Chat Window
document.addEventListener("DOMContentLoaded", function() {
    const languageBubbles = document.querySelectorAll('.language-bubble');
    const languageStyleButtons = document.querySelectorAll('.language-style-btn');
    const languageDiffButtons = document.querySelectorAll('.language-diff-btn');
    const chatHeader = document.querySelector('.chat-header');

    let selectedLanguage = '';
    let selectedLanguageStyle = '';
    let selectedLanguageDiff = '';

    languageBubbles.forEach(bubble => {
        bubble.addEventListener('click', function() {
            // Get the selected language from the clicked bubble
            selectedLanguage = bubble.dataset.language;

            // Remove 'selected' class from all language bubbles and style/diff buttons & Add 'selected' class to the clicked bubble
            languageBubbles.forEach(b => b.classList.remove('selected'));
            languageStyleButtons.forEach(btn => btn.classList.remove('selected'));
            languageDiffButtons.forEach(btn => btn.classList.remove('selected'));
            bubble.classList.add('selected');

            // Update chat header with selected language
            chatHeader.textContent = 'Please select a language style and difficulty level for the ' + selectedLanguage + ' Bot';

            clearChat();
        });
    });

    languageDiffButtons.forEach(button => {
        button.addEventListener('click', function() {
            languageDiffButtons.forEach(btn => btn.classList.remove('selected'));
            selectedLanguageDiff = button.getAttribute('lang-diff');
            button.classList.add('selected');

            updateChatHeader();
        });
    });

    languageStyleButtons.forEach(button => {
        button.addEventListener('click', function() {
            languageStyleButtons.forEach(btn => btn.classList.remove('selected'));
            selectedLanguageStyle = button.getAttribute('lang-style');
            button.classList.add('selected');

            updateChatHeader();
        });
    });

    function updateChatHeader() {
        if (selectedLanguageStyle && selectedLanguageDiff) {
            chatHeader.textContent = selectedLanguageDiff + ' ' + selectedLanguageStyle + ' ' + selectedLanguage + ' Bot';
            simulateBotTyping(selectedLanguage, selectedLanguageStyle);
        }
    }

});




//https://medium.com/swlh/how-to-create-your-first-login-page-with-html-css-and-javascript-602dd71144f1 
const loginForm = document.getElementById("login-form");
const loginButton = document.getElementById("login-form-submit");
const loginErrorMsg = document.getElementById("login-error-msg");

loginButton.addEventListener("click", (e) => {
    e.preventDefault();
    const username = loginForm.username.value;
    const password = loginForm.password.value;

    if (username === "user" && password === "a") {
        alert("You have successfully logged in.");
        window.location.href = "main.html"
    } else {
        loginErrorMsg.style.opacity = 1;
    }
})
