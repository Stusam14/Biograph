<template>
    <div class="chat-container">
      <div class="chat-box">
        <!-- Loop through messages and align based on sender -->
        <div
          v-for="(message, index) in messages"
          :key="index"
          :class="['message', message.sender]"
        >
          <div class="message-content">{{ message.text }}</div>
        </div>
      </div>
      <div class="input-box">
        <input
          v-model="userInput"
          type="text"
          @keyup.enter="sendMessage"
          placeholder="Type your message..."
        />
        <button @click="sendMessage">Send</button>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        userInput: "",
        messages: [],
      };
    },
    methods: {
      async sendMessage() {
        if (this.userInput.trim() === "") return;
  
        // Add the user's message
        this.messages.push({
          sender: "user",
          text: this.userInput,
        });
  
        // Clear the input box
        const userMessage = this.userInput;
        this.userInput = "";
  
        // Simulate a delay before ChatGPT's response
        setTimeout(() => {
          this.addChatGptResponse(userMessage);
        }, 1000);
      },
  
      addChatGptResponse(userMessage) {
        // Simulate a response from ChatGPT based on the userMessage
        const response = `You said: "${userMessage}". This is ChatGPT's response!`;
  
        this.messages.push({
          sender: "gpt",
          text: response,
        });
  
        // Scroll to the bottom of the chat after the new message
        this.scrollToBottom();
      },
  
      scrollToBottom() {
        const chatBox = this.$el.querySelector(".chat-box");
        chatBox.scrollTop = chatBox.scrollHeight;
      },
    },
  };
  </script>
  
  <style scoped>
  /* Ensure the container takes up the full viewport */
  html, body, #app {
    height: 100%;
    margin: 0;
    padding: 0;
  }
  
  .chat-container {
    display: flex;
    flex-direction: column;
    width: 100vw; /* Full viewport width */
    height: 100vh; /* Full viewport height */
    border: 1px solid #3E403F;
    overflow: hidden; /* Prevent overflow */
  }
  
  .chat-box {
    flex-grow: 1; /* Takes up all available vertical space */
    padding: 10px;
    overflow-y: auto; /* Scrollable chat box */
    /* background-color: #f7f7f7; */
    background-color: #3E403F;

  }
  
  .message {
    max-width: 50%; /* Limit width of messages */
    padding: 10px;
    margin-bottom: 10px;
    border-radius: 10px;
    position: relative;
    word-wrap: break-word; /* Ensure long words break properly */
    white-space: pre-wrap; /* Preserve formatting like newlines */
    overflow-wrap: break-word; /* Handle long words or URLs */
  }
  
  /* Align user messages to the left */
  .message.user {
    background-color: #d1ffd1;
    align-self: flex-start;
    border-top-left-radius: 0;
  }
  
  /* Align GPT messages to the right */
  .message.gpt {
    background-color: #f0f0f0;
    align-self: flex-end;
    border-top-right-radius: 0;

    margin-left: 650px;
  }
  
  .message-content {
    font-size: 14px;
  }
  
  /* Input box is centered, but smaller and does not fill entire width */
  .input-box {
    display: flex;
    justify-content: center;
    padding: 35px;
    /* background-color: #fff;
    border-top: 1px solid #ccc; */
    background-color: #3E403F;
    border-top: 1px solid #3E403F;
  }
  
  input[type="text"] {
    width: 60%; /* Input box is centered and smaller */
    padding: 10px;
    border: 1px solid #ccc;
    border-radius: 5px;
  }
  
  button {
    margin-left: 10px;
    padding: 10px;
    background-color: #007bff;
    color: #fff;
    border: none;
    border-radius: 5px;
    cursor: pointer;
  }
  
  button:hover {
    background-color: #0056b3;
  }
  </style>