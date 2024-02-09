<template>
  <div class="chat-container">
    <div class="chat-app">
      <div class="recent-chats">
        <button @click="createNewChat" class="new-chat-btn">New Chat</button>
        <select id="chatDropdown" v-model="selectedChat" @change="changeChat" @click="fetchChats" class="dropdown">
          <option v-for="chat in recentChats" :value="chat" :key="chat.chat_id">{{ chat.chat_title }}</option>
        </select>
      </div>
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
        <div class="custom-dropdown">
          <select id="modelDropdown" v-model="selectedModel" @change="changeModel" @click="fetchModelData"
            class="dropdown">
            <option v-for="model in models" :value="model" :key="model.id">{{ model.model_name }}</option>
          </select>
        </div>
        <label v-if="isVisionModel" for="imageUpload" class="attachment-icon">
          🖼️
        </label>
        <input id="imageUpload" v-if="isVisionModel" type="file" @change="onImageChange" accept="image/*" />
        <input v-model="userInput.text" @keyup.enter="sendMessage" placeholder="Type your message..." />
        <button class="send-btn" @click="sendMessage">Send</button>
      </div>
    </div>
  </div>
  <notification-modal :show="showNotification" :message="notificationMessage" :notification-type="notificationType"
    @close="hideNotification" />
</template>

<script>
import axios from "axios";
import Spinner from "@/components/Spinner.vue"
import NotificationModal from '@/components/NotificationModal.vue';
import NotificationMixin from '@/mixins/notificationMixin.js';
import { origin } from "@/services/config";

export default {
  mixins: [NotificationMixin],
  components: {
    NotificationModal
  },
  data() {
    return {
      recentChats: [{
        model: "string",
        model_id: 0,
        timestamp: 0,
        chat_id: 0,
        chat_title: "string",
        messages: [
          {
            message_id: 0,
            role: "string",
            content: "string",
            images: []
          }
        ]
      }, {
        model: "string",
        model_id: 0,
        timestamp: 0,
        chat_id: 0,
        chat_title: "string",
        messages: [
          {
            message_id: 0,
            role: "string",
            content: "string",
            images: []
          }
        ]
      }],
      selectedChat: null,
      showNotification: false,
      notificationMessage: '',
      notificationType: 'info',
      loading: false,
      models: [
        { name: 'Model A', id: 1, is_vision: true },
        { name: 'Model B', id: 2, is_vision: false },
        { name: 'Model C', id: 3, is_vision: true },
      ],
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
    }
  },
  methods: {
    changeModel() {
      if (this.selectedModel) {
        console.log("Selected Model Data:", this.selectedModel);
      }
    },
    changeChat(){
      if (this.selectedChat){
        console.log(this.selectedChat)
      }
    },
    async fetchChats(){
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
        console.log(response.data)
        this.recentChats = response.data;
      } catch (error) {
        console.error('Failed to fetch model data', error);
      }
    },
    async fetchModelData() {
      try {
        const accessToken = localStorage.getItem('accessToken');
        if (!accessToken) {
          console.error('Access token not found. Please authenticate first.');
          return;
        }
        const response = await axios.get(`${origin}/model_constellation/`, {
          headers: {
            'Authorization': `Bearer ${accessToken}`,
          },
        });

        this.models = response.data;
      } catch (error) {
        console.error('Failed to fetch model data', error);
      }
    },
    sendMessage() {
      if (!this.selectedModel) {
        this.showNotificationModal('error', 'Please select a model to chat');
        return
      }
      if (this.userInput.text.trim() === '' && !this.userInput.image) return;
      // Add user message to the chat
      this.messages.push({ id: Date.now(), text: this.userInput.text, image: this.userInput.image, isUser: true });

      const modelResponse = 'This is a model response.';
      this.messages.push({ id: Date.now() + 1, text: modelResponse, isUser: false });
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
  background: linear-gradient(90deg, #8A75D2 , #BD6A97, #D2667A);
  color:#333;
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
  border: 1px solid ;
  border-color: linear-gradient(90deg, #8A75D2 , #BD6A97, #D2667A);
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
  background: linear-gradient(90deg, #8A75D2 , #BD6A97, #D2667A);
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
  background: linear-gradient(90deg, #8A75D2 , #BD6A97, #D2667A);
  color:#333;
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
