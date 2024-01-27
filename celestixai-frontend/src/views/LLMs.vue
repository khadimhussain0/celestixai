<template>
  <!-- Render model cards for LLM Constellation -->
  <div v-for="model in modelData" :key="model.id" class="model-card">
    <div class="model-info-container">
      <img src="https://picsum.photos/200" alt="Model Icon" class="model-icon" />
      <div class="model-info">
        <div class="model-parameter">Model Name: {{ model.model_name }}</div>
        <div class="model-class">Parameters: {{ model.parameters }}</div>
        <div class="model-task">Model Class: {{ model.model_class }}</div>
        <div class="model-name">Model Task: {{ model.model_task }}</div>
      </div>
    </div>
    <div class="finetune-btn">
      <input type="button" value="Fine Tune">
    </div>
  </div>
</template>
  
<script>
import axios from 'axios';
import { BACKEND_API_URL } from '../services/config';

export default {
  data() {
    return {
      modelData: [],
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
        const baseUrl = new URL(BACKEND_API_URL);
        const response = await axios.get(`${baseUrl.origin}/models/`, {
          headers: {
            'Authorization': `Bearer ${accessToken}`,
          },
        });

        this.modelData = response.data;
      } catch (error) {
        console.error('Failed to fetch model data', error);
      }
    }
  },
  mounted() {
    // Calling fetchModelData function when the component is mounted
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
  /* Smooth transition */
}

.model-card:hover {
  background: linear-gradient(360deg, #90b9f6 , #92f879);
  /* Gradient background on hover */
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

.model-parameter,
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

.finetune-btn input {
  background-color: #3498db;
  color: #fff;
  padding: 10px;
  cursor: pointer;
  border: none;
  border-radius: 4px;
  font-size: 14px;
  transition: background-color 0.3s;
}

.finetune-btn input:hover {
  background-color: #2980b9;
}


.finetune-btn input {
  position: relative;
  display: inline-block;
  width: 100px;
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
 
.finetune-btn input:hover {
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
</style>
