import Vue from 'vue'
import App from './App.vue'
import router from './router'
import JsMind from './components/JsMind/index'
import VueAnalytics from 'vue-analytics'
import {store} from "./store"

Vue.config.productionTip = false
Vue.use(JsMind)
Vue.use(VueAnalytics,{
  id : 'UA-112917851-2',
  router,
})

new Vue({
  router,
  store: store,
  render: h => h(App)
}).$mount('#app')

