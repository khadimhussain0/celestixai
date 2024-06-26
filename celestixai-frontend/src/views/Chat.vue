<template>
  <div class="chat-container">
    <div class="chat-app">
      <div class="recent-chats">
        <button @click="createNewChat" class="new-chat-btn">New Chat</button>
        <select id="chatDropdown" v-model="currentChat" @change="changeChat" @click="fetchChats" class="dropdown">
          <option v-for="chat in recentChats" :value="chat" :key="chat.chat_id">{{ chat.chat_title }}</option>
        </select>
      </div>
    </div>

    <div class="chat-window">
      <div class="chat-messages" ref="chatMessages">
        <div v-for="message in currentChat.messages" :key="message.message_id"
          :class="{ 'user-message': message.role === 'user', 'model-message': message.role === 'assistant' }">
          <img v-if="message.images && message.images[0]" class="message-image" :src="message.images[0]"
            alt="Attached Image" />
          <p v-if="message.content" class="message-text">{{ message.content }}</p>
        </div>
      </div>


      <div class="user-input">
        <div class="custom-dropdown">
          <select id="modelDropdown" v-model="selectedModel" @change="changeModel" @click="fetchModelData"
            class="dropdown">
            <option v-for="model in models" :value="model" :key="model.id">{{ model.custom_name }}</option>
          </select>
        </div>
        <label v-if="isVisionModel" for="imageUpload" class="attachment-icon">
          🖼️
        </label>
        <input id="imageUpload" v-if="isVisionModel" type="file" @change="onImageChange" accept="image/*" />

        <label class="switch">
          <input type="checkbox" v-model="buttonState" @click="toggleButton()">
          <span class="slider round"></span>
          <span class="rag-span">RAG</span>
        </label>
        <input v-model="userInput.text" @keyup.enter="sendMessage" placeholder="Type your message..." />
        <button class="send-btn" @click="sendMessage">Send</button>
      </div>
    </div>
  </div>
  <notification-modal :show="showNotification" :message="notificationMessage" :notification-type="notificationType"
    @close="hideNotification" />
  <spinner :loading="loading" />
  <RAG v-if="buttonState"/>
</template>

<script>
import axios from "axios";
import Spinner from "@/components/Spinner.vue"
import NotificationModal from '@/components/NotificationModal.vue';
import NotificationMixin from '@/mixins/notificationMixin.js';
import { origin } from "@/services/config";
import RAG from "@/components/RAG.vue";

