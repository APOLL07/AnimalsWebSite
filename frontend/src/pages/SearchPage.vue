<template>
  <div class="search-page">
    <div class="search-page__container">
      <h1 class="search-page__title">{{ t('search.title') }}</h1>

      <div class="search-form-wrap">
        <form class="search-form" @submit.prevent="doSearch">
          <input
            v-model="query"
            type="search"
            class="search-form__input"
            :placeholder="t('search.placeholder')"
            autofocus
            @input="onInput"
          />
          <button type="submit" class="search-form__btn">{{ t('search.submit') }}</button>
        </form>

        <!-- Autocomplete suggestions -->
        <div v-if="suggestions.length && !searched" class="search-suggestions">
          <RouterLink
            v-for="item in suggestions"
            :key="item.id"
            :to="`/product/${item.slug}`"
            class="search-suggestion"
          >
            <img
              v-if="item.images?.length"
              :src="item.images[0].url"
              :alt="item.name"
              class="search-suggestion__img"
            />
            <div v-else class="search-suggestion__img search-suggestion__img--empty"></div>
            <div class="search-suggestion__info">
              <span class="search-suggestion__brand">{{ item.brand }}</span>
              <span class="search-suggestion__name">{{ item.name }}</span>
            </div>
          </RouterLink>
        </div>
      </div>

      <div v-if="loading" class="search-results">
        <div v-for="i in 4" :key="i" class="skeleton" style="height:5rem; margin-bottom:1rem; border-radius:8px"></div>
      </div>

      <div v-else-if="searched && results.length" class="search-results">
        <p class="search-results__count">{{ t('search.found') }} {{ total }}</p>
        <article v-for="product in results" :key="product.id" class="search-item">
          <RouterLink :to="`/product/${product.slug}`" class="search-item__link">
            <div class="search-item__image">
              <img
                v-if="product.images && product.images.length"
                :src="product.images[0].url"
                :alt="product.name"
              />
              <div v-else class="search-item__no-image">
                <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1">
                  <rect x="3" y="3" width="18" height="18" rx="2" />
                </svg>
              </div>
            </div>
            <div class="search-item__info">
              <p class="search-item__brand">{{ product.brand }}</p>
              <h3 class="search-item__name">{{ product.name }}</h3>
              <p v-if="product.description" class="search-item__desc">
                {{ product.description.slice(0, 120) }}{{ product.description.length > 120 ? '...' : '' }}
              </p>
            </div>
          </RouterLink>
        </article>

        <!-- Pagination -->
        <div v-if="totalPages > 1" class="pagination">
          <button class="pagination__btn" :disabled="page <= 1" @click="goToPage(page - 1)">
            &larr; {{ t('pagination.prev') }}
          </button>
          <span class="pagination__info">{{ page }} / {{ totalPages }}</span>
          <button class="pagination__btn" :disabled="page >= totalPages" @click="goToPage(page + 1)">
            {{ t('pagination.next') }} &rarr;
          </button>
        </div>
      </div>

      <div v-else-if="searched" class="search-page__empty">
        <p>{{ t('search.notFound') }} &laquo;{{ searchedQuery }}&raquo;</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useRoute, useRouter, RouterLink } from 'vue-router'
import { api } from '../api/client'
import { useI18n } from '../i18n/index.js'

const { t } = useI18n()
const route = useRoute()
const router = useRouter()

const query = ref('')
const results = ref([])
const total = ref(0)
const page = ref(1)
const loading = ref(false)
const searched = ref(false)
const searchedQuery = ref('')
const suggestions = ref([])
const pageSize = 20
const totalPages = computed(() => Math.ceil(total.value / pageSize))

let debounceTimer = null

function onInput() {
  clearTimeout(debounceTimer)
  suggestions.value = []
  searched.value = false
  const q = query.value.trim()
  if (!q) return
  debounceTimer = setTimeout(async () => {
    try {
      suggestions.value = await api.searchSuggest(q)
    } catch {
      suggestions.value = []
    }
  }, 250)
}

async function doSearch() {
  if (!query.value.trim()) return
  suggestions.value = []
  router.push({ path: '/search', query: { q: query.value.trim(), page: '1' } })
}

async function fetchResults() {
  const q = route.query.q
  if (!q) return

  loading.value = true
  searched.value = true
  searchedQuery.value = q
  query.value = q
  suggestions.value = []

  try {
    const data = await api.search({
      q,
      page: page.value,
      page_size: pageSize,
    })
    results.value = data.items
    total.value = data.total
  } catch {
    results.value = []
  } finally {
    loading.value = false
  }
}

