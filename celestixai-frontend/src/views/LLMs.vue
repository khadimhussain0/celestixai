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
    <div class="button-container">
      <div class="finetune-btn" :class="{ 'finetune-in-progress': isFineTuning && model.id === fineTuningModelId }">
        <input type="button" value="Fine Tune" @click="startFineTuning(model)">
        <div class="progress-bar" v-if="isFineTuning && model.id === fineTuningModelId">
          <div class="progress" :style="{ width: fineTuneProgress + '%' }"></div>
        </div>
      </div>
      <div class="config-btn">
        <input type="button" value="Config" @click="openConfigModal(model)">
      </div>
      <div class="config-btn">
        <input type="button" value="Deploy">
      </div>
    </div>
    <!-- Include the ChangeConfigModel component -->
    <change-config-model v-if="showConfigModal" :model="selectedModel" @config-changed="handleConfigChanged"
     @close="closeConfigModal"/>
    <!-- Use NotificationModal component -->
    <notification-modal :show="showNotification" :message="notificationMessage" :notification-type="notificationType"
      @close="hideNotification" />
  </div>
</template>

<script>
import axios from 'axios';
import { origin } from '../services/config';
import ChangeConfigModel from '@/components/ChangeConfigModal.vue';
import NotificationModal from '@/components/NotificationModal.vue';
import NotificationMixin from '@/mixins/notificationMixin.js';

export default {
  mixins: [NotificationMixin],
  data() {
    return {
      showNotification: false,
      notificationMessage: '',
      notificationType: 'info',
      modelData: [],
      showConfigModal: false,
      selectedModel: null,
      showNotification: false,
      notificationMessage: '',
      notificationType: 'info',
      isFineTuning: false,
      fineTuningModelId: null,
      fineTuneProgress: 0,
      fineTuneInterval: null,
    };
  },
  components: {
    ChangeConfigModel,
    NotificationModal
  },
  methods: {
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

        this.modelData = response.data;
      } catch (error) {
        console.error('Failed to fetch model data', error);
      }
    },
    openConfigModal(model) {
      this.selectedModel = model;
      this.showConfigModal = true;
    },
    closeConfigModal() {
      this.showConfigModal = false;
    },
    handleConfigChanged({ type, message }) {
      this.showNotificationModal(type, message);
      this.showConfigModal = false;
      this.fetchModelData();
    },
    startFineTuning(model) {
      // Start fine tuning process for the selected model
      if (this.isFineTuning){
        this.showNotificationModal("info", "Can't Start a new fine tuning job\n One Job is already in progress");
        return
      }
      this.isFineTuning = true;
      this.fineTuningModelId = model.id;
      this.fineTuneProgress = 0;
      this.fineTuneInterval = setInterval(() => {
        this.fineTuneProgress += 1;
        if (this.fineTuneProgress >= 100) {
          clearInterval(this.fineTuneInterval);
          this.isFineTuning = false;
          this.fineTuningModelId = null;
          this.showNotificationModal('success', 'Fine tuning completed successfully.');
        }
      }, 100);
    },
  },
  mounted() {
    this.modelData = [];
    this.fetchModelData();
  }
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

.button-container input:hover {
  background-color: #2980b9;
}


.button-container input {
  position: relative;
  display: inline-block;
  cursor: pointer;
  width: 100px;
  height: 35px;
  text-align: center;
  color: #fff;
  font-size: 14px;
  text-transform: uppercase;
  text-decoration: none;
  font-family: sans-serif;
  box-sizing: border-box;
  margin: 3px;
  background: linear-gradient(90deg, #03a9f4, #f441a5, #ffeb3b, #03a9f4);
  transition: background-color 0.3s;
  background-size: 400%;
  border: none;
  border-radius: 30px;
  z-index: 1;
}
 
.button-container input:hover {
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
 
.finetune-btn input:before {
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
 
.finetune-btn input:hover:before {
  filter: blur(20px);
  opacity: 1;
  animation: animate 8s linear infinite;
}

.progress-bar {
  width: 100%;
  height: 10px;
  background-color: #f0f0f0;
  border-radius: 5px;
  margin-top: 5px;
  overflow: hidden;
}

.progress {
  height: 100%;
  background-color: #07a8f4;
  transition: width 0.2s ease;
}

.finetune-in-progress input {
  cursor: not-allowed;
}

.finetune-in-progress input:hover {
  background-color: #bbb;
}
</style>