export default {
  mixins: [NotificationMixin],
  components: {
    NotificationModal,
    Spinner, 
    RAG
  },
  data() {
    return {
      buttonState: false,
      recentChats: null,
      currentChat: {
        rag: false,
        model: "null",
        model_id: 0,
        timestamp: Date.now(),
        chat_id: 0,
        chat_title: "Select Recent Chats",
        messages: []
      },
      showNotification: false,
      notificationMessage: '',
      notificationType: 'info',
      loading: false,
      models: null,
      selectedModel: null,
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
    },
    buttonText() {
      return this.buttonState ? 'ON' : 'OFF';
    }
  },
  methods: {
    toggleButton() {
      this.buttonState = !this.buttonState;
      this.currentChat.rag=this.buttonState;
      console.log(this.buttonState)
    },
    changeModel() {
      if (this.selectedModel) {
        // console.log("Selected Model Data:", this.selectedModel);
      }
    },
    changeChat() {
      // console.log("clicked on a chat")
      // console.log(this.currentChat)
    },
    async fetchChats() {
      console.log("fetching chats...")
      try {
        const accessToken = localStorage.getItem('accessToken');
        if (!accessToken) {
          console.error('Access token not found. Please authenticate first.');
          return;
        }
        const response = await axios.get(`${origin}/chat`, {
          headers: {
            'Authorization': `Bearer ${accessToken}`,
          },
        });
        this.recentChats = response.data;
        this.$refs.chatMessages.scrollTop = this.$refs.chatMessages.scrollHeight;
        return response.data
      } catch (error) {
        this.showNotificationModal("error", "Could not load recent chats")
        console.error('Failed to fetch recent chats', error);
      }
    },
    async fetchModelData() {
      try {
        const accessToken = localStorage.getItem('accessToken');
        if (!accessToken) {
          console.error('Access token not found. Please authenticate first.');
          return;
        }
        const response = await axios.get(`${origin}/models/`, {
          headers: {
            'Authorization': `Bearer ${accessToken}`,
          },
        });

        this.models = response.data;
        return response.data
      } catch (error) {
        this.showNotificationModal("error", "Could not load models please try again")
        console.error('Failed to fetch model data', error);
      }
    },
    async sendMessage() {
      if (!this.selectedModel) {
        this.showNotificationModal('error', 'Please select a model to chat');
        return;
      }

      this.loading = true
      this.currentChat.model = this.selectedModel.custom_name;
      this.currentChat.model_id = this.selectedModel.id;
      this.currentChat.timestamp = Date.now();

      if (this.userInput.text.trim() === '' && !this.userInput.image) return;

      if (this.currentChat.chat_id === 0) {
        this.currentChat.chat_title = this.userInput.text.slice(0, 30)
      };

      // Add user message to the chat

      this.currentChat.messages.push({ message_id: Date.now(), content: this.userInput.text, images: this.userInput.image ? [this.userInput.image] : [], role: "user" });
      this.userInput.image = null;
      this.userInput.text = '';

      // Create a copy of the current chat for sending
      const chat = { ...this.currentChat };
      chat.messages = [chat.messages[chat.messages.length - 1]];

      try {
        const accessToken = localStorage.getItem('accessToken');
        if (!accessToken) {
          throw new Error('Access token not found');
        }

        const response = await axios.post(`${origin}/chat/`, chat, {
          headers: {
            'accept': 'application/json',
            'Authorization': `Bearer ${accessToken}`,
            'Content-Type': 'application/json'
          }
        });

        // Assuming the model response is within the messages content
        const modelResponse = response.data.content;
        // Add chat_id to current_chat
        this.currentChat.chat_id = response.data.chat_id
        // Add the model response to the chat messages
        this.currentChat.messages.push({ message_id: response.data.message_id, content: modelResponse, role: "assistant" });
      } catch (error) {
        console.error('Error:', error);
        this.showNotificationModal('error', 'Error generating response');
      } finally {
        this.loading = false
      }
      // Scroll to the bottom of the chat window
      this.$refs.chatMessages.scrollTop = this.$refs.chatMessages.scrollHeight;
    },
    createNewChat() {
      this.currentChat = {
        rag: this.buttonState,
        model: "null",
        model_id: 0,
        timestamp: Date.now(),
        chat_id: 0,
        chat_title: "New Chat",
        messages: []
      }
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
  mounted() {
    const accessToken = localStorage.getItem('accessToken');
    if (accessToken) {
      this.isLoggedIn = true;
    } else {
      this.isLoggedIn = false;
    }
    this.fetchChats().then(recentChats => {
      if (this.currentChat != null && recentChats.length > 0) {
        // console.log(this.currentChat)
        this.recentChats = [this.currentChat, ...this.recentChats]
        this.currentChat = recentChats[0];
      }
    });

    this.fetchModelData().then(models => {
      console.log(models)
      if (models.length > 0) {
        this.selectedModel = models[0]
      }
    });
  },
};
</script>
  

<style scoped>
.chat-app {
  position: right;
}

.recent-chats {
  margin-bottom: 20px;
  border: 0px solid #ccc;
}

.new-chat-btn {
  padding: 12px;
  margin-right: 10px;
  background: linear-gradient(90deg, #8A75D2, #BD6A97, #D2667A);
  color: #333;
  font-size: 16px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.chat-container {
  flex-grow: 1;
  padding: 20px;
}

.chat-container {
  flex-grow: 1;
  display: flex;
  flex-direction: column;
  max-width: 1000px;
  margin: auto;
  padding: 20px;
  border: 1px solid;
  border-color: linear-gradient(90deg, #8A75D2, #BD6A97, #D2667A);
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

.custom-dropdown {
  position: relative;
  display: inline-block;
  padding: 10px;
}

.dropdown {
  font-size: 16px;
  border: none;
  border-radius: 8px;
  padding: 12px;
  background: linear-gradient(90deg, #8A75D2, #BD6A97, #D2667A);
  color: #333;
  appearance: none;
  -webkit-appearance: none;
  -moz-appearance: none;
  cursor: pointer;
  width: 100px;
  outline: none;
}

.custom-dropdown:hover .dropdown-icon i {
  transform: translateY(-50%) rotate(180deg);
}

.dropdown-label {
  margin-right: 10px;
  font-size: 18px;
  color: #666;
}

.dropdown::-webkit-scrollbar {
  width: 8px;
}

.dropdown::-webkit-scrollbar-thumb {
  background-color: #888;
  border-radius: 4px;
}

.dropdown::-webkit-scrollbar-track {
  background-color: #f1f1f1;
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

.send-btn {
  padding: 8px 12px;
  font-size: 16px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  background: linear-gradient(90deg, #8A75D2, #BD6A97, #D2667A);
  color: #333;
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

.switch {
  position: relative;
  display: inline-block;
  width: 60px;
  height: 34px;
  margin-right: 50px;
}

.switch input {
  opacity: 0;
  width: 0;
  height: 0;
}

.slider {
  position: absolute;
  cursor: pointer;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  padding-left: 105px;
  background-color: #ccc;
  -webkit-transition: .4s;
  transition: .4s;
  border-radius: 34px;
}

.slider:before {
  position: absolute;
  content: "";
  height: 26px;
  width: 26px;
  left: 50px;
  bottom: 4px;
  background-color: white;
  -webkit-transition: .4s;
  transition: .4s;
  border-radius: 50%;
}

input:checked+.slider {
  background-color: #2196F3;
}

input:focus+.slider {
  box-shadow: 0 0 1px #2196F3;
}

input:checked+.slider:before {
  -webkit-transform: translateX(26px);
  -ms-transform: translateX(26px);
  transform: translateX(26px);
}

.slider.round {
  border-radius: 34px;
}

.slider.round:before {
  border-radius: 50%;
}

.rag-span {
  position: absolute;
  left: 5px;
  /* font-size: large; */
  /* font-weight: bold; */
  top: 50%;
  transform: translateY(-50%);
}
</style>
