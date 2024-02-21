<template>
  <!-- Render model cards for LLM Constellation -->
  <div v-for="model in modelData" :key="model.id" class="model-card">
    <div class="model-info-container">
      <img src="https://picsum.photos/200" alt="Model Icon" class="model-icon" />
      <div class="model-info">
        <div class="model-name">Model Name: {{ model.model_name }}</div>
        <div class="model-parameters">Parameters: {{ model.parameters }}</div>
        <div class="model-is_vision">Vision: {{ model.is_vision ? "Supported" : "Not supported" }}</div>
        <div class="model-class">Model Class: {{ model.model_class }}</div>
        <div class="model-task">Model Tasks: {{ model.model_task }}</div>
      </div>
    </div>
    <div class="add-to-workspace-button">
      <input type="button" value="Add to Workspace" @click="addToWorkspace(model.id)">
    </div>
  </div>
  <notification-modal :show="showNotification" :message="notificationMessage" :notification-type="notificationType"
    @close="hideNotification" />
</template>

<script>
import axios from 'axios';
import NotificationModal from '@/components/NotificationModal.vue';
import NotificationMixin from '@/mixins/notificationMixin.js';
import { origin } from '../services/config';

export default {
  mixins: [NotificationMixin],
  data() {
    return {
      modelData: [],
      showNotification: false,
      notificationMessage: '',
      notificationType: 'info', // Default to info type
    };
  },
  methods: {
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

        this.modelData = response.data;
      } catch (error) {
        console.error('Failed to fetch model data', error);
      }
    },
    async addToWorkspace(modelId) {
      try {
        const accessToken = localStorage.getItem('accessToken');
        if (!accessToken) {
          console.error('Access token not found. Please authenticate first.');
          return;
        }
        const apiUrl = `${origin}/models/`;
        const requestData = {
          id: modelId,
        };

        await axios.post(apiUrl, requestData, {
          headers: {
            'Authorization': `Bearer ${accessToken}`,
            'Content-Type': 'application/json',
            'accept': 'application/json',
          },
        });
        this.showNotificationModal('success', 'Model added to workspace successfully!');
      } catch (error) {
        console.error('Failed to add model to workspace', error);
        this.showNotificationModal('error', 'Failed to add model to workspace');
      }
    },
  },
  mounted() {
    this.modelData = [];
    this.fetchModelData();
  },
};
</script>

<style scoped>
.model-card {
  display: flex;
  align-items: center;
  justify-content: space-between;
  border: 1px solid #ddd;
  padding: 10px;
  margin-bottom: 10px;
  border-radius: 8px;
  transition: background-color 0.5s ease;
  /* Smooth transition */
}

.model-card:hover {
  background: linear-gradient(360deg, #90b9f6 , #92f879);
}

.model-icon {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  margin-right: 10px;
}

.model-info-container {
  display: flex;
  align-items: center;
}

.model-info {
  display: flex;
  flex-direction: column;
}

.model-parameters,
.model-is_vision,
.model-class,
.model-task,
.model-name {
  margin-bottom: 5px;
  font-weight: bold;
  background: linear-gradient(to right, #07a825, #2339df);
  color: transparent;
  -webkit-background-clip: text;
  background-clip: text;
  border-radius: 3px;
  text-align: left;
  font-family: 'Roboto', sans-serif;
}

.add-to-workspace-button input {
  background-color: #3498db;
  color: #fff;
  padding: 10px;
  cursor: pointer;
  border: none;
  border-radius: 4px;
  font-size: 14px;
  transition: background-color 0.3s;
}

.add-to-workspace-button input:hover {
  background-color: #2980b9;
}


.add-to-workspace-button input {
  position: relative;
  display: inline-block;
  width: 180px;
  height: 40px;
  text-align: center;
  color: #fff;
  font-size: 14px;
  text-transform: uppercase;
  text-decoration: none;
  font-family: sans-serif;
  box-sizing: border-box;
  background: linear-gradient(90deg, #03a9f4, #f441a5, #ffeb3b, #03a9f4);
  background-size: 400%;
  border-radius: 30px;
  z-index: 1;
}
 
.add-to-workspace-button input:hover {
  animation: animate 8s linear infinite;
}
 
@keyframes animate {
  0% {
    background-position: 0%;
  }
  100% {
    background-position: 400%;
  }
}
 
.add-to-workspace-button input:before {
  content: "";
  position: absolute;
  top: -5px;
  right: -5px;
  bottom: -5px;
  left: -5px;
  z-index: -1;
  background: linear-gradient(90deg, #03a9f4, #f441a5, #ffeb3b, #03a9f4);
  background-size: 400%;
  border-radius: 40px;
  opacity: 0;
  transition: .5s;
}
 
.add-to-workspace-button input:hover:before {
  filter: blur(20px);
  opacity: 1;
  animation: animate 8s linear infinite;
}
</style>
