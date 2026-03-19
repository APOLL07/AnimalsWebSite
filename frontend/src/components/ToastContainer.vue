<template>
  <Teleport to="body">
    <div class="toast-container" aria-live="polite">
      <TransitionGroup name="toast">
        <div
          v-for="item in notifications.items"
          :key="item.id"
          :class="['toast', `toast--${item.type}`]"
        >
          {{ item.message }}
        </div>
      </TransitionGroup>
    </div>
  </Teleport>
</template>

<script setup>
import { useNotifications } from '../stores/notifications'
const notifications = useNotifications()
</script>

<style scoped>
.toast-container {
  position: fixed;
  top: 80px;
  right: 1rem;
  z-index: 300;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  max-width: 360px;
}

.toast {
  padding: 0.75rem 1rem;
  border-radius: 8px;
  font-size: 0.875rem;
  color: white;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.toast--success { background: var(--color-success); }
.toast--error { background: var(--color-error); }

.toast-enter-active { transition: all 0.3s ease; }
.toast-leave-active { transition: all 0.3s ease; }
.toast-enter-from { opacity: 0; transform: translateX(1rem); }
.toast-leave-to { opacity: 0; transform: translateX(1rem); }
</style>
