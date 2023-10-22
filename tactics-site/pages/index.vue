<script setup lang="ts">
import yaml from 'js-yaml'
import { get_image_path } from '~/composables/imagePath'
import Hero from '~/components/Hero.vue'
import type { Game } from '~/composables/gameTypes'

const yamlText = ref('')
const yamlContent = ref<Game>()

onMounted(async () => {
  const response = await fetch('/input.yaml')
  yamlText.value = await response.text()
  yamlContent.value = yaml.load(yamlText.value)
})

const heroes = computed(() => {
  if (!yamlContent.value) {
    return []
  }

  const heroIds = []
  for (const gameSet of yamlContent.value.sets) {
    for (const hero of gameSet.heroes) {
      heroIds.push({ nameWithSet: `${hero.name} (${gameSet.name})`, version: hero.version })
    }
  }
  return heroIds
})

const maps = computed(() => {
  if (!yamlContent.value) {
    return []
  }

  const mapIds = []
  for (const gameSet of yamlContent.value.sets) {
    for (const gameMap of gameSet.maps) {
      mapIds.push({ name: gameMap.name, version: gameMap.version })
    }
  }
})
</script>

<template>
  <GameReportForm :heroes="heroes" :maps="maps" />

  <div v-if="yamlContent" m-4 font-sans md:m-6>
    <ICollapsible>
      <ICollapsibleItem
        v-for="set of yamlContent.sets" :key="set.name" :title="set.name" accordion
        rounded bg-gray shadow-md
      >
        <div m-3>
          <pre>{{ set.description }}</pre>
        </div>

        <ICollapsible>
          <ICollapsibleItem title="Rules" accordian rounded bg-gray-50>
            <div v-for="rule of set.rules" :key="rule.name" my-2 border border-gray rounded p-2>
              <div flex items-start>
                <img
                  :src="get_image_path([set.name, `${set.name}_rules`, rule.name])"
                  :alt="rule.name"
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
          </ICollapsibleItem>

          <ICollapsibleItem
            v-for="hero of set.heroes" :key="hero.name" :title="hero.name" accordian
            rounded bg-gray-50
          >
            <Hero :hero="hero" :set="set" />
          </ICollapsibleItem>
        </ICollapsible>
      </ICollapsibleItem>
    </ICollapsible>
  </div>
</template>

<style scoped>
pre {
  white-space: pre-wrap;
}
</style>
