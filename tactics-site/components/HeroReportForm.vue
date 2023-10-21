<script setup lang="ts">
import { IFormGroup, IInput } from '@inkline/inkline'
import type { PropType } from 'vue'
import { useVModel } from '@vueuse/core'
import type { Hero, HeroReport } from '~/composables/gameTypes'

const props = defineProps({
  modelValue: {
    type: Object as PropType<HeroReport>,
    required: true,
  },
  heroes: {
    type: Array as PropType<Hero[]>,
    required: true,
  },
})

const emit = defineEmits(['update:modelValue'])

const heroNames = computed(() => props.heroes.map(hero => hero.name))

const isGreat = ref(false)
const isTerrible = ref(false)

watch([isGreat, isTerrible], ([newIsGreat, newIsTerrible]) => {
  if (newIsGreat && !newIsTerrible) {
    isTerrible.value = false
    emit('update:modelValue', {
      ...props.modelValue,
      impression: 'Great',
    })
  }
  else if (newIsTerrible && !newIsGreat) {
    isGreat.value = false
    emit('update:modelValue', {
      ...props.modelValue,
      impression: 'Terrible',
    })
  }
  else {
    emit('update:modelValue', {
      ...props.modelValue,
      impression: undefined,
    })
  }
})

function setIsGreat() {
  isGreat.value = true
  isTerrible.value = false
}
function setIsTerrible() {
  isGreat.value = false
  isTerrible.value = true
}

const getImpression = computed(() => {
  if (isGreat.value) {
    return 'Great'
  }
  if (isTerrible.value) {
    return 'Terrible'
  }
})

const heroReport = useVModel(props, 'modelValue', emit)
</script>

<template>
  <i-container mt-4 border-1 border-gray-6 rd py-6>
    <v-select v-model="heroReport.name" :options="heroNames" bg-white text-black placeholder="Hero Name" />

    <IFormGroup mt-2>
      <IInput id="hero-note" v-model="heroReport.note" type="text" placeholder="Hero Note?" />
    </IFormGroup>

    <i-checkbox-group>
      <div flex>
        <i-checkbox v-model="isTerrible" type="radio" input-id="impression-terrible">
          <i-form-label text-white for="impression-terrible">
            Did little?
          </i-form-label>
        </i-checkbox>

        <i-checkbox v-model="isGreat" type="radio" input-id="impression-great">
          <i-form-label text-white for="impression-great">
            An MVP?
          </i-form-label>
        </i-checkbox>
      </div>
    </i-checkbox-group>
  </i-container>
</template>
