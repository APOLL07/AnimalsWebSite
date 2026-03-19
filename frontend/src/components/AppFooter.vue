<template>
  <footer class="footer">
    <div class="footer__container">
      <p class="footer__text">&copy; {{ year }} fashionAnimals. {{ t('footer.rights') }}</p>
    </div>
  </footer>
</template>

<script setup>
import { useI18n } from '../i18n/index.js'

const { t } = useI18n()
const year = new Date().getFullYear()
</script>

<style scoped>
.footer {
  border-top: 1px solid var(--color-border);
  padding: 2rem 1rem;
  margin-top: auto;
}

.footer__container {
  max-width: 1280px;
  margin: 0 auto;
  text-align: center;
}

.footer__text {
  color: var(--color-text-secondary);
  font-size: 0.875rem;
}
</style>
