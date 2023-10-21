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

// const isGreat = ref(false)
// const isTerrible = ref(true)

const impression = ref<'Great' | 'Terrible' | null>(null)
const impressionGreat = ref(false)
const impressionTerrible = ref(false)

function updateImpression(value: ('Great' | 'Terrible')) {
  if (value === 'Terrible') {
    impressionGreat.value = false
    if (impression.value === 'Terrible') {
      impression.value = null
    }
    else {
      impression.value = 'Terrible'
    }
  }
  else if (value === 'Great') {
    impressionTerrible.value = false
    if (impression.value === 'Great') {
      impression.value = null
    }
    else {
      impression.value = 'Great'
    }
  }
}

// watch([isGreat, isTerrible], ([newIsGreat, newIsTerrible]) => {
//   if (newIsGreat) {
//     isTerrible.value = false
//     emit('update:modelValue', {
//       ...props.modelValue,
//       impression: 'Great',
//     })
//   }
// else if (newIsTerrible) {
//   isGreat.value = false
//   isTerrible.value = true
//   emit('update:modelValue', {
//     ...props.modelValue,
//     impression: 'Terrible',
//   })
// }
// else {
//   isGreat.value = false
//   isTerrible.value = false
//   emit('update:modelValue', {
//     ...props.modelValue,
//     impression: undefined,
//   })
// }
// })

// const getImpression = computed(() => {
//   if (isGreat.value) {
//     return 'Great'
//   }
//   if (isTerrible.value) {
//     return 'Terrible'
//   }
// })

const heroReport = useVModel(props, 'modelValue', emit)
</script>

<template>
  <i-container mt-4 border-1 border-gray-6 rd py-6>
    <v-select v-model="heroReport.name" :options="heroNames" rd bg-white text-black placeholder="Hero Name" />

    <IFormGroup mt-2>
      <IInput id="hero-note" v-model="heroReport.note" type="text" placeholder="Hero Note?" />
    </IFormGroup>

    <div flex>
      <i-checkbox v-model="impressionTerrible" type="radio" input-id="impression-terrible" @change="updateImpression('Terrible')">
        <i-form-label text-white for="impression-terrible">
          Did little?
        </i-form-label>
      </i-checkbox>

      <i-checkbox v-model="impressionGreat" type="radio" input-id="impression-great" @change="updateImpression('Great')">
        <i-form-label text-white for="impression-great">
          An MVP?
        </i-form-label>
      </i-checkbox>
    </div>
  </i-container>
</template>
