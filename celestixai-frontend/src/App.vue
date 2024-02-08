<template>
  <div>
    <video autoplay muted loop id="backgroundVideo">
      <source src="@/assets/Gen-2 889013846, a constellation of c, logo-upsampledpng, M 5.mp4" type="video/mp4">
      Your browser does not support the video tag.
    </video>
    <div class="overlay"></div>
    <router-view />
  </div>
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
  padding: 0;
  min-height: 100vh;
  overflow: hidden; /* Ensure video covers entire viewport */
  position: relative;
  overflow-y: auto;
}

#backgroundVideo {
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  min-width: 100%;
  min-height: 100%;
  width: auto;
  height: auto;
  z-index: -1; /* Place video behind other content */
}

.overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.6); /* Adjust the alpha value for darkness */
  z-index: -1; /* Place overlay behind other content */
}

.logo_image {
  position: absolute;
  border-radius: 8px;
  top: 10px;
  left: 10px;
  width: 100px;
  height: auto;
}
</style>
