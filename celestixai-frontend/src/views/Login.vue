<!-- components/Login.vue -->
<template>
    <div class="login-container">
      <div class="login-card">
      <h1>Login</h1>
      <form @submit.prevent="login">
        <label for="username">Username:</label>
        <input type="text" v-model="username" required>
        <label for="password">Password:</label>
        <input type="password" v-model="password" required>
        <button class="login-btn" type="submit">Login</button>
      </form>
      </div>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  
  export default {
    data() {
      return {
        username: '',
        password: '',
      };
    },
    methods: {
      async login() {
        try {
          const params = new URLSearchParams();
          params.append('username', this.username);
          params.append('password', this.password);
  
          const response = await axios.post('http://127.0.0.1:8000/login/', params, {
            headers: {
              'Content-Type': 'application/x-www-form-urlencoded',
            },
          });
  
          const accessToken = response.data.access_token;
          localStorage.setItem('accessToken', accessToken);
  
          // Redirect to LLMs page after successful login
          this.$router.push('/app');
        } catch (error) {
          console.error('Login failed', error);
          // Handle login failure (show error message, reset form, etc.)
        }
      },
    },
  };
  </script>
  
  <style scoped>

.login-container {
    display: flex;
    justify-content: center;
    align-items: center;
    padding: 20px;
    /* background-color: rgba(255, 255, 255, 0.1); */
  }

  .login-card {
  max-width: 400px;
  margin: 70px;
  width: 100%;
  padding: 30px;
  padding-right: 50px;
  border: 1px solid #ccc;
  border-radius: 8px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
  background-color: rgba(255, 255, 255, 0.5); /* Adjusted alpha value for transparency */
}
.login-container h1 {
  font-size: 24px;
  text-align: center;
  margin-bottom: 20px;
  color: #2196F3;
}

.login-container form {
  display: flex;
  flex-direction: column;
}

.login-container label {
  margin-top: 10px;
}

.login-container input {
  margin-bottom: 10px;
  padding: 8px;
}

.login-btn {
  width: 100%;
  padding: 14px;
  font-size: 16px;
  color: #fff;
  background-color: #2196F3;
  border: none;
  border-radius: 10px;
  cursor: pointer;
}

.login-btn:hover {
  background-color: rgb(43, 143, 18);
}
  </style>
  