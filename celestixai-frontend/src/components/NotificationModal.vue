<template>
  <div v-if="show" class="notification-modal">
    <div class="notification-content" :class="notificationType">
      <p>{{ message }}</p>
      <button @click="hideModal">Close</button>
    </div>
  </div>
</template>
  
<script>
export default {
  props: {
    show: {
      type: Boolean,
      required: true,
    },
    message: {
      type: String,
      required: true,
    },
    notificationType: {
      type: String,
      default: 'info',
    },
  },
  methods: {
    hideModal() {
      this.$emit('close');
    },
  },
};
</script>
  
<style scoped>
.notification-modal {
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  z-index: 1000;
  background-color: rgba(0, 0, 0, 0.8);
  color: #fff;
  padding: 2px;
  border-radius: 8px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.5);
  text-align: center;
}

.notification-content {
  padding: 15px;
  border-radius: 8px;
  background: linear-gradient(90deg, #f441a5, #03a9f4);
}

.info {
  background-color: #3498db;
}

.success {
  background-color: #2ecc71;
}

.warning {
  background-color: #f39c12;
}

.error {
  background-color: #e74c3c;
}

button {
  margin-top: 10px;
  padding: 8px 16px;
  background-color: #fff;
  color: #333;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
}

button:hover {
  background-color: #eee;
}
</style>
  