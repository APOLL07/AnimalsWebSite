import { defineStore } from 'pinia'
import { ref } from 'vue'
import { api } from '../api/client'

export const useAuthStore = defineStore('auth', () => {
  const isLoggedIn = ref(false)
  const email = ref('')
  const role = ref('')
  const showLoginModal = ref(false)

  async function checkAuth() {
    try {
      const data = await api.me()
      isLoggedIn.value = true
      email.value = data.email
      role.value = data.role
    } catch {
      isLoggedIn.value = false
      email.value = ''
      role.value = ''
    }
  }

  async function login(emailVal, password) {
    const data = await api.login(emailVal, password)
    isLoggedIn.value = true
    role.value = data.role
    email.value = emailVal
    showLoginModal.value = false
  }

  async function logout() {
    await api.logout()
    isLoggedIn.value = false
    email.value = ''
    role.value = ''
  }

  return { isLoggedIn, email, role, showLoginModal, checkAuth, login, logout }
})
