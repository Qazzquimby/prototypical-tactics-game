<script setup lang="ts">
import type { PropType } from 'vue'
import { ref } from 'vue'
import { IButton, IForm, IFormGroup, IInput } from '@inkline/inkline'
import type { GameMap, GameReport, Hero, HeroReport } from '~/composables/gameTypes'

const props = defineProps({
  heroes: {
    type: Array as PropType<Hero[]>,
    required: true,
  },
  maps: {
    type: Array as PropType<GameMap[]>,
    required: true,
  },
})

const gameReport = ref<GameReport>({
  redScore: undefined,
  blueScore: undefined,
  redHeroes: [{ name: '', version: undefined, note: '', impression: undefined }],
  blueHeroes: [{ name: '', version: undefined, note: '', impression: undefined }],
  note: '',
  map: '',
})

const mapNames = computed(() => props.maps.map(gameMap => gameMap.name))

function addHero() {
  gameReport.value.redHeroes.push({ name: '', version: undefined, note: '', impression: undefined })
  gameReport.value.blueHeroes.push({ name: '', version: undefined, note: '', impression: undefined })
}

function updateRedHeroReport(index: number, updatedReport: HeroReport) {
  gameReport.value.redHeroes[index] = updatedReport
}

function updateBlueHeroReport(index: number, updatedReport: HeroReport) {
  gameReport.value.blueHeroes[index] = updatedReport
}

function submitForm() {
  console.log(gameReport.value)
}
</script>

<template>
  <IForm my-8 @submit="submitForm">
    <h1 text-2xl>
      Report Game
    </h1>

    <v-select v-model="gameReport.map" :options="mapNames" my-2 rd bg-white text-black placeholder="Map Name" />

    <IFormGroup>
      <IInput id="game-note" v-model="gameReport.note" type="text" placeholder="Game note?" />
    </IFormGroup>

    <i-row mt-4>
      <i-column sm="6">
        <IFormGroup>
          <IFormLabel for="red-score">
            Red Score
          </IFormLabel>
          <IInput id="red-score" v-model="gameReport.redScore" type="number" />
        </IFormGroup>
      </i-column>
      <i-column sm="6">
        <IFormGroup>
          <IFormLabel for="blue-score">
            Blue Score
          </IFormLabel>
          <IInput id="blue-score" v-model="gameReport.blueScore" type="number" />
        </IFormGroup>
      </i-column>
    </i-row>

    <i-row mb-1>
      <i-column sm="6">
        <div v-for="(heroReport, index) in gameReport.redHeroes" :key="index">
          <HeroReportForm :model-value="heroReport" :heroes="props.heroes" @update:model-value="val => updateRedHeroReport(index, val)" />
        </div>
      </i-column>

      <i-column sm="6">
        <div v-for="(heroReport, index) in gameReport.blueHeroes" :key="index">
          <HeroReportForm :model-value="heroReport" :heroes="props.heroes" @update:model-value="val => updateBlueHeroReport(index, val)" />
        </div>
      </i-column>
    </i-row>

    <i-row>
      <IButton mx-1rem h-3rem w-full rd-1 @click="addHero">
        <span translate-y--2px text-white>Add Heroes</span>
      </IButton>
    </i-row>

    <div mt-4>
      <i-row h-4 justify-center>
        <IButton type="submit" text-white>
          Submit
        </IButton>
      </i-row>
    </div>
  </IForm>
</template>
