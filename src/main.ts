import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import pinia from './stores' // 引入 Pinia

createApp(App)
  .use(router)
  .use(pinia) // 挂载 Pinia
  .mount('#app')
import './style.css'
