<template>
  <div>
    <div class="floating-upload-button" @click="openFileUploader">
      <span>+</span>
    </div>
    <!-- Hidden file input to trigger file selection -->
    <input type="file" ref="fileInput" style="display: none" @change="handleFileUpload" />
  </div>
</template>
  
<script>
import axios from 'axios';
import { useToast } from 'vue-toastification';

export default {
  data() {
    return {
      modelData: [],
    };
  },
  methods: {
    openFileUploader() {
      this.$refs.fileInput.click();
    },
    handleFileUpload(event) {
      const file = event.target.files[0];
      this.sendFileToApi(file);
    },
    sendFileToApi(file) {
      const accessToken = localStorage.getItem('accessToken');
      const apiUrl = 'http://127.0.0.1:8000/dataset/';

      const formData = new FormData();

      formData.append('dataset', file, 'file.jpg');

      axios.post(apiUrl, formData, {
        headers: {
          'Authorization': `Bearer ${accessToken}`,
          'Content-Type': 'multipart/form-data',
          'accept': 'application/json',
        },
      })
        .then(response => response.json())
        .then(data => {
          this.showToast('Dataset uploaded successfully!', 'success');
          console.log('File uploaded successfully:', data);
        })
        .catch(error => {
          this.showToast('Failed to upload dataset. Please try again.', 'error');
          console.error('Error uploading file:', error);
        });
    },
    showToast(message, type) {
      const toast = useToast();
      toast[type](message, {
        position: 'top-right',
        timeout: 3000,
        closeOnClick: true,
        pauseOnHover: true,
      });
    },
  },
  mounted() {
    const accessToken = localStorage.getItem('accessToken');
    if (accessToken) {
      this.isLoggedIn = true;
    }
  },

};
</script>
  
<style scoped>
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
  