<template>
    <div id="app" class="chatwindow">
        <div class="language-style-div">
            <h6> Language Style</h6>
            <div>
                <button class="language-style-btn" lang-style="Informal">Informal</button>  
            </div>
            <div>
                <button class="language-style-btn" lang-style="Formal">Formal</button> 
            </div>
            <div>
                <button class="language-style-btn" lang-style="Academic">Academic</button>
            </div>
        </div>

        <div class="language-difficulty-div">
            <h6> Difficulty Level</h6>
            <div>
                <button class="language-diff-btn" lang-diff="Beginner">Beginner</button>  
            </div>
            <div>
                <button class="language-diff-btn" lang-diff="Intermediate">Intermediate</button> 
            </div>
            <div>
                <button class="language-diff-btn" lang-diff="Advanced">Advanced</button>
            </div>
        </div>

        <div class="chat-container">
            <div class="chat-header">choose the language you want to learn</div>
            <div class="chat-messages" id="chat-messages"></div>
            <div class="input-container">
                <input type="text" class="chat-input" id="user-input" placeholder="Send a message...">
                <button id="send-button">Send</button>
            </div>
        </div>

        <div class="language-bubbles">
            <div class="language-bubble" data-language="English">
                <img class="language-icon" :src="require('@/assets/flag_en.jpg')" alt="English Flag">
            </div>
            <div class="language-bubble" data-language="Spanish">
                <img class="language-icon" :src="require('@/assets/flag_es.png')" alt="Spanish Flag">
            </div>
            <div class="language-bubble" data-language="French">
                <img class="language-icon" :src="require('@/assets/flag_fr.png')" alt="French Flag">
            </div>
            <div class="language-bubble" data-language="German">
                <img class="language-icon" :src="require('@/assets/flag_de.png')" alt="German Flag">
            </div>
        </div>
    </div>
</template>

<script>
export default {
    mounted() {
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
                } else {
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
                    botResponse = 'Hello, I am langchatAI and I will help you learn ' + selectedLanguageStyle + ' ' + selectedLanguage + '!';
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
    }
}
</script>

<style>
@import url('https://fonts.googleapis.com/css?family=IBM Plex Mono');

div.chatwindow {
    text-align: center;
    margin-top: 3rem;
}

/* CHAT */

/*Language Bubbles*/
.language-bubbles {
position: fixed;
top: 50%;
right: 50px;
display: flex;
flex-direction: column;
align-items: flex-end;
transform: translateY(-50%);
}

.language-bubble {
width: 60px;
height: 60px;
border-radius: 75%;
display: flex;
justify-content: center;
align-items: center;
margin-bottom: 20px;
cursor: pointer;
transition: background-color 0.3s ease;
border: 1px solid #a9a9a9;
box-shadow: 0 4px 8px #4646461a;
}

.language-icon {
width: 50px; /* Adjust the icon size */
height: 50px; /* Adjust the icon size */
border-radius: 50%; /* Ensures the icon is round */
object-fit: cover; /* Maintain aspect ratio */
border-style: hidden;
}

.language-bubble:hover {
background-color: #b8b6b6a6;
}

.language-bubble.selected {
background-color: #b8b6b6a6; 
}


/*Language Style*/
.language-style-div {
  position: fixed;
  top: 35%;
  left: 30px; 
  transform: translateY(-50%);
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  z-index: 999; 
}

.language-style-btn{
  width: 120px;
  height: 40px;
  border-radius: 10px;
  display: flex;
  justify-content: center;
  align-items: center;
  margin-bottom: 20px;
  cursor: pointer;
  transition: background-color 0.3s ease;
  background-color: #003EC6;
  color: #fff;
  border: none;
  box-shadow: 2px 2px 2px #0a3899;
  font-size: 14px;
}
button{
    font-family: 'IBM Plex Mono', monospace;
}

.language-style-btn:hover,#send-button:hover {
  background-color: #3272fc;
}

.language-style-btn.selected {
  background-color: #3272fc;
}

/*Language Difficulty*/
.language-difficulty-div {
  position: fixed;
  top: 70%;
  left: 30px; 
  transform: translateY(-50%);
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  z-index: 999; 
}
.language-diff-btn{
  width: 120px;
  height: 40px;
  border-radius: 10px;
  display: flex;
  justify-content: center;
  align-items: center;
  margin-bottom: 20px;
  cursor: pointer;
  transition: background-color 0.3s ease;
  background-color: #003EC6;
  color: #fff;
  border: none;
  box-shadow: 2px 2px 2px #0a3899;
  font-size: 14px;
}

#send-button{
  width: 80px;
  height: 30px;
  margin-left: 10px; 
  margin-right: 10px;
  cursor: pointer;
  border-radius: 10px;
  transition: background-color 0.3s ease;
  background-color: #003EC6;
  color: #fff;
  border: none;
  box-shadow: 2px 2px 2px #0a3899;
  font-size: 14px;
}

.language-diff-btn:hover,#send-button:hover {
  background-color: #3272fc;
}

.language-diff-btn.selected {
  background-color: #3272fc;
}

h4 {
  font-size: 15px;
  margin-bottom: 15px;
}


/* CHAT WINDOW */
.chat-container {
  width: 60%;
  height: 70vh; /* 70% of the viewport height */
  margin: 20px auto;
  border: 1px solid #ccc;
  border-radius: 10px;
  overflow: hidden;
  background-color: #fff;
  box-shadow: 0 20px 20px 20px #a7a7a73a;
}

.chat-messages {
  padding: 20px;
  overflow-y: auto;
  height: calc(100% - 150px);
  word-wrap: break-word;
  font-size: 14px;
}

.chat-header {
  background-color: #003EC6;
  color: #fff;
  padding: 15px;
  text-align: center;
  font-size: 15px;
}

.user-message, .bot-message {
  margin-bottom: 10px;
  display: block; 
  white-space: pre-wrap;
  clear: both;
}

.user-message {
  text-align: right;
  color: #003EC6;
  border-radius: 15px;
  padding: 10px;
  padding-right: 20px;
  background-color: #fff;
  box-shadow: 0 4px 8px #4646461a;
  border: 2px #003EC6 solid;
}

.bot-message {
  text-align: left;
  color: #0D1117;
  border: 1px solid #444;
  border-radius: 15px;
  padding: 10px;
  padding-left: 20px;
  box-shadow: 0 4px 8px #4646461a;
}

.bot-message.typing-indicator {
  background-color: transparent;
  border: none;
  box-shadow: none;
}

.chat-input {
  width: 100%;
  padding: 10px;
  border: none;
  font-size: 14px;
  resize: vertical;
  font-family: monospace;
}
.input-container {
  display: flex;
  align-items: center;
  justify-content: space-between;
  border-top: 1px solid #ccc;
  padding: 10px;
  margin-top: auto;
}

</style>