import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useNotifications = defineStore('notifications', () => {
  const items = ref([])
  let nextId = 0

  function show(message, type = 'success', duration = 3000) {
    const id = nextId++
    items.value.push({ id, message, type })
    setTimeout(() => {
      items.value = items.value.filter((n) => n.id !== id)
    }, duration)
  }

  function success(message) { show(message, 'success') }
  function error(message) { show(message, 'error') }

  return { items, show, success, error }
})
