<template>
    <!-- Render model cards for LLM Constellation -->
    <div v-for="model in modelData" :key="model.id" class="model-card">
      <div class="model-info-container">
        <img src="https://picsum.photos/200" alt="Model Icon" class="model-icon" />
        <div class="model-info">
          <div class="model-parameter">{{ model.parameters }}</div>
          <div class="model-class">{{ model.model_class }}</div>
          <div class="model-task">{{ model.model_task }}</div>
          <div class="model-name">{{ model.model_name }}</div>
        </div>
      </div>
      <div class="add-to-workspace-button">
        <input type="button" value="Add to Workspace">
      </div>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  
  export default {
    data() {
      return {
        modelData: [],
      };
    },
    methods: {
      async fetchModelData() {
        try {
          // Retrieve the token from localStorage
          const accessToken = localStorage.getItem('accessToken');
  
          // Check if the token is present before making the request
          if (!accessToken) {
            console.error('Access token not found. Please authenticate first.');
            return;
          }
  
          const response = await axios.get('http://127.0.0.1:8000/models/', {
            headers: {
              'Authorization': `Bearer ${accessToken}`,
            },
          });
  
          this.modelData = response.data;
        } catch (error) {
          console.error('Failed to fetch model data', error);
          // Handle error (show error message, etc.)
        }
      }
    },
    mounted() {
      // Call the fetchModelData function when the component is mounted
      this.modelData=[];
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
    transition: background-color 0.5s ease; /* Smooth transition */
  }

  .model-card:hover {
    background: linear-gradient(45deg, #3498db, #1abc9c); /* Gradient background on hover */
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
</style>
