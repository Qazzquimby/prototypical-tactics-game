import { pwa } from './config/pwa'
import { appDescription } from './constants/index'

export default defineNuxtConfig({
  modules: [
    'nuxt-vuefire',
    'nuxt-primevue',
    '@inkline/plugin/nuxt',
    '@vueuse/nuxt',
    '@unocss/nuxt',
    '@pinia/nuxt',
    '@nuxtjs/color-mode',
    '@vite-pwa/nuxt',
  ],
  vuefire: {
    config: {
      apiKey: 'AIzaSyDMMtuzQY8-0TzjMZD9Ll8pi4HMxOOAWLg',
      authDomain: 'tabletop-teamfight.firebaseapp.com',
      projectId: 'tabletop-teamfight',
      storageBucket: 'tabletop-teamfight.appspot.com',
      messagingSenderId: '831358413965',
      appId: '1:831358413965:web:282ff4ddbe5046839786c4',
    },
  },
  primevue: {
    components: {
      include: ['Dropdown'],
    },
  },

  plugins: [
    '~/plugins/vue-select.js',
  ],

  // services: {
  //   firestore: true,
  // },
  experimental: {
    // when using generate, payload js assets included in sw precache manifest
    // but missing on offline, disabling extraction it until fixed
    payloadExtraction: false,
    inlineSSRStyles: false,
    renderJsonPayloads: true,
    typedPages: true,
  },

  css: [
    '@unocss/reset/tailwind.css',
    '~/styles/global.css',
  ],

  colorMode: {
    classSuffix: '',
  },

  nitro: {
    esbuild: {
      options: {
        target: 'esnext',
      },
    },
    prerender: {
      crawlLinks: false,
      routes: ['/', '/images/*'],
      ignore: ['/hi'],
    },
  },

  app: {
    head: {
      viewport: 'width=device-width,initial-scale=1',
      link: [
        { rel: 'icon', href: '/favicon.ico', sizes: 'any' },
        { rel: 'icon', type: 'image/svg+xml', href: '/nuxt.svg' },
        { rel: 'apple-touch-icon', href: '/apple-touch-icon.png' },
      ],
      meta: [
        {
          name: 'viewport',
          content: 'width=device-width, initial-scale=1',
        },
        { name: 'description', content: appDescription },
        {
          name: 'apple-mobile-web-app-status-bar-style',
          content: 'black-translucent',
        },
      ],
    },
  },

  pwa,

  devtools: {
    enabled: true,
  },
})
