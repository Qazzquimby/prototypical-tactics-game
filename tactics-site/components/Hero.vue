<script setup lang="ts">
import type { GameSet, HeroDeck } from '~/composables/gameTypes'

import { get_image_path } from '~/composables/imagePath'

defineProps<{
  set: GameSet
  hero: HeroDeck
}>()
</script>

<template>
  <div>
    <div flex items-start>
      <img
        :src="get_image_path([set.name, hero.name, hero.name])" :alt="hero.name" mx-2 mt-2
        h-32 rounded object-contain
      >
      <div>
        <h3 text-primary-700 font-bold>
          {{ hero.name }} - {{ hero.health }} health,
          {{ hero.speed }} speed
        </h3>
        <pre>{{ hero.description }}</pre>

        <p v-if="hero.passives">
          ---
        </p>
        <div v-for="passive of hero.passives" :key="passive.name">
          <h4 class="text-primary-600 font-bold">
            {{ passive.name }}
          </h4>
          <pre>{{ passive.text }}</pre>
        </div>

        <p v-if="hero.default_abilities">
          ---
        </p>
        <div v-for="def of hero.default_abilities" :key="def.name">
          <h4 class="text-primary-600 font-bold">
            {{ def.name }}
          </h4>
          <pre>{{ def.text }}</pre>
        </div>
      </div>
    </div>


    <div v-for="ability of hero.abilities" :key="ability.name" my-2 rounded bg-blue-100 p-2>
      <div class="flex items-start">
        <img
          :src="get_image_path([set.name, hero.name, ability.name])" :alt="ability.name"
          mx-2
          mt-2 h-32 rounded object-contain
        >
        <div>
          <h4 class="text-primary-600 font-bold">
            {{ ability.name }}
          </h4>
          <pre>{{ ability.text }}</pre>
        </div>
      </div>
    </div>

    <div v-for="unit of hero.units" :key="unit.name" my-2>
      <Unit :image-path="get_image_path([set.name, hero.name, unit.name])" :unit="unit" />
    </div>
  </div>
</template>

<style scoped>
pre {
  white-space: pre-wrap;
}
</style>
