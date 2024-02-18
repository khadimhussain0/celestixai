<template>
  <div v-for="dataset in datasetData" :key="dataset.id" class="dataset-card">
    <div class="dataset-info-container">
      <img src="https://picsum.photos/200" alt="Dataset Icon" class="dataset-icon" />
      <div class="dataset-info">
        <div class="dataset-parameter">{{ dataset.filename }}</div>
        <div class="dataset-class">{{ dataset.file_size }}</div>
        <!-- <div class="dataset-task">{{ model.model_task }}</div>
        <div class="dataset-name">{{ model.model_name }}</div> -->
      </div>
    </div>
    <div class="delete-button">
      <input type="button" value="Delete" @click="deleteDataset(dataset.id)">
    </div>
  </div>

  <div>
    <div class="floating-upload-button" @click="openFileUploader">
      <span>+</span>
    </div>
    <!-- Hidden file input to trigger file selection -->
    <input type="file" ref="fileInput" style="display: none" @change="handleFileUpload" />

    <!-- Use NotificationModal component -->
    <notification-modal :show="showNotification" :message="notificationMessage" :notification-type="notificationType"
      @close="hideNotification" />
  </div>
  <spinner :loading="loading" />
</template>

<script>
import axios from 'axios';
import NotificationModal from '@/components/NotificationModal.vue';
import NotificationMixin from '@/mixins/notificationMixin.js';
import { BACKEND_API_URL, origin } from '../services/config';
import Spinner from "@/components/Spinner.vue"

export default {
  mixins: [NotificationMixin],
  components:{
    Spinner
  },
  data() {
    return {
      loading: false,
      datasetData: [],
      showNotification: false,
      notificationMessage: '',
      notificationType: 'info', // Default to info type
    };
  },
  methods: {
    openFileUploader() {
      this.$refs.fileInput.click();
    },
    handleFileUpload(event) {
      this.loading = true;
      const file = event.target.files[0];
      const accessToken = localStorage.getItem('accessToken');
      const apiUrl = `${origin}/dataset/`;

      const formData = new FormData();
      formData.append('dataset', file, file.name);

      axios.post(apiUrl, formData, {
        headers: {
          'Authorization': `Bearer ${accessToken}`,
          'Content-Type': 'multipart/form-data',
          'accept': 'application/json',
        },
      })
        .then(response => {
          console.log('File uploaded successfully:', response.data);
          this.datasetData = [...this.datasetData, response.data]
          this.showNotificationModal('success', 'File uploaded successfully');
        })
        .catch(error => {
          console.error('Error uploading file:', error);
          this.showNotificationModal('error', 'Error uploading file');
        })
        .finally(()=>{
          this.loading = false;
        });
    },
    
    async fetchDatasetData() {
      try {
        const accessToken = localStorage.getItem('accessToken');
        if (!accessToken) {
          console.error('Access token not found. Please authenticate first.');
          this.showNotificationModal("error", "Please Login Again")
          return;
        }
        const response = await axios.get(`${origin}/dataset/`, {
          headers: {
            'Authorization': `Bearer ${accessToken}`,
          },
        });

        this.datasetData = response.data;
      } catch (error) {
        this.showNotificationModal("error", "Could not load datasets")
        console.error('Failed to fetch model data', error);
      }
    },
    async deleteDataset(datasetId) {
      try {
        const accessToken = localStorage.getItem('accessToken');
        if (!accessToken) {
          console.error('Access token not found. Please authenticate first.');
          return;
        }
        const apiUrl = `${origin}/dataset/${datasetId}`;

        await axios.delete(apiUrl, {
          headers: {
            'Authorization': `Bearer ${accessToken}`,
            'Content-Type': 'application/json',
            'accept': 'application/json',
          },
        });

        this.showNotificationModal('success', 'Dataset deleted successfully!');
        this.datasetData = [];
        this.fetchDatasetData();
      } catch (error) {
        console.error('Failed to delete dataset', error);
        this.showNotificationModal('error', 'Failed to delete dataset');
      }
    }

  }
  ,
  mounted() {
    this.datasetData = [];
    this.fetchDatasetData();
  }
};
</script>

<style scoped>
.dataset-card {
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

.dataset-card:hover {
  background: linear-gradient(360deg, #90b9f6 , #92f879);
  /* Gradient background on hover */
}

.dataset-icon {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  margin-right: 10px;
}

.dataset-info-container {
  display: flex;
  align-items: center;
}

.dataset-info {
  display: flex;
  flex-direction: column;
}

.dataset-parameter,
.dataset-class,
.dataset-task,
.dataset-name {
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

.delete-button input {
  background-color: #db3434;
  color: #fff;
  padding: 10px;
  cursor: pointer;
  border: none;
  border-radius: 4px;
  font-size: 14px;
  transition: background-color 0.3s;
}

.delete-button input:hover {
  background-color: #b92929;
}

.floating-upload-button {
  position: fixed;
  bottom: 20px;
  right: 20px;
  background-color: #4CAF50;
  color: #fff;
  padding: 10px 20px;
  border-radius: 5px;
  cursor: pointer;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  transition: background-color 0.3s;
}

.floating-upload-button:hover {
  background-color: #45a049;
}
</style>
