import { createRouter, createWebHistory } from 'vue-router'
import Files from '../views/Files.vue'
import ModelsView from '../views/ModelsView.vue'
import Search from '../views/Search.vue'
import Settings from '../views/Settings.vue'
import Home from '../views/Home.vue'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      component: Home
    },
    {
      path: '/files',
      component: Files
    },
    {
      path: '/details',
      component: ModelsView
    },
    {
      path: '/search',
      component: Search
    },
    {
      path: '/settings',
      component: Settings
    }
  ]
})

export default router
