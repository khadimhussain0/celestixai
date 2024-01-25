<template>
    <div>
      <!-- Landing page content -->
      <p>test here</p>
      <button @click="redirectToCreateAccount">Create an Account</button>
    </div>
  </template>
  
  <script>
  export default {
    methods: {
      redirectToCreateAccount() {
        this.$router.push('/login');
      },
    },
  };
  </script>
  
  <style scoped>
  /* Your styles for landing page */
  </style>
  