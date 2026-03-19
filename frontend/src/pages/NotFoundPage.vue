<template>
  <div class="not-found">
    <div class="not-found__container">
      <h1 class="not-found__code">404</h1>
      <p class="not-found__text">{{ t('notFound.title') }}</p>
      <RouterLink to="/" class="not-found__link">{{ t('notFound.back') }}</RouterLink>
    </div>
  </div>
</template>

<script setup>
import { RouterLink } from 'vue-router'
import { useI18n } from '../i18n/index.js'

const { t } = useI18n()
</script>

<style scoped>
.not-found {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 60vh;
  text-align: center;
  padding: 2rem;
}

.not-found__code {
  font-size: 6rem;
  color: var(--color-text-secondary);
  line-height: 1;
  margin-bottom: 0.5rem;
}

.not-found__text {
  font-size: 1.25rem;
  color: var(--color-text-secondary);
  margin-bottom: 2rem;
}

.not-found__link {
  display: inline-block;
  padding: 0.75rem 2rem;
  background: var(--color-primary);
  color: white;
  text-decoration: none;
  border-radius: 8px;
  font-weight: 500;
  min-height: 44px;
  transition: opacity 0.2s;
}

.not-found__link:hover {
  opacity: 0.9;
}
</style>
