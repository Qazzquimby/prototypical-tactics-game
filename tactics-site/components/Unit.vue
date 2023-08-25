<script setup lang="ts">
import type { UnitCard } from '~/composables/gameTypes'

defineProps<{
  imagePath: string
  unit: UnitCard
}>()
</script>

<template>
  <div class="flex items-start">
    <img
      :src="imagePath" :alt="unit.name" mx-2 mt-2
      h-32 rounded object-contain
    >
    <h4 class="text-primary-600 font-bold">
      {{ unit.name }}
      <p>{{ unit.health }} health</p>
      <p>{{ unit.speed }} speed</p>

      <p v-if="unit.passives">
        ---
      </p>
      <div v-for="passive of unit.passives" :key="passive.name">
        <h4 class="text-primary-600 font-bold">
          {{ passive.name }}
        </h4>
        <pre>{{ passive.text }}</pre>
      </div>

      <p v-if="unit.default_abilities">
        ---
      </p>
      <div v-for="def of unit.default_abilities" :key="def.name">
        <h4 class="text-primary-600 font-bold">
          {{ def.name }}
        </h4>
        <pre>{{ def.text }}</pre>
      </div>
    </h4>
  </div>
</template>

<style scoped>
pre {
  white-space: pre-wrap;
}
</style>
