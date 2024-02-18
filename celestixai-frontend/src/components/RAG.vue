<template>
    <div class="vector-store-modal" v-if="isModalVisible" @click="closeModal">
      <div class="modal-content" @click.stop>
        <button class="close-button" @click="closeModal">X</button>
        <h2>Select Datasets</h2>
        <div v-if="datasetData.length === 0">Loading datasets...</div>
        <ul v-else class="dataset-list">
          <li v-for="dataset in datasetData" :key="dataset.id">
            <label>
              <span class="filename">{{ truncateFilename(dataset.filename) }}</span>
              <input class="checkboxes" type="checkbox" v-model="selectedDatasets" :value="dataset.id" @click.stop>
            </label>
          </li>
        </ul>
        <button @click="buildVectorStore" class="modal-button">Build Vector Store</button>
      </div>
      <spinner :loading="loading" />
    </div>
  </template>
  
  
  <script>
import axios from 'axios';
import Spinner from "@/components/Spinner.vue"
import { BACKEND_API_URL } from '../services/config';

export default {
  data() {
    return {
      loading: false,
      isModalVisible: true,
      datasetData: [],
      selectedDatasets: []
    };
  },
  async created() {
    await this.fetchDatasetData();
  },
  methods: {
    async fetchDatasetData() {
      try {
        const accessToken = localStorage.getItem('accessToken');
        if (!accessToken) {
          console.error('Access token not found. Please authenticate first.');
          return;
        }

        const baseUrl = new URL(BACKEND_API_URL);
        const response = await axios.get(
          `${baseUrl.origin}/dataset/`,
          {
            headers: {
              Authorization: `Bearer ${accessToken}`,
            },
          }
        );

        this.datasetData = response.data;
      } catch (error) {
        console.error('Failed to fetch dataset data', error);
      }
    },
    async buildVectorStore() {
      console.log("Building Vector Store...");
      this.closeModal();
    },
    closeModal() {
      this.isModalVisible = false;
      this.$emit('close');
    },
    truncateFilename(filename) {
      if (filename.length > 30) {
        return filename.substring(0, 30) + '...';
      }
      return filename;
    },
  },
};
</script>

  
  <style scoped>
  .vector-store-modal {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(0, 0, 0, 0.5);
    display: flex;
    justify-content: center;
    align-items: center;
    overflow-y: auto;
  }
  
  .modal-content {
  background: linear-gradient(90deg, #f441a5, #03a9f4);
  border-radius: 8px;
  max-width: 80%;
  padding: 20px;
  position: relative; 
}

.close-button {
  position: absolute;
  top: 10px;
  right: 10px;
  background-color: transparent;
  border: none;
  font-size: 18px;
  cursor: pointer;
}

.modal-content h2 {
  margin-top: 0;
}

.modal-content ul {
  list-style-type: none;
  padding: 0;
  max-height: 300px;
  overflow-y: auto;
}

.modal-content li {
  margin-bottom: 10px;
}
.modal-content input[type="checkbox"] {
  appearance: none;
  position: relative;
  display: inline-block;
  width: 20px;
  height: 20px;
  background-color: #fff;
  border: 2px solid #03a9f4;
  border-radius: 4px;
  cursor: pointer;
  vertical-align: middle;
  margin-right: 10px;
}
.modal-content input[type="checkbox"]:checked::after {
  content: '\2714';
  font-size: 16px;
  color: #29c40a;
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
}
.modal-content label {
  display: flex;
  align-items: center;
}

.modal-content button {
  display: block;
  margin-top: 20px;
}

.close-button {
  position: absolute;
  top: 10px;
  right: 10px;
  /* background-color: transparent; */
  background-color: red;
  border: none;
  border-radius: 5px;
  font-size: 24px;
  cursor: pointer;
  color: #fff;
  transition: transform 0.3s ease;
}

.close-button:hover {
  transform: rotate(180deg);
}

.modal-button {
  display: inline-block;
  padding: 10px 20px;
  background-color: #4CAF50; 
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.modal-button:hover {
  background-color: #45a049;
}

  </style>
  