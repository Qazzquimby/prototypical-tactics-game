<script setup lang="ts">
import { IFormGroup, IInput } from '@inkline/inkline'
import type { PropType } from 'vue'
import { useVModel } from '@vueuse/core'
import type { HeroReport } from '~/composables/gameTypes'

const props = defineProps({
  modelValue: {
    type: Object as PropType<HeroReport>,
    required: true,
  },
})

const emit = defineEmits(['update:modelValue'])
const heroReport = useVModel(props, 'modelValue', emit)
</script>

<template>
  <i-container mt-2 border-1 border-gray-6 rd>
    <IFormGroup>
      <i-form-label for="hero-name" />
      <IInput id="hero-name" v-model="heroReport.name" type="text" placeholder="Name" />
    </IFormGroup>

    <IFormGroup>
      <IInput id="hero-note" v-model="heroReport.note" type="text" placeholder="Note?" />
    </IFormGroup>

    <i-checkbox-group>
      <div flex>
        <i-checkbox v-model="heroReport.impression" type="radio" input-id="impression-terrible" true-value="Terrible">
          <i-form-label text-white for="impression-terrible">
            Did little?
          </i-form-label>
        </i-checkbox>

        <i-checkbox v-model="heroReport.impression" type="radio" input-id="impression-great" true-value="Great">
          <i-form-label text-white for="impression-great">
            An MVP?
          </i-form-label>
        </i-checkbox>
      </div>
    </i-checkbox-group>
  </i-container>
</template>
