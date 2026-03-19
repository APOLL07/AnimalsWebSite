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
        <a href="#catalog" class="hero__cta">{{ t('home.heroCta') }}</a>
      </div>
    </section>

    <!-- Catalog section -->
    <section id="catalog" class="catalog-section">
      <div class="catalog-section__container">
        <h2 class="catalog-section__title">{{ t('home.catalogTitle') }}</h2>

        <!-- Animal filter pills -->
        <div class="animal-pills">
          <button
            :class="['animal-pill', { active: !selectedAnimal }]"
            @click="selectedAnimal = ''"
          >
            {{ t('home.all') }}
          </button>
          <button
            v-for="a in animals"
            :key="a.slug"
            :class="['animal-pill', { active: selectedAnimal === a.slug }]"
            @click="selectedAnimal = a.slug"
          >
            {{ a.name }}
          </button>
        </div>

        <!-- Products grid -->
        <div v-if="loading" class="products-grid">
          <div v-for="i in 8" :key="i" class="product-card product-card--skeleton">
            <div class="skeleton skeleton--image"></div>
            <div class="skeleton skeleton--text"></div>
            <div class="skeleton skeleton--text-short"></div>
          </div>
        </div>

        <div v-else-if="products.length" class="products-grid">
          <article v-for="product in products" :key="product.id" class="product-card">
            <RouterLink :to="`/product/${product.slug}`" class="product-card__link">
              <div class="product-card__image-wrap">
                <img
                  v-if="product.images?.length"
                  :src="product.images[0].url"
                  :alt="product.name"
                  loading="lazy"
                  class="product-card__image"
                />
                <div v-else class="product-card__no-image">
                  <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1">
                    <rect x="3" y="3" width="18" height="18" rx="2" />
                    <circle cx="8.5" cy="8.5" r="1.5" />
                    <path d="m21 15-5-5L5 21" />
                  </svg>
                </div>
              </div>
              <div class="product-card__body">
                <p class="product-card__brand">{{ product.brand }}</p>
                <h3 class="product-card__name">{{ product.name }}</h3>
              </div>
            </RouterLink>
          </article>
        </div>

        <div v-else class="catalog-section__empty">
          <p>{{ t('home.productsNotFound') }}</p>
        </div>

        <div v-if="totalPages > 1" class="pagination">
          <button class="pagination__btn" :disabled="page <= 1" @click="page--; loadProducts()">
            &larr; {{ t('pagination.prev') }}
          </button>
          <span class="pagination__info">{{ page }} / {{ totalPages }}</span>
          <button class="pagination__btn" :disabled="page >= totalPages" @click="page++; loadProducts()">
            {{ t('pagination.next') }} &rarr;
          </button>
        </div>

        <div class="catalog-section__more">
          <RouterLink to="/catalog" class="btn btn--primary">{{ t('home.goToCatalog') }}</RouterLink>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { RouterLink } from 'vue-router'
import { api } from '../api/client'
import { useI18n } from '../i18n/index.js'

const { t } = useI18n()

const animals = ref([])
const products = ref([])
const loading = ref(true)
const total = ref(0)
const page = ref(1)
const selectedAnimal = ref('')
const pageSize = 12
const totalPages = computed(() => Math.ceil(total.value / pageSize))

async function loadProducts() {
  loading.value = true
  try {
    const params = { page: page.value, page_size: pageSize, sort_by: 'created_at', sort_order: 'desc' }
    if (selectedAnimal.value) params.animal_slug = selectedAnimal.value
    const data = await api.getProducts(params)
    products.value = data.items
    total.value = data.total
  } catch {
    products.value = []
  } finally {
    loading.value = false
  }
}

watch(selectedAnimal, () => {
  page.value = 1
  loadProducts()
})

onMounted(async () => {
  try {
    animals.value = await api.getAnimals()
  } catch {}
  loadProducts()
})
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

/* Catalog section */
.catalog-section {
  padding: 3rem 1rem;
}

.catalog-section__container {
  max-width: 1280px;
  margin: 0 auto;
}

.catalog-section__title {
  text-align: center;
  margin-bottom: 1.5rem;
  font-size: 1.75rem;
  color: var(--color-text);
}

.animal-pills {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  justify-content: center;
  margin-bottom: 2rem;
}

.animal-pill {
  padding: 0.5rem 1.25rem;
  border: 1px solid var(--color-border);
  border-radius: 24px;
  background: white;
  font-size: 0.875rem;
  cursor: pointer;
  transition: all 0.15s;
  font-family: inherit;
}

.animal-pill:hover { background: var(--color-bg-hover); }
.animal-pill.active {
  background: var(--color-primary);
  color: white;
  border-color: var(--color-primary);
}

.products-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.product-card {
  border: 1px solid var(--color-border);
  border-radius: 12px;
  overflow: hidden;
  background: var(--color-bg-card);
  transition: box-shadow 0.2s, transform 0.2s;
}

.product-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.08);
}

.product-card__link { text-decoration: none; color: inherit; display: block; }

.product-card__image-wrap {
  aspect-ratio: 1;
  overflow: hidden;
  background: #f5f5f5;
  display: flex;
  align-items: center;
  justify-content: center;
}

.product-card__image { width: 100%; height: 100%; object-fit: cover; }
.product-card__no-image { color: var(--color-border); }
.product-card__body { padding: 1rem; }

.product-card__brand {
  font-size: 0.75rem;
  color: var(--color-text-secondary);
  text-transform: uppercase;
  letter-spacing: 0.05em;
  margin-bottom: 0.25rem;
}

.product-card__name {
  font-size: 0.9375rem;
  font-weight: 600;
  line-height: 1.3;
}

.product-card--skeleton { pointer-events: none; }

.skeleton {
  background: linear-gradient(90deg, #f0f0f0 25%, #e0e0e0 50%, #f0f0f0 75%);
  background-size: 200% 100%;
  animation: shimmer 1.5s infinite;
  border-radius: 4px;
}

.skeleton--image { aspect-ratio: 1; }
.skeleton--text { height: 1rem; margin: 1rem; width: 80%; }
.skeleton--text-short { height: 0.75rem; margin: 0 1rem 1rem; width: 50%; }

@keyframes shimmer {
  0% { background-position: -200% 0; }
  100% { background-position: 200% 0; }
}

.catalog-section__empty {
  text-align: center;
  padding: 3rem 1rem;
  color: var(--color-text-secondary);
  font-size: 1.125rem;
}

.catalog-section__more {
  text-align: center;
  margin-top: 1rem;
}

.pagination {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 1rem;
  margin-top: 1rem;
}

.pagination__btn {
  padding: 0.5rem 1rem;
  border: 1px solid var(--color-border);
  border-radius: 8px;
  background: white;
  cursor: pointer;
  font-size: 0.875rem;
  font-family: inherit;
}

.pagination__btn:hover:not(:disabled) { background: var(--color-bg-hover); }
.pagination__btn:disabled { opacity: 0.4; cursor: not-allowed; }
.pagination__info { font-size: 0.875rem; color: var(--color-text-secondary); }

.btn {
  display: inline-flex;
  align-items: center;
  padding: 0.625rem 1.5rem;
  border: 1px solid var(--color-border);
  border-radius: 8px;
  background: white;
  font-size: 0.9375rem;
  cursor: pointer;
  text-decoration: none;
  font-family: inherit;
}

.btn--primary {
  background: var(--color-primary);
  color: white;
  border-color: var(--color-primary);
}

.btn--primary:hover { background: var(--color-primary-dark); }
</style>
