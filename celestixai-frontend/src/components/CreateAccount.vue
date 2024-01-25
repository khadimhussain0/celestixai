<template>
    <div class="register-container">
      <div class="register-card">
        <h2 class="register-title">Sign Up</h2>
        <form @submit.prevent="registerUser">
          <div class="form-group">
            <label for="firstname">First Name</label>
            <input v-model="formData.firstname" type="text" id="firstname" placeholder="Enter your first name" required>
          </div>
          <div class="form-group">
            <label for="lastname">Last Name</label>
            <input v-model="formData.lastname" type="text" id="lastname" placeholder="Enter your last name" required>
          </div>
          <div class="form-group">
            <label for="email">Email</label>
            <input v-model="formData.email" type="email" id="email" placeholder="Enter your email" required>
          </div>
          <div class="form-group">
            <label for="password">Password</label>
            <input v-model="formData.password" type="password" id="password" placeholder="Enter your password" required>
          </div>
          <button type="submit" class="register-btn">Sign Up</button>
        </form>
      </div>
    </div>
  </template>
  
  <script>
  import axios from 'axios';

  export default {
    data() {
      return {
        formData: {
          firstname: '',
          lastname: '',
          email: '',
          password: '',
        },
      };
    },
    methods: {
        async registerUser() {
      try {
        const response = await axios.post('http://127.0.0.1:8000/user', this.formData);
        console.log('User Registration Response:', response.data);
        this.$router.push('/app');
        // Display a success message or perform any other action
      } catch (error) {
        console.error('Error creating account:', error.message);
        // Display a toast or any other error handling mechanism
      }
    }
    },
  };
  </script>
  
  <style scoped>
  .register-container {
    display: flex;
    justify-content: center;
    align-items: center;
    /* height: 100vh; */
    padding: 20px;
    /* background-color: rgba(255, 255, 255, 0.8); */
  }
  
  .register-card {
  max-width: 400px;
  width: 100%;
  padding: 30px;
  padding-right: 50px;
  border: 1px solid #ccc;
  border-radius: 8px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
  background-color: rgba(255, 255, 255, 0.5); /* Adjusted alpha value for transparency */
}
  
  .register-title {
    font-size: 24px;
    text-align: center;
    margin-bottom: 20px;
    color: #2196F3;
  }
  
  .form-group {
    margin-bottom: 15px;
  }
  
  label {
    display: block;
    font-size: 14px;
    margin-bottom: 5px;
    color: #333;
  }
  
  input {
    width: 100%;
    padding: 10px;
    margin-right: 200px;
    font-size: 14px;
    border: 1px solid #ccc;
    border-radius: 4px;
    background-color: rgba(255, 255, 255, 0.5); /* Added transparent background */
  }
  
  .register-btn {
    /* width: 100%; */
    padding: 14px;
    padding-left: 20px;
    padding-right: 20px;
    font-size: 16px;
    color: #fff;
    background-color: #2196F3;
    border: none;
    border-radius: 10px;
    cursor: pointer;
  }

  .register-btn:hover{
    background-color: rgb(43, 143, 18);
  }
  </style>
  