<template>
  <footer class="footer">
    <div class="footer__phones">
      <div class="footer__container">
        <span class="footer__order-label">{{ t('footer.orderBy') }}</span>
        <a href="tel:+380991900846" class="footer__phone">+38 (099) 190-08-46</a>
        <a href="tel:+380991900684" class="footer__phone">+38 (099) 190-06-84</a>
      </div>
    </div>
    <div class="footer__bottom">
      <div class="footer__container">
        <p class="footer__text">&copy; {{ year }} fashionAnimals. {{ t('footer.rights') }}</p>
      </div>
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
  margin-top: auto;
}

.footer__phones {
  padding: 1.25rem 1rem;
  background: var(--color-bg-secondary, #f8f8f8);
  border-bottom: 1px solid var(--color-border);
}

.footer__container {
  max-width: 1280px;
  margin: 0 auto;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-wrap: wrap;
  gap: 0.5rem 1rem;
}

.footer__order-label {
  color: var(--color-text-secondary);
  font-size: 0.875rem;
  font-weight: 500;
}

.footer__phone {
  color: var(--color-primary);
  font-size: 0.9375rem;
  font-weight: 600;
  text-decoration: none;
  transition: opacity 0.15s;
}

.footer__phone:hover {
  opacity: 0.75;
}

.footer__bottom {
  padding: 1.5rem 1rem;
}

.footer__text {
  color: var(--color-text-secondary);
  font-size: 0.875rem;
  text-align: center;
}
</style>
