<template>
  <div class="auth-container">
    <div class="auth-card">
      <h2 class="auth-title">{{ isRegister ? 'Sign Up' : 'Login' }}</h2>

      <!-- Navigation buttons -->
      <div class="auth-nav">
        <button @click="toggleForm" :class="{ 'active': isRegister }">Sign Up</button>
        <button @click="toggleForm" :class="{ 'active': !isRegister }">Login</button>
      </div>

      <form v-if="isRegister" @submit.prevent="registerUser">
        <div class="form-group">
          <label for="firstname">First Name</label>
          <input v-model="registerData.firstname" type="text" id="firstname" placeholder="Enter your first name" required>
        </div>
        <div class="form-group">
          <label for="lastname">Last Name</label>
          <input v-model="registerData.lastname" type="text" id="lastname" placeholder="Enter your last name" required>
        </div>
        <div class="form-group">
          <label for="email">Email</label>
          <input v-model="registerData.email" type="email" id="email" placeholder="Enter your email" required>
        </div>
        <div class="form-group">
          <label for="password">Password</label>
          <input v-model="registerData.password" type="password" id="password" placeholder="Enter your password" required>
        </div>
        <button type="submit" class="auth-btn">Sign Up</button>
      </form>

      <form v-if="!isRegister" @submit.prevent="loginUser">
        <div class="form-group">
          <label for="loginEmail">Email</label>
          <input v-model="loginData.email" type="email" id="loginEmail" placeholder="Enter your email" required>
        </div>
        <div class="form-group">
          <label for="loginPassword">Password</label>
          <input v-model="loginData.password" type="password" id="loginPassword" placeholder="Enter your password"
            required>
        </div>
        <button type="submit" class="auth-btn">Login</button>
      </form>
    </div>
  </div>
  <!-- Use NotificationModal component -->
  <notification-modal :show="showNotification" :message="notificationMessage" :notification-type="notificationType"
    @close="hideNotification" />
</template>

<script>
import axios from 'axios';
import NotificationModal from '@/components/NotificationModal.vue';
import NotificationMixin from '@/mixins/notificationMixin.js';
import { BACKEND_API_URL } from '../services/config';

export default {
  mixins: [NotificationMixin],
  data() {
    return {
      showNotification: false,
      notificationMessage: '',
      notificationType: 'info', // Default to info type
      isRegister: false,
      registerData: {
        firstname: '',
        lastname: '',
        email: '',
        password: '',
      },
      loginData: {
        email: '',
        password: '',
      },
    };
  },
  methods: {
    async registerUser() {
      try {
        const baseUrl = new URL(BACKEND_API_URL);
        const response = await axios.post(`${baseUrl.origin}/user`, this.registerData);
        console.log('User Registration Response:', response.data);
        this.showNotificationModal('success', 'Wellcome Aboard!\n Please Login to continue');
        this.isRegister = false;
        this.registerData = {
          firstname: '',
          lastname: '',
          email: '',
          password: '',
        };
        // this.$router.push('/app');
      } catch (error) {
        console.error('Error creating account:', error.message);
        this.showNotificationModal('error', 'Error creating acccount');
      }
    },
    async loginUser() {
      try {
        const params = new URLSearchParams();
        params.append('username', this.loginData.email);
        params.append('password', this.loginData.password);
        const baseUrl = new URL(BACKEND_API_URL);
        const response = await axios.post(`${baseUrl.origin}/login/`, params, {
          headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
          },
        });

        const accessToken = response.data.access_token;
        localStorage.setItem('accessToken', accessToken);
        this.$router.push('/app');
      } catch (error) {
        console.error('Login failed', error);
        this.showNotificationModal('error', 'Login failed please try again');
      }
    },
    toggleForm() {
      this.isRegister = !this.isRegister;
    },
  },
};
</script>

<style scoped>
.auth-container {
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 8px;
  /* min-height: 100vh; */
  /* background-color: #f4f4f4; */

}

.auth-card {
  max-width: 400px;
  width: 100%;
  padding: 20px;
  padding-right: 50px;
  border-radius: 8px;
  box-shadow: 0 0 20px rgba(0, 0, 0, 0.1);
  background-color: #fff;
  text-align: center;

}

.auth-title {
  font-size: 24px;
  margin-bottom: 20px;
  color: #2196F3;
}

.auth-nav {
  display: flex;
  justify-content: center;
  margin-bottom: 20px;
}

.auth-nav button {
  background: none;
  border: none;
  padding: 10px 20px;
  font-size: 16px;
  color: #555;
  cursor: pointer;
  transition: color 0.3s;
}

.auth-nav button.active {
  color: #2196F3;
}

.form-group {
  margin-bottom: 20px;
}

input {
  width: 100%;
  padding: 12px;
  font-size: 14px;
  border: 1px solid #ccc;
  border-radius: 4px;
}

.auth-btn {
  padding: 14px;
  font-size: 16px;
  color: #fff;
  background-color: #2196F3;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.auth-btn:hover {
  background-color: #1769aa;
}
</style>
