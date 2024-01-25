<template>
  <div>
    <div class="floating-upload-button" @click="openFileUploader">
      <span>+</span>
    </div>
    <!-- Hidden file input to trigger file selection -->
    <input type="file" ref="fileInput" style="display: none" @change="handleFileUpload" />

    <!-- Use NotificationModal component -->
    <notification-modal
      :show="showNotification"
      :message="notificationMessage"
      :notification-type="notificationType"
      @close="hideNotification"
    />
  </div>
</template>

<script>
import axios from 'axios';
import NotificationModal from '@/components/NotificationModal.vue';

export default {
  data() {
    return {
      modelData: [],
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
        .then(response => {
          console.log('File uploaded successfully:', response.data);
          this.showNotificationModal('success', 'File uploaded successfully');
        })
        .catch(error => {
          console.error('Error uploading file:', error);
          this.showNotificationModal('error', 'Error uploading file');
        });
    },
    showNotificationModal(type, message) {
      this.notificationType = type;
      this.notificationMessage = message;
      this.showNotification = true;

      // Automatically hide the notification after a delay (e.g., 3000 milliseconds)
      setTimeout(() => {
        this.hideNotification();
      }, 3000);
    },
    hideNotification() {
      this.showNotification = false;
      this.notificationMessage = '';
      this.notificationType = 'info'; // Reset to default type
    },
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
