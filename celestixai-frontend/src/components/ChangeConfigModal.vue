<template>
  <div class="config-modal" v-if="isModalVisible">
    <div class="modal-content">
      <button class="close-button" @click="closeModal">X</button>
      <label for="newModelName" class="modal-label">New Model Name:</label>
      <input v-model="newModelName" type="text" id="newModelName" class="modal-input" />

      <button @click="changeConfig" class="modal-button">Change Config</button>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import { BACKEND_API_URL } from '../services/config';

export default {
  props: ['model'],
  data() {
    return {
      isModalVisible: true,
      newModelName: '',
    };
  },
  methods: {
    async changeConfig() {
      try {
        const accessToken = localStorage.getItem('accessToken');
        if (!accessToken) {
          console.error('Access token not found. Please authenticate first.');
          return;
        }

        const baseUrl = new URL(BACKEND_API_URL);
        const response = await axios.put(
          `${baseUrl.origin}/models/${this.model.id}`,
          { model_name: this.newModelName },
          {
            headers: {
              Authorization: `Bearer ${accessToken}`,
            },
          }
        );

        // Emit event to notify the parent component about the change
        if (response.status === 200) {
          this.$emit('config-changed', { type: 'success', message: 'Model name successfully changed.' });
        } else {
          this.$emit('config-changed', { type: 'error', message: 'Failed to change model name.' });
        }

        this.newModelName = '';
        this.closeModal();
      } catch (error) {
        console.error('Failed to change model name', error);
        this.$emit('config-changed', { type: 'error', message: 'An error occurred.' });
      }
    },
    closeModal() {
      this.isModalVisible = false;
      this.$emit('close');
    },
  },
};
</script>
<style scoped>

.config-modal {
    position: fixed;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    background: #f8f9fa;
    padding: 20px;
    border-radius: 8px;
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
  }

  .modal-content {
    text-align: center;
    position: relative;
  }

  .close-button {
    position: absolute;
    top: 10px;
    right: 10px;
    font-size: 18px;
    padding: 8px 12px;
    margin-top: 65px;
    background-color: #dc3545;
    color: #fff;
    border: none;
    border-radius: 4px;
    cursor: pointer;
  }

  .close-button:hover {
    background-color: #c82333;
  }

  .modal-label {
    display: block;
    margin-bottom: 10px;
    font-weight: bold;
    color: #495057;
  }

  .modal-input {
    width: calc(100% - 20px); /* Adjust width and subtract padding */
    padding: 8px;
    margin-bottom: 15px;
    border: 1px solid #ced4da;
    border-radius: 4px;
  }

  .modal-button {
    background-color: #007bff;
    color: #fff;
    padding: 10px 20px;
    cursor: pointer;
    border: none;
    border-radius: 4px;
    font-size: 16px;
    transition: background-color 0.3s;
  }

  .modal-button:hover {
    background-color: #0056b3;
  }
</style>
