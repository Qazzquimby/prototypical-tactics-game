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
  return `/image_${path}.jpg`
}
</script>

<template>
  <div v-if="yamlContent" m-4 font-sans text-gray-700 md:m-6>
    <div v-for="set of yamlContent.sets" :key="set.name" mb-6 rounded bg-white p-4 shadow-md>
      <div flex items-start>
        <h2 text-primary-700 mb-2 flex-grow text-xl font-bold>
          {{ set.name }}
        </h2>
        <p text-gray-600>
          {{ set.description }}
        </p>
      </div>

      <div v-for="rule of set.rules" :key="rule.name" my-2 rounded bg-blue-100 p-2>
        <div flex items-start>
          <img :src="get_image_path([set.name, `${set.name}_rules`, rule.name])" :alt="rule.name" mx-2 h-32 rounded object-contain>
          <div>
            <h3 text-secondary-700 font-bold>
              {{ rule.name }}
            </h3>
            <p>{{ rule.text }}</p>
          </div>
        </div>
      </div>

      <div v-for="hero of set.heroes" :key="hero.name" my-4 b-2 rounded bg-gray-50 p-2>
        <div flex items-start>
          <img :src="get_image_path([set.name, hero.name, hero.name])" :alt="hero.name" mx-2 mt-2 h-32 rounded object-contain>
          <div>
            <h3 text-primary-700 font-bold>
              {{ hero.name }}
            </h3>
            <p>{{ hero.description }}</p>
          </div>
        </div>

        <div v-for="ability of hero.abilities" :key="ability.name" my-2 rounded bg-blue-100 p-2>
          <div class="flex items-start">
            <img :src="get_image_path([set.name, hero.name, ability.name])" :alt="ability.name" mx-2 mt-2 h-32 rounded object-contain>
            <div>
              <h4 class="text-primary-600 font-bold">
                {{ ability.name }}
              </h4>
              <p>{{ ability.text }}</p>
            </div>
          </div>
        </div>

        <div v-for="unit of hero.units" :key="unit.name" my-2>
          <div class="flex items-start">
            <img :src="get_image_path([set.name, hero.name, unit.name])" :alt="unit.name" mx-2 mt-2 h-32 rounded object-contain>
            <h4 class="text-primary-600 font-bold">
              {{ unit.name }}
            </h4>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
