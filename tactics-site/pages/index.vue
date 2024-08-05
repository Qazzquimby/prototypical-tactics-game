<script setup lang="ts">
import { useRouter } from 'vue-router'

const router = useRouter()

// Redirect to /rules when the component is mounted
onMounted(() => {
  router.push('/rules')
})
</script>

<template>
  <div class="redirect-message">
    <h1>Redirecting to Rules...</h1>
  </div>
</template>

<style scoped>
.redirect-message {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  font-family: Arial, sans-serif;
}

h1 {
  font-size: 24px;
  color: #333;
}
</style>
