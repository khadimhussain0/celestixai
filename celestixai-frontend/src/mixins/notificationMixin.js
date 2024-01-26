export default {
  methods: {
    showNotificationModal(type, message) {
      this.notificationType = type;
      this.notificationMessage = message;
      this.showNotification = true;

      setTimeout(() => {
        this.hideNotification();
      }, 1000);
    },
    hideNotification() {
      this.showNotification = false;
      this.notificationMessage = '';
      this.notificationType = 'info';
    },
  },
};
