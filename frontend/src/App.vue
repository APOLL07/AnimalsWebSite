<template>
  <div class="app">
    <AppHeader />
    <main>
      <RouterView />
    </main>
    <AppFooter />

    <LoginModal v-if="auth.showLoginModal" @close="auth.showLoginModal = false" />
    <ToastContainer />
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { RouterView } from 'vue-router'
import AppHeader from './components/AppHeader.vue'
import AppFooter from './components/AppFooter.vue'
import LoginModal from './components/LoginModal.vue'
import ToastContainer from './components/ToastContainer.vue'
import { useAuthStore } from './stores/auth'

const auth = useAuthStore()

onMounted(() => {
  auth.checkAuth()
})
</script>
