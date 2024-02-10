<template>
  <div class="chat-wrapper">
    <div class="sidebar">
      <div>
        <p class="side-head">Chats</p>
      </div>
      <div @click="createNewChatPrompt" class="clickable">
        <p class="new-box clickable">New Chat</p>
      </div>
      <div v-for="chat in chats" :key="chat.chat_id" class="chat-box" @click="handleChatClick(chat)">
        {{ chat.chat_name }}
      </div>
    </div>
    
    <div v-if="selectedChat" class="message-wrapper">
      <h2>
        Messages for {{ selectedChat.chat_name }}
      </h2>
      <input type="checkbox" id="grammarAssistant" v-model="grammarAssistant">
      <label for="grammarAssistant">Switch to Grammar Assistant</label>
      <input type="checkbox" id="informalCheckbox" v-model="informalAssistant">
      <label for="informalCheckbox">Switch to Informal</label>
      <div v-for="(message, index) in splitMessages(selectedChat.messages)" :key="index" class="message-box" :class="{ 'left': index % 2 === 0, 'right': index % 2 !== 0 }">

        <div v-if="index % 2 === 0">
          <p class="left">AI</p>
          {{ message }}
        </div>
        <div v-else>
          <p class="right">User</p>
          {{ message }} 
        </div>
      </div>
    </div> 

    <!-- Text input field and button with added styling -->
    <div class="bottom-input">
      <input v-model="userInput" type="text" placeholder="Type your message..." class="message-input">
      <button @click="sendMessage" class="send-button">Send</button>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  props: ["chat"],
  data() {
    return {
      chats: [],
      selectedChat: null,
      userInput: '',
    };
  },
  created() {
    console.log('UserChats component created. User ID:', this.$route.params.id);
    this.fetchChats();
  },
  methods: {
    async fetchChats() {
      try {
        console.log(`${this.$route.params.id}`);
        const response = await axios.get(`http://localhost:5000/user_chats/${this.$route.params.id}`);
        this.chats = response.data;
      } catch (error) {
        console.error('Error fetching chats:', error);
      }
    },
    handleChatClick(chat) {
      console.log(`Clicked on chat: ${chat.chat_name}`);
      this.selectedChat = chat;
    },
    splitMessages(messages) {
      return messages.split('\\n');
    },
    async createNewChatPrompt() {
      const newChatName = prompt('Enter the name for the new chat:');
      if (newChatName !== null && newChatName !== '') {
        await this.createNewChat(newChatName);
      }
    },
    async createNewChat(chatName) {
      try {
        await axios.post(`http://localhost:5000/add_chat`, {
          user_id: this.$route.params.id,
          chat_name: chatName,
          messages: '',
        });

        this.fetchChats();
      } catch (error) {
        console.error('Error creating new chat:', error);
      }
    },
    async sendMessage() {
      const message = this.userInput.trim();
      if (message !== '') {
        console.log('Sending message:', message);

        try {
          // Determine the parameter based on the checkbox state
          const parameterName = this.grammarAssistant ? 'grammar' : 'conversation';
          const chatType = this.informalAssistant ? 'informal' : 'formal';

          // Call the backend endpoint to process and update messages
          const response = await axios.post(`http://localhost:5000/process_message/${this.selectedChat.chat_id}`, {
            message: message,
            [parameterName]: true, // Add the parameter dynamically
            [chatType]: true, // Add the informal/formal parameter dynamically
          });

          // Check for success and update the frontend
          if (response.data.success) {
            const processedMessage = response.data.message;

            // Fetch the updated list of chats
            await this.fetchChats();

            // Display the processed message
            this.selectedChat.messages += "\\n" + message + "\\n" + processedMessage;
          } else {
            console.error('Error processing message:', response.data.error);
          }

          this.userInput = ''; // Clear the input field after sending
        } catch (error) {
          console.error('Error sending message:', error);
        }
      }
    },

    async updateChatMessages(chatId, newMessage) {
      try {
        // Make a request to the backend to update the chat messages
        await axios.post(`http://localhost:5000/add_message/${chatId}`, {
          message: newMessage,
        });
      } catch (error) {
        console.error('Error updating chat messages:', error);
      }
    },
  },
};
</script>

<style>
body {
  background-color: #f1f1f1; /* Set your default background color */
  margin: 0; /* Remove default body margin */
  font-family: 'Arial', sans-serif;
}

.bottom-input {
  display: flex;
  align-items: center;
  margin-top: 20px;
  margin-left: 220px;
  margin-right: 450px;
}

.message-input {
  flex: 1;
  padding: 8px;
  margin-right: 10px;
}

.send-button {
  padding: 8px 16px;
  background-color: #4caf50;
  color: #fff;
  border: none;
  cursor: pointer;
}

.chat-box {
  display: block;
  margin: 10px 0;
  padding: 10px;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  background-color: #6b6464;
  text-align: center;
  text-decoration: none;
  color: #f3f1f1;
  cursor: pointer;
  transition: background-color 0.3s;
}

.chat-box:hover {
  background-color: #f0f0f0;
  color: #6b6464
}

.new-box {
  display: block;
  margin: 10px 0;
  padding: 10px;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  background-color: #050404;
  text-align: center;
  text-decoration: none;
  color: #ffffff;
  cursor: pointer;
  transition: background-color 0.3s;
  margin-bottom: 30px;
}

.new-box:hover {
  background-color: #f0f0f0;
  color: #6b6464
}

.sidebar {
  position: fixed;
  top: 0;
  left: 0;
  height: 100%;
  width: 200px;
  background-color: #242020;
  overflow: auto;
  z-index: 1; /* Set z-index for the chat names list */
}

.message-wrapper {
  margin-left: 220px; /* Adjust as needed to avoid overlap with the sidebar */
}

h2 {
  color: #242020;
}

.message-box {
  padding: 10px;
  margin: 5px 0;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  background-color: #ffffff;
  color: #333;
}

.left {
  text-align: left;
  background-color: #c7f0ce;
}

.right {
  text-align: right;
  background-color: #ccd2eb;
}

.side-head {
  color: #ffffff;
}

.who {
  background-color: #ffffff;
}
</style>