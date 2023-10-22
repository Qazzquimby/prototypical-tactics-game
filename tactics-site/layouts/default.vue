<script setup lang="ts">
const title = 'TABLETOP_TEAMFIGHT'
const titleArray = computed(() => title.split(''))
</script>

<template>
  <div id="header" flex flex-col items-center justify-center bg-gray-3 text-black>
    <div w-full flex items-center justify-between px-8rem py-1 text-xl lg:w-55rem>
      <span v-for="(letter, key) in titleArray" :key="key" class="letter">{{ letter }}</span>
    </div>

    <div flex="~" justify-center>
      <router-link :class="{ 'active-link': $route.path === '/rules' }" to="/rules" inline-block bg-gray-4 p-4>
        Rules
      </router-link>
      <router-link :class="{ 'active-link': $route.path === '/compendium' }" to="/compendium" inline-block bg-gray-4 p-4>
        Compendium
      </router-link>
      <router-link :class="{ 'active-link': $route.path === '/reports' }" to="/reports" inline-block bg-gray-4 p-4>
        Reports
      </router-link>
    </div>
  </div>
  <main class="px-10 py-10">
    <slot />
  </main>
</template>

<style scoped>
  .active-link {
    font-weight: bold;
    @apply bg-gray-3;
  }
</style>
