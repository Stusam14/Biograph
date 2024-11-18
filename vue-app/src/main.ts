// import './assets/main.css'

// import DataZone from 'dropzone-vue'
import { createApp } from 'vue'
import App from './App.vue'
import router from './router/index'

import PrimeVue from 'primevue/config'
import Aura from '@primevue/themes/aura'

const app = createApp(App)
app
  .use(PrimeVue, {
    theme: {
      preset: Aura
    }
  })
  .use(router)
  .mount('#app')
