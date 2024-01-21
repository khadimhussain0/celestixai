<template>
    <div class="signup">
      <h2>Sign Up</h2>
      <form @submit.prevent="submitForm" class="signup-form">
        <div class="form-group">
          <label for="name">Name:</label>
          <input type="text" id="name" v-model="name" required>
        </div>
        <div class="form-group">
          <label for="email">Email:</label>
          <input type="email" id="email" v-model="email" required>
        </div>
        <div class="form-group">
          <label for="password">Password:</label>
          <input type="password" id="password" v-model="password" required>
        </div>
        <div class="form-group">
          <label for="confirm-password">Confirm Password:</label>
          <input type="password" id="confirm-password" v-model="confirmPassword" required>
        </div>
        <button type="submit">Sign Up</button>
      </form>
    </div>
  </template>
  
  <script>
import axios from 'axios';
import { useToast } from 'vue-toastification';
export default {
  name: 'SignUp',
  data() {
    return {
      name: '',
      email: '',
      password: '',
      confirmPassword: ''
    };
  },
  methods: {
    async submitForm() {
      try {
        const formData = {
          name: this.name,
          email: this.email,
          password: this.password,
          confirmPassword: this.confirmPassword
        };

        // Send the form data to the backend API
        const response = await axios.post('http://localhost:5000/api/signup', formData);

        // Handle the response as needed
        console.log(response.data);
        alert("Account created");
        const toast = useToast();
        toast.success('Account created successfully!', {
          position: 'top-right',
          timeout: 3000,
          closeOnClick: true,
          pauseOnHover: true
        });
        // Clear the form fields
        this.name = '';
        this.email = '';
        this.password = '';
        this.confirmPassword = '';
      } 
      
      catch (error) {
        // Handle error
        console.error(error);
      }
    }
  }
};
</script>
  
  <style scoped>
  h2 {
    font-size: 24px;
    margin-bottom: 20px;
  }
  
  .signup-form {
    display: flex;
    flex-direction: column;
    align-items: flex-start;
  }
  
  .form-group {
    margin-bottom: 20px;
    margin-left: 200px;
  }
  
  label {
    font-weight: bold;
    margin-right: 150px;
  }
  
  input {
    padding: 8px;
    width: 250px;
  }
  
  button {
    padding: 10px 20px;
    border-radius: 8px;
    background-color: #42b983;
    color: white;
    border: none;
    cursor: pointer;
  }
  
  button:hover {
    background-color: #318e6d;
  }
  </style>
