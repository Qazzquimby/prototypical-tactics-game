<script setup lang="ts">
import fs from 'node:fs'
import yaml from 'js-yaml'
import type { Game } from 'composables/gameTypes'

const online = useOnline()

const yamlText = fs.readFileSync('./public/input.yaml', 'utf8')
const yamlContent: Game = yaml.load(yamlText)

function get_image_path(names: string[]): string {
  const path = names.join('__')
  return `./public/images/${path}.jpg`
}

</script>

<template>
  <div>
    <div v-for="set of yamlContent.sets" :key="set.name">
      {{ set.name }}
      {{set.description}}
      <div v-for="rule of yamlContent.rules" :key="rule.name">
        {{ rule.name }}
        {{rule.text}}
        <img :src="get_image_path([set.name, rule.name])" />
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
