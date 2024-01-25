<template>
    <div class="chat-container">
      <div class="model-selection">
        <label for="modelDropdown">Select Model:</label>
        <select id="modelDropdown" v-model="selectedModel" @change="changeModel">
          <option v-for="model in models" :value="model.value" :key="model.value">{{ model.label }}</option>
        </select>
      </div>
  
      <div class="chat-window">
        <div class="chat-messages" ref="chatMessages">
          <div v-for="message in messages" :key="message.id" :class="{ 'user-message': message.isUser, 'model-message': !message.isUser }">
            {{ message.text }}
          </div>
        </div>
  
        <div class="user-input">
          <input v-model="userInput" @keyup.enter="sendMessage" placeholder="Type your message..." />
          <button @click="sendMessage">Send</button>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        models: [
          { label: 'Model A', value: 'modelA' },
          { label: 'Model B', value: 'modelB' },
          // Add more models as needed
        ],
        selectedModel: 'modelA',
        userInput: '',
        messages: [],
      };
    },
    methods: {
      changeModel() {
        // Logic to switch language model
        // You may want to fetch model-specific data here
      },
      sendMessage() {
        if (this.userInput.trim() === '') return;
  
        // Add user message to the chat
        this.messages.push({ id: Date.now(), text: this.userInput, isUser: true });
  
        // Simulate model response (replace this with actual LLM interaction)
        const modelResponse = 'This is a model response.';
        this.messages.push({ id: Date.now() + 1, text: modelResponse, isUser: false });
  
        // Clear user input
        this.userInput = '';
  
        // Scroll to the bottom of the chat window
        this.$refs.chatMessages.scrollTop = this.$refs.chatMessages.scrollHeight;
      },
    },
  };
  </script>
  
  <style scoped>
  .chat-container {
    display: flex;
    flex-direction: column;
    max-width: 600px;
    margin: auto;
    padding: 20px;
    border: 1px solid #ccc;
    border-radius: 10px;
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
  }

  .model-selection {
    margin-bottom: 15px;
  }

  label {
    font-size: 16px;
    margin-right: 10px;
    color: #333;
  }

  select {
    padding: 8px;
    font-size: 14px;
    border: 1px solid #ccc;
    border-radius: 5px;
    cursor: pointer;
  }

  .chat-window {
    flex-grow: 1;
    overflow-y: auto;
  }

  .chat-messages {
    display: flex;
    flex-direction: column;
    gap: 10px;
  }

  .user-message,
  .model-message {
    padding: 10px;
    border-radius: 8px;
    max-width: 80%;
    word-wrap: break-word;
  }

  .user-message {
    background-color: #4CAF50;
    color: white;
    align-self: flex-end;
  }

  .model-message {
    background-color: #2196F3;
    color: white;
    align-self: flex-start;
  }

  .user-input {
    display: flex;
    align-items: center;
    margin-top: 10px;
  }

  input {
    flex-grow: 1;
    padding: 8px;
    font-size: 14px;
    border: 1px solid #ccc;
    border-radius: 5px;
    margin-right: 10px;
  }

  button {
    padding: 8px 12px;
    font-size: 14px;
    border: none;
    border-radius: 5px;
    cursor: pointer;
    background-color: #2196F3;
    color: white;
  }
</style>

  