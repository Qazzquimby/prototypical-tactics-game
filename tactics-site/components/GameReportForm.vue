<script setup lang="ts">
import { ref } from 'vue'
import { IButton, IForm, IFormGroup, IInput } from '@inkline/inkline'
import type { GameReport } from '~/composables/gameTypes'

const gameReport = ref<GameReport>({
  redScore: null,
  blueScore: null,
  redHeroes: [{ name: '', version: null, note: '', impression: '' }],
  blueHeroes: [{ name: '', version: null, note: '', impression: '' }],
  note: '',
  map: '',
})

function addHero() {
  gameReport.value.redHeroes.push({ name: '', version: null, note: '', impression: '' })
  gameReport.value.blueHeroes.push({ name: '', version: null, note: '', impression: '' })
}

function updateRedHeroReport(index, updatedReport) {
  gameReport.value.redHeroes[index] = updatedReport
}

function updateBlueHeroReport(index, updatedReport) {
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

    <IFormGroup>
      <IFormLabel for="game-note">
        Where was it?
      </IFormLabel>
      <IInput id="game-note" v-model="gameReport.map" type="text" />
    </IFormGroup>

    <IFormGroup>
      <IFormLabel for="game-note">
        How'd it go?
      </IFormLabel>
      <IInput id="game-note" v-model="gameReport.note" type="text" />
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
          <HeroReportForm :model-value="heroReport" @update:model-value="val => updateRedHeroReport(index, val)" />
        </div>
      </i-column>

      <i-column sm="6">
        <div v-for="(heroReport, index) in gameReport.blueHeroes" :key="index">
          <HeroReportForm :model-value="heroReport" @update:model-value="val => updateBlueHeroReport(index, val)" />
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
