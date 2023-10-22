<script setup lang="ts">
import yaml from 'js-yaml'
import type { Game } from '~/composables/gameTypes'

const yamlText = ref('')
const yamlContent = ref<Game>()

onMounted(async () => {
  const response = await fetch('/input.yaml')
  yamlText.value = await response.text()
  yamlContent.value = yaml.load(yamlText.value)
})
// todo make the yamltext a shared composable, only loaded once

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
    if (!gameSet.maps) {
      continue
    }
    for (const gameMap of gameSet.maps) {
      mapIds.push({ name: gameMap.name, version: gameMap.version })
    }
  }
})
</script>

<template>
  <GameReportForm :heroes="heroes" :maps="maps" />
</template>
