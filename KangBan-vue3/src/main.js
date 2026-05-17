import { createApp } from 'vue'
import './style.css'
import App from './App.vue'
import router from './router'
import { createPinia } from 'pinia'
import { Icon } from '@iconify/vue'

const app = createApp(App)
app.use(router)
app.use(createPinia())
app.component('iconify-icon', Icon)
app.mount('#app')
