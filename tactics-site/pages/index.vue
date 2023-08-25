<script setup lang="ts">
import yaml from 'js-yaml'
import type { Game } from 'composables/gameTypes'
import { get_image_path } from '~/composables/imagePath'
import Hero from '~/components/Hero.vue'

const yamlText = ref('')
const yamlContent = ref<Game>()

onMounted(async () => {
  const response = await fetch('/input.yaml')
  yamlText.value = await response.text()
  yamlContent.value = yaml.load(yamlText.value)
})
</script>

<template>
  <div v-if="yamlContent" m-4 font-sans text-gray-700 md:m-6>
    <div v-for="set of yamlContent.sets" :key="set.name" mb-6 rounded bg-white p-4 shadow-md>
      <div>
        <h2 text-primary-700 mb-2 text-xl font-bold>
          {{ set.name }}
        </h2>
        <pre text-gray-600>{{ set.description }}</pre>
      </div>

      <div v-for="rule of set.rules" :key="rule.name" my-2 rounded bg-blue-100 p-2>
        <div flex items-start>
          <img
            :src="get_image_path([set.name, `${set.name}_rules`, rule.name])" :alt="rule.name"
            mx-2 h-32 rounded object-contain
          >
          <div>
            <h3 text-secondary-700 font-bold>
              {{ rule.name }}
            </h3>
            <pre>{{ rule.text }}</pre>
          </div>
        </div>
      </div>

      <ICollapsible>
      <ICollapsibleItem :title="hero.name" accordian v-for="hero of set.heroes" :key="hero.name" my-4 b-2 rounded bg-gray-50 p-2>
        <Hero :hero="hero" :set="set" />
      </ICollapsibleItem>
      </ICollapsible>
    </div>
  </div>
</template>

<style scoped>
pre {
  white-space: pre-wrap;
}
</style>