function goToPage(p) {
  router.push({ path: '/search', query: { q: route.query.q, page: String(p) } })
}

watch(
  () => [route.query.q, route.query.page],
  () => {
    page.value = parseInt(route.query.page) || 1
    fetchResults()
  }
)

onMounted(() => {
  if (route.query.q) {
    page.value = parseInt(route.query.page) || 1
    query.value = route.query.q
    fetchResults()
  }
})
</script>

<style scoped>
.search-page__container {
  max-width: 800px;
  margin: 0 auto;
  padding: 2rem 1rem;
}

.search-page__title {
  font-size: 1.75rem;
  margin-bottom: 1.5rem;
}

.search-form-wrap {
  position: relative;
  margin-bottom: 2rem;
}

.search-form {
  display: flex;
  gap: 0.75rem;
}

.search-form__input {
  flex: 1;
  padding: 0.75rem 1rem;
  border: 1px solid var(--color-border);
  border-radius: 8px;
  font-size: 1rem;
  font-family: inherit;
  outline: none;
  transition: border-color 0.15s;
}

.search-form__input:focus {
  border-color: var(--color-primary);
}

.search-form__btn {
  padding: 0.75rem 1.5rem;
  background: var(--color-primary);
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 1rem;
  cursor: pointer;
  font-family: inherit;
  transition: background 0.15s;
}

.search-form__btn:hover {
  background: var(--color-primary-dark);
}

/* Autocomplete suggestions */
.search-suggestions {
  position: absolute;
  top: 100%;
  left: 0;
  right: 0;
  background: white;
  border: 1px solid var(--color-border);
  border-radius: 8px;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.1);
  margin-top: 0.25rem;
  overflow: hidden;
  z-index: 50;
}

.search-suggestion {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.75rem 1rem;
  text-decoration: none;
  color: inherit;
  transition: background 0.1s;
}

.search-suggestion:hover {
  background: var(--color-bg-hover);
}

.search-suggestion:not(:last-child) {
  border-bottom: 1px solid var(--color-border);
}

.search-suggestion__img {
  width: 48px;
  height: 48px;
  border-radius: 6px;
  object-fit: cover;
  flex-shrink: 0;
}

.search-suggestion__img--empty {
  background: #f0f0f0;
}

.search-suggestion__info {
  display: flex;
  flex-direction: column;
  min-width: 0;
}

.search-suggestion__brand {
  font-size: 0.6875rem;
  color: var(--color-text-secondary);
  text-transform: uppercase;
  letter-spacing: 0.04em;
}

.search-suggestion__name {
  font-size: 0.9375rem;
  font-weight: 500;
}

/* Results */
.search-results__count {
  color: var(--color-text-secondary);
  margin-bottom: 1rem;
  font-size: 0.875rem;
}

.search-item {
  border: 1px solid var(--color-border);
  border-radius: 12px;
  overflow: hidden;
  margin-bottom: 1rem;
  transition: box-shadow 0.2s;
}

.search-item:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.06);
}

.search-item__link {
  display: flex;
  text-decoration: none;
  color: inherit;
}

.search-item__image {
  width: 120px;
  height: 120px;
  flex-shrink: 0;
  background: #f5f5f5;
  display: flex;
  align-items: center;
  justify-content: center;
}

@media (max-width: 480px) {
  .search-item__image { width: 80px; height: 80px; }
}

.search-item__image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.search-item__no-image { color: var(--color-border); }

.search-item__info {
  padding: 1rem;
  flex: 1;
  min-width: 0;
}

.search-item__brand {
  font-size: 0.75rem;
  color: var(--color-text-secondary);
  text-transform: uppercase;
  letter-spacing: 0.05em;
  margin-bottom: 0.125rem;
}

.search-item__name {
  font-size: 1rem;
  font-weight: 600;
  margin-bottom: 0.375rem;
}

.search-item__desc {
  font-size: 0.8125rem;
  color: var(--color-text-secondary);
  line-height: 1.5;
}

.search-page__empty {
  text-align: center;
  padding: 3rem 1rem;
  color: var(--color-text-secondary);
  font-size: 1.125rem;
}

.skeleton {
  background: linear-gradient(90deg, #f0f0f0 25%, #e0e0e0 50%, #f0f0f0 75%);
  background-size: 200% 100%;
  animation: shimmer 1.5s infinite;
}

@keyframes shimmer {
  0% { background-position: -200% 0; }
  100% { background-position: 200% 0; }
}

.pagination {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 1rem;
  margin-top: 1.5rem;
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
</style>
