<template>
  <div class="home">
    <!-- Hero with video -->
    <section class="hero">
      <video
        class="hero__video"
        autoplay
        muted
        loop
        playsinline
        poster=""
      >
        <source src="/hero-video.mp4" type="video/mp4" />
      </video>
      <div class="hero__overlay">
        <h1 class="hero__title">fashion<strong>Animals</strong></h1>
        <p class="hero__subtitle">{{ t('home.heroSubtitle') }}</p>
        <RouterLink to="/catalog" class="hero__cta">{{ t('home.heroCta') }}</RouterLink>
      </div>
    </section>
  </div>
</template>

<script setup>
import { RouterLink } from 'vue-router'
import { useI18n } from '../i18n/index.js'

const { t } = useI18n()
</script>

<style scoped>
/* Hero */
.hero {
  position: relative;
  min-height: 80vh;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
  background: #1a1a2e;
}

.hero__video {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
  opacity: 0.6;
}

.hero__overlay {
  position: relative;
  z-index: 1;
  text-align: center;
  color: white;
  padding: 2rem;
}

.hero__title {
  font-size: clamp(2rem, 5vw, 4rem);
  margin-bottom: 0.5rem;
  text-shadow: 0 2px 8px rgba(0,0,0,0.3);
}

.hero__subtitle {
  font-size: clamp(1rem, 2.5vw, 1.5rem);
  opacity: 0.9;
  margin-bottom: 2rem;
}

.hero__cta {
  display: inline-block;
  padding: 1rem 2.5rem;
  background: white;
  color: #667eea;
  text-decoration: none;
  border-radius: 8px;
  font-weight: 600;
  font-size: 1.125rem;
  transition: transform 0.2s, box-shadow 0.2s;
}

.hero__cta:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
}

@media (max-width: 768px) {
  .hero { min-height: 60vh; }
}
</style>
