import { createRouter, createWebHashHistory } from 'vue-router'

const router = createRouter({
  history: createWebHashHistory(),
  // 映射关系: path -> component
  routes: [
    {
      path: "/",
      redirect: "/home"
    },
    {
      path: "/home",
      component: () => import("../views/home/home.vue")
    },
    {
      path: "/photo",
      component: () => import("../views/photo/photo.vue")
    },
    {
      path: "/recorder",
      component: () => import("../views/recorder/recorder.vue")
    }
  ]
})

export default router
