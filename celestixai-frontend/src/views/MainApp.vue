<template>
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
      <div v-if="activeTab === 0">
        <Dashboard />
      </div>
      <div v-if="activeTab === 1">
        <TextCorpus />
      </div>
      <div v-if="activeTab === 2">
        <LLMs />
      </div>
      <div v-if="activeTab === 3">
        <LLMConstellation />
      </div>
      <div v-if="activeTab === 4">
        <Chat />
      </div>
      <div v-if="activeTab === 5">Deployments</div>
    </div>
  </div>
</template>

<script>
import TextCorpus from '@/views/TextCorpus.vue';
import LLMConstellation from '@/views/LLMConstellation.vue';
import LLMs from '@/views/LLMs.vue';
import Chat from '@/views/Chat.vue';
import Dashboard from '@/views/Dashboard.vue';
import Auth from '@/components/Auth.vue'

export default {
  data() {
    return {
      tabs: ["Dashboard", "Text Corpus", "LLMs", "LLM Constellation", "Chat", "Deployments"],
      activeTab: 0,
      isLoggedIn: false,
    };
  },
  components: {
    Dashboard,
    TextCorpus,
    LLMConstellation,
    LLMs,
    Chat,
    Auth
  },
  methods: {
    changeTab(index) {
      this.activeTab = index;
    },
    logout() {
      // Clear the token from local storage or cookie
      localStorage.removeItem('accessToken');
      this.isLoggedIn = false;
      this.$router.push('/auth');
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
.main-container {
  display: flex;
  height: 100vh;
}

.menu-container {
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  background-color: #2c3e50;
  /* Dark background color */
  color: #ecf0f1;
  /* Light text color */
  padding: 20px;
  width: 200px;
  /* border-top-right-radius: 15px;
  border-bottom-right-radius: 15px; */
  border-radius: 10px;
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
  border-radius: 8px;
  /* Rounded corners for tabs */
  text-align: left;
  /* Align text to the left within tabs */
}

.menu div:hover {
  background-color: #34495e;
  /* Darker background color on hover */
}

.menu div.active {
  background-color: #3498db;
  /* Active tab color */
  font-weight: bold;
}

.content-container {
  flex-grow: 1;
  padding: 20px;
  /* margin-left: 20px;  */
  overflow-y: auto;
  /* Enable vertical scrolling for the content area */
}

.logout-button {
  background-color: #e74c3c;
  /* Logout button color */
  color: #ecf0f1;
  /* Logout button text color */
  border: none;
  padding: 10px;
  cursor: pointer;
  transition: background-color 0.3s;
  border-radius: 8px;
  /* Rounded corners for the logout button */
  text-align: left;
  /* Align text to the left within the logout button */
}

.logout-button:hover {
  background-color: #c0392b;
  /* Darker logout button color on hover */
}</style>
