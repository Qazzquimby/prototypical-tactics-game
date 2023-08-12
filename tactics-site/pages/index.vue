<script setup lang="ts">
import yaml from 'js-yaml'
import type { Game } from 'composables/gameTypes'

const online = useOnline()

// const yamlText = fs.readFileSync('/input.yaml', 'utf8')

const yamlText = ref('')
const yamlContent = ref<Game>()

onMounted(async () => {
  const response = await fetch('/input.yaml')
  yamlText.value = await response.text()
  yamlContent.value = yaml.load(yamlText.value)
})

function get_image_path(names: string[]): string {
  const path = names.join('__')
  return `/images/${path}.jpg`
}
</script>

<template>
  <div v-if="yamlContent">
    <div v-for="set of yamlContent.sets" :key="set.name">
      {{ set.name }}
      {{ set.description }}
      <div v-for="rule of set.rules" :key="rule.name">
        {{ rule.name }}
        {{ rule.text }}
        <img :src="get_image_path([set.name, `${set.name}_rules`, rule.name])" :alt="rule.name" h-120>
      </div>

      <div v-for="hero of set.heroes" :key="hero.name">
        {{ hero.name }}
        {{ hero.description }}
        <img :src="get_image_path([set.name, hero.name, hero.name])" :alt="hero.name" h-120>

        <div v-for="ability of hero.abilities" :key="ability.name">
          {{ ability.name }}
          {{ ability.text }}
          <img :src="get_image_path([set.name, hero.name, ability.name])" :alt="ability.name" h-120>
        </div>

        <div v-for="unit of hero.units" :key="unit.name">
          {{ unit.name }}
          <img :src="get_image_path([set.name, hero.name, unit.name])" :alt="unit.name" h-120>
        </div>
      </div>
    </div>

    <Logos mb-6 />
    <Suspense>
      <ClientOnly>
        <PageView v-if="online" />
        <div v-else text-gray:80>
          You're offline
        </div>
      </ClientOnly>
      <template #fallback>
        <div italic op50>
          <span animate-pulse>Loading...</span>
        </div>
      </template>
    </Suspense>
    <InputEntry />
  </div>
</template>
