import { createApp } from 'vue'
import { createPinia } from 'pinia'

import App from './App.vue'
import router from './router'

// import './assets/main.css'

import ViewUIPlus from 'view-ui-plus'
import 'view-ui-plus/dist/styles/viewuiplus.css'

import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'



const app = createApp(App)

app.use(createPinia())
app.use(router)
app.use(ViewUIPlus)
app.use(ElementPlus)

app.mount('#app')
