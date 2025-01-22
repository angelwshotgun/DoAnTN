// https://nuxt.com/docs/api/configuration/nuxt-config
import Aura from '@primevue/themes/aura';
import path from 'path';

export default defineNuxtConfig({
  compatibilityDate: '2024-11-01',
  devtools: { enabled: true },
  modules: [
    '@primevue/nuxt-module',
    '@nuxtjs/tailwindcss',
    '@nuxtjs/google-fonts',
  ],
  primevue: {
    options: {
      theme:{
        preset: Aura
      }
    }
  },
  googleFonts: {
    families: {
      'Roboto': true,
    },
    preload: true,
  },
  css: [path.resolve(__dirname, 'assets/global.scss'), 'primeicons/primeicons.css'],
})
