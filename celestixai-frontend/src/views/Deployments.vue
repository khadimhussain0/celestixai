<template>
  <div class="container">
    <div class="content">
      <p class="text">Deployments API</p>
      <div class="coming-soon">
        <p class="text-coming">Coming Soon!</p>
        <div class="indicator"></div>
      </div>
    </div>
  </div>
</template>
  
<script>

</script>
  
<style scoped>
.container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
}

.content {
  text-align: center;
}

.text {
  font-size: 24px;
  font-weight: bold;
  color: #333;
}

.coming-soon {
  position: relative;
  margin-top: 20px;
}

.text-coming {
  font-size: 32px;
  font-weight: bold;
  color: #4CAF50; /* Green color */
  margin-bottom: 10px;
}

.indicator {
  position: absolute;
  top: 50%;
  left: 50%;
  width: 100px;
  height: 100px;
  background: #4CAF50; /* Green color */
  border-radius: 50%;
  animation: pulse 2s infinite;
  transform: translate(-50%, -50%);
}

@keyframes pulse {
  0% {
    transform: translate(-50%, -50%) scale(0.9);
    opacity: 0.5;
  }
  50% {
    transform: translate(-50%, -50%) scale(1.2);
    opacity: 1;
  }
  100% {
    transform: translate(-50%, -50%) scale(0.9);
    opacity: 0.5;
  }
}
</style>
