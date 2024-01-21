<template>
  <div v-if="isLoggedIn">
    <div class="main-container">
      <div class="menu-container">
        <div class="menu">
          <div v-for="(tab, index) in tabs" :key="index" @click="changeTab(index)" :class="{ active: activeTab === index }">
            {{ tab }}
          </div>
        </div>
        <button class="logout-button" @click="logout">Log Out</button>
      </div>
      <div class="content-container">
        <div v-if="activeTab === 0">Dashboard Content</div>
        <div v-if="activeTab === 1">Text Corpus Content</div>
        <div v-if="activeTab === 2">
          <!-- Render model cards for LLM Constellation -->
          <div v-for="model in modelData" :key="model.id" class="model-card">
            <img src="https://picsum.photos/200" alt="Model Icon" class="model-icon" />
            <div class="model-info">
              <div class="model-parameter">{{ model.parameters }}</div>
              <div class="model-class">{{ model.model_class }}</div>
              <div class="model-task">{{ model.model_task }}</div>
              <div class="model-name">{{ model.model_name }}</div>
              <div class="add-to-workspace-button"><input type="button" value="Add to Workspace"></div>
            </div>
          </div>
        </div>
        <div v-if="activeTab === 3">
          <!-- Render model cards for LLM Constellation -->
          <div v-for="model in modelData" :key="model.id" class="model-card">
            <img src="https://picsum.photos/200" alt="Model Icon" class="model-icon" />
            <div class="model-info">
              <div class="model-parameter">{{ model.parameters }}</div>
              <div class="model-class">{{ model.model_class }}</div>
              <div class="model-task">{{ model.model_task }}</div>
              <div class="model-name">{{ model.model_name }}</div>
              <div class="add-to-workspace-button"><input type="button" value="Add to Workspace"></div>
            </div>
          </div>
        </div>
        <div v-if="activeTab === 4">Chat Content</div>
        <div v-if="activeTab === 5">Deployments Content</div>
      </div>
    </div>
  </div>
  <div v-else>
    <!-- Login form when user is not logged in -->
    <div class="login-container">
      <h1>Login</h1>
      <form @submit.prevent="login">
        <label for="username">Username:</label>
        <input type="text" v-model="username" required>
        <label for="password">Password:</label>
        <input type="password" v-model="password" required>
        <button type="submit">Login</button>
      </form>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      tabs: ["Dashboard", "Text Corpus", "LLMs", "LLM Constellation", "Chat", "Deployments"],
      activeTab: 0,
      isLoggedIn: false,
      username: '',
      password: '',
      modelData: [],
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
        // });

        });

        const accessToken = response.data.access_token;

        // You can store the token in local storage or a secure cookie for future requests
        localStorage.setItem('accessToken', accessToken);

        // Set isLoggedIn to true to show the main UI
        this.isLoggedIn = true;

        // Fetch LLM Constellation data after successful login
        this.fetchModelData();
      } catch (error) {
        console.error('Login failed', error);
        // Handle login failure (show error message, reset form, etc.)
      }
    },
    changeTab(index) {
      this.activeTab = index;

      // Fetch LLM Constellation data when the tab is clicked
      if (index === 3 && this.isLoggedIn) {
        this.fetchModelData();
      }
    },
    logout() {
      // Clear the token from local storage or cookie
      localStorage.removeItem('accessToken');

      // Set isLoggedIn to false to show the login form
      this.isLoggedIn = false;
    },
    async fetchModelData() {
  try {
    // Retrieve the token from localStorage
    const accessToken = localStorage.getItem('accessToken');

    // Check if the token is present before making the request
    if (!accessToken) {
      console.error('Access token not found. Please authenticate first.');
      return;
    }

    const response = await axios.get('http://127.0.0.1:8000/model_constellation/', {
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
,
  },
  mounted() {
    // Check if the user is already logged in (e.g., token exists in local storage)
    const accessToken = localStorage.getItem('accessToken');
    if (accessToken) {
      this.isLoggedIn = true;
    }
  },
};
</script>

<style scoped>
.main-container {
  display: flex;
  height: 100vh;
}

.menu-container {
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  background-color: #2c3e50; /* Dark background color */
  color: #ecf0f1; /* Light text color */
  padding: 20px;
  width: 200px;
  border-top-left-radius: 15px;
  border-bottom-left-radius: 15px;
  overflow-y: auto;
}

.menu {
  display: flex;
  flex-direction: column;
}

.menu div {
  padding: 10px;
  cursor: pointer;
  transition: background-color 0.3s;
  border-radius: 8px; /* Rounded corners for tabs */
  text-align: left; /* Align text to the left within tabs */
}

.menu div:hover {
  background-color: #34495e; /* Darker background color on hover */
}

.menu div.active {
  background-color: #3498db; /* Active tab color */
  font-weight: bold;
}

.logout-button {
  background-color: #e74c3c; /* Logout button color */
  color: #ecf0f1; /* Logout button text color */
  border: none;
  padding: 10px;
  cursor: pointer;
  transition: background-color 0.3s;
  border-radius: 8px; /* Rounded corners for the logout button */
  text-align: left; /* Align text to the left within the logout button */
}

.logout-button:hover {
  background-color: #c0392b; /* Darker logout button color on hover */
}

.content-container {
  flex-grow: 1;
  padding: 20px;
  /* margin-left: 20px;  */
  overflow-y: auto; /* Enable vertical scrolling for the content area */
}

.login-container {
  max-width: 300px;
  margin: 100px auto;
  padding: 20px;
  border: 1px solid #ddd;
  border-radius: 8px;
}

.login-container h1 {
  text-align: center;
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

.login-container button {
  background-color: #3498db;
  color: #fff;
  padding: 10px;
  cursor: pointer;
  border: none;
  border-radius: 4px;
}

.model-card {
  display: flex;
  align-items: center;
  margin-bottom: 20px;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 8px;
  position: relative;
}

.model-icon {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  margin-right: 10px;
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
.add-to-workspace-button {
  position: absolute;
  margin-left: auto;
  top: 50%;
  right: 10px;
  transform: translateY(-50%);
  text-align: center;
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
