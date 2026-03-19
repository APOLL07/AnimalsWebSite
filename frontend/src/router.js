import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: () => import('./pages/HomePage.vue'),
  },
  {
    path: '/catalog/:animalSlug?',
    name: 'Catalog',
    component: () => import('./pages/CatalogPage.vue'),
  },
  {
    path: '/product/:slug',
    name: 'Product',
    component: () => import('./pages/ProductPage.vue'),
  },
  {
    path: '/search',
    name: 'Search',
    component: () => import('./pages/SearchPage.vue'),
  },
  {
    path: '/:pathMatch(.*)*',
    name: 'NotFound',
    component: () => import('./pages/NotFoundPage.vue'),
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior() {
    return { top: 0 }
  },
})

export default router
