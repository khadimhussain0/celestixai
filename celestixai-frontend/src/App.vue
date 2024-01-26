<template>
  <router-view />
</template>

<script>
export default {
  name: 'App',
};
</script>

<style>
body {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #fff;
  margin: 0;
  /* Remove default margin */
  padding: 0;
  /* Remove default padding */
  background: url('../src/assets/logo-unsampled.png') center center no-repeat;
  background-size: cover;
  min-height: 100vh;
  /* Make sure the background covers the entire viewport height */
}


.logo_image {
  position: absolute;
  border-radius: 8px;
  top: 10px;
  left: 10px;
  width: 100px;
  height: auto;
}</style>
