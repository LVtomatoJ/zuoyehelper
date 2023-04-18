import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import LoginView from '../views/LoginView.vue'
import RegView from '../views/RegView.vue'
import AboutView from '../views/AboutView.vue'
import CollectView from '../views/public/CollectView.vue'
import UserIndexView from '../views/user/UserIndexView.vue'
import AddCollectView from '../views/user/AddCollectView.vue'
import { useLoginStore } from '../stores/login'


const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      path: '/login',
      name: 'login',
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: LoginView
    },
    {
      path: '/reg',
      name: 'reg',
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: RegView
    },
    {
      path: '/about',
      name: 'about',
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: AboutView
    },
    {
      path:'/public/collect/:collect_id',
      name:'publiccollect',
      component:CollectView
    },
    {
      path: '/user/index',
      name: 'user_index',
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: UserIndexView
    },
    {
      path: '/user/addcollect/:type',
      name: 'user_add_collect',
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: AddCollectView
    }

  ]
})

router.beforeEach((to) => {
  const store = useLoginStore()
  if (!store.isLoggedIn&&to.name!=='login'&&to.name!=='home'&&to.name!=='publiccollect'&&to.name!=='reg')
    return '/login'
})


export default router