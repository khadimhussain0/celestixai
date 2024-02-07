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
        <div v-for="message in messages" :key="message.id"
          :class="{ 'user-message': message.isUser, 'model-message': !message.isUser }">
          <img v-if="message.image" class="message-image" :src="message.image" alt="Attached Image" />
          <p v-if="message.text" class="message-text">{{ message.text }}</p>
        </div>
      </div>

      <div class="user-input">
        <label v-if="isVisionModel" for="imageUpload" class="attachment-icon">
          🖼️
          <!-- <img src="attachment_icon.png" alt="Attachment Icon" /> -->
        </label>
        <input id="imageUpload" v-if="isVisionModel" type="file" @change="onImageChange" accept="image/*" />
        <input v-model="userInput.text" @keyup.enter="sendMessage" placeholder="Type your message..." />
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
        { label: 'Model A', value: {name:'LLAMA', id:2, is_vision:true, metadata:{}} },
        { label: 'Model B', value: {name:'LLAMA2', id:2, is_vision:false, metadata:{}} },
        { label: 'Model 3', value: {name:'LLAMA3', id:2, is_vision:true, metadata:{}} },
        // Add more models as needed
      ],
      selectedModel: 'modelA',
      userInput: {
        text: '',
        image: null,
      },
      messages: [],
    };
  },
  computed: {
    isVisionModel() {
      return this.selectedModel && this.selectedModel.is_vision;
    }
  },
  methods: {
    changeModel() {
      // Logic to switch language model
      // You may want to fetch model-specific data here
    },
    sendMessage() {
      if (this.userInput.text.trim() === '' && !this.userInput.image) return;

      // Add user message to the chat
      this.messages.push({ id: Date.now(), text: this.userInput.text, image: this.userInput.image, isUser: true });

      // Simulate model response (replace this with actual LLM interaction)
      const modelResponse = 'This is a model response.';
      this.messages.push({ id: Date.now() + 1, text: modelResponse, isUser: false });

      // Clear user input
      this.userInput.text = '';
      this.userInput.image = null;

      // Scroll to the bottom of the chat window
      this.$refs.chatMessages.scrollTop = this.$refs.chatMessages.scrollHeight;
    },
    onImageChange(event) {
      const file = event.target.files[0];
      if (file) {
        const reader = new FileReader();
        reader.onload = () => {
          this.userInput.image = reader.result;
        };
        reader.readAsDataURL(file);
      }
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
  padding: 5px;
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
  margin-bottom: 5px;
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

.attachment-icon {
  cursor: pointer;
}

.attachment-icon img {
  width: 24px;
  height: 24px;
}

#imageUpload {
  display: none;
}

.message-image {
  max-width: 100%;
  border-radius: 20px;
}

.message-text {
  margin-top: 5px;
}
</style>
