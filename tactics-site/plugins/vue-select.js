import { defineNuxtPlugin } from '#app'
import 'vue-select/dist/vue-select.css'
import vSelect from 'vue-select'

export default defineNuxtPlugin((nuxtApp) => {
  nuxtApp.vueApp.component('v-select', vSelect)
})
