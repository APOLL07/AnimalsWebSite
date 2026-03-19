<template>
  <div class="catalog">
    <div class="catalog__container">
      <!-- Mobile filter toggle -->
      <button class="catalog__filter-toggle" @click="filtersOpen = !filtersOpen">
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <line x1="4" y1="6" x2="20" y2="6" /><line x1="4" y1="12" x2="16" y2="12" /><line x1="4" y1="18" x2="12" y2="18" />
        </svg>
        {{ t('catalog.filters') }}
      </button>

      <!-- Sidebar filters -->
      <aside :class="['catalog__sidebar', { 'catalog__sidebar--open': filtersOpen }]">
        <div class="sidebar__header">
          <h2 class="sidebar__title">{{ t('catalog.filters') }}</h2>
          <button class="sidebar__close" @click="filtersOpen = false">&times;</button>
        </div>

        <div class="filter-group">
          <h3 class="filter-group__title">{{ t('catalog.animal') }}</h3>
          <ul class="filter-list">
            <li v-for="a in animals" :key="a.slug">
              <RouterLink
                :to="selectedAnimal === a.slug ? '/catalog' : `/catalog/${a.slug}`"
                :class="['filter-link', { active: selectedAnimal === a.slug }]"
                @click="filtersOpen = false"
              >
                {{ a.name }}
              </RouterLink>
            </li>
          </ul>
        </div>

        <div class="filter-group">
          <h3 class="filter-group__title">{{ t('catalog.category') }}</h3>
          <ul class="filter-list">
            <template v-for="cat in categories" :key="cat.id">
              <li>
                <button
                  :class="['filter-link filter-link--parent', { active: selectedCategory === cat.slug }]"
                  @click="toggleCategory(cat.slug); filtersOpen = false"
                >
                  {{ cat.name }}
                </button>
              </li>
              <li v-for="child in cat.children" :key="child.id" class="filter-child">
                <button
                  :class="['filter-link', { active: selectedCategory === child.slug }]"
                  @click="toggleCategory(child.slug); filtersOpen = false"
                >
                  {{ child.name }}
                </button>
              </li>
            </template>
          </ul>
        </div>

        <!-- Admin: Manage animals/categories -->
        <div v-if="auth.isLoggedIn" class="sidebar__admin">
          <button class="btn btn--sm" @click="showAnimalManager = true">{{ t('catalog.manageAnimals') }}</button>
          <button class="btn btn--sm" @click="showCategoryManager = true">{{ t('catalog.manageCategories') }}</button>
        </div>
      </aside>

      <!-- Sidebar overlay on mobile -->
      <div v-if="filtersOpen" class="catalog__sidebar-overlay" @click="filtersOpen = false"></div>

      <!-- Main content -->
      <div class="catalog__main">
        <div class="catalog__header">
          <h1 class="catalog__title">{{ pageTitle }}</h1>
          <div class="catalog__sort">
            <select v-model="sortValue" @change="loadProducts" class="sort-select" :aria-label="t('catalog.sorting')">
              <option value="created_at:desc">{{ t('catalog.sortNewest') }}</option>
              <option value="created_at:asc">{{ t('catalog.sortOldest') }}</option>
              <option value="name:asc">{{ t('catalog.sortNameAsc') }}</option>
              <option value="name:desc">{{ t('catalog.sortNameDesc') }}</option>
            </select>
          </div>
        </div>

        <!-- Admin: add product button -->
        <button v-if="auth.isLoggedIn" class="btn btn--primary catalog__add-btn" @click="showProductForm = true">
          {{ t('catalog.addProduct') }}
        </button>

        <!-- Loading skeleton -->
        <div v-if="loading" class="products-grid">
          <div v-for="i in 8" :key="i" class="product-card product-card--skeleton">
            <div class="skeleton skeleton--image"></div>
            <div class="skeleton skeleton--text"></div>
            <div class="skeleton skeleton--text-short"></div>
          </div>
        </div>

        <!-- Products grid -->
        <div v-else-if="products.length" class="products-grid">
          <article v-for="product in products" :key="product.id" class="product-card">
            <RouterLink :to="`/product/${product.slug}`" class="product-card__link">
              <div class="product-card__image-wrap">
                <img
                  v-if="product.images && product.images.length"
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
                <div class="product-card__attrs">
                  <span
                    v-for="attr in (product.attributes || []).filter(a => a.is_main).slice(0, 2)"
                    :key="attr.id"
                    class="product-card__attr"
                  >
                    {{ attr.key }}: {{ attr.value }}
                  </span>
                </div>
              </div>
            </RouterLink>
            <div v-if="auth.isLoggedIn" class="product-card__admin">
              <button class="btn btn--sm" @click="editProduct(product)">{{ t('common.edit') }}</button>
              <button class="btn btn--sm btn--danger" @click="confirmDelete(product)">{{ t('common.delete') }}</button>
            </div>
          </article>
        </div>

        <!-- Empty state -->
        <div v-else class="catalog__empty">
          <p>{{ t('catalog.productsNotFound') }}</p>
          <RouterLink to="/catalog" class="btn btn--primary">{{ t('catalog.resetFilters') }}</RouterLink>
        </div>

        <!-- Pagination -->
        <div v-if="totalPages > 1" class="pagination">
          <button class="pagination__btn" :disabled="currentPage <= 1" @click="goToPage(currentPage - 1)">
            &larr; {{ t('pagination.prev') }}
          </button>
          <span class="pagination__info">{{ currentPage }} / {{ totalPages }}</span>
          <button class="pagination__btn" :disabled="currentPage >= totalPages" @click="goToPage(currentPage + 1)">
            {{ t('pagination.next') }} &rarr;
          </button>
        </div>
      </div>
    </div>

    <!-- Product Form Modal -->
    <ProductFormModal
      v-if="showProductForm"
      :product="editingProduct"
      :animals="animals"
      :categories="allCategories"
      @close="showProductForm = false; editingProduct = null"
      @saved="onProductSaved"
    />

    <!-- Delete confirmation -->
    <div v-if="deletingProduct" class="modal-overlay" @click.self="deletingProduct = null">
      <div class="modal">
        <h3>{{ t('common.delete') }} &laquo;{{ deletingProduct.name }}&raquo;?</h3>
        <p>{{ t('common.cannotUndo') }}</p>
        <div class="modal__actions">
          <button class="btn" @click="deletingProduct = null">{{ t('common.cancel') }}</button>
          <button class="btn btn--danger" @click="doDelete">{{ t('common.delete') }}</button>
        </div>
      </div>
    </div>

    <!-- Animal Manager Modal -->
    <EntityManager
      v-if="showAnimalManager"
      :title="t('catalog.manageAnimals')"
      :items="animals"
      :fields="['name']"
      :placeholders="{ name: t('entityManager.namePlaceholder') }"
      @close="showAnimalManager = false"
      @create="onCreateAnimal"
      @update="onUpdateAnimal"
      @delete="onDeleteAnimal"
    />

    <!-- Category Manager Modal -->
    <CategoryManager
      v-if="showCategoryManager"
      :categories="categories"
      @close="showCategoryManager = false"
      @refresh="refreshMeta"
    />
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted } from 'vue'
import { useRoute, useRouter, RouterLink } from 'vue-router'
import { api } from '../api/client'
import { useAuthStore } from '../stores/auth'
import { useNotifications } from '../stores/notifications'
import { useI18n } from '../i18n/index.js'
import ProductFormModal from '../components/ProductFormModal.vue'
import EntityManager from '../components/EntityManager.vue'
import CategoryManager from '../components/CategoryManager.vue'

const { t } = useI18n()
const route = useRoute()
const router = useRouter()
const auth = useAuthStore()
const notify = useNotifications()

const animals = ref([])
const categories = ref([])
const allCategories = ref([])
const products = ref([])
const loading = ref(true)
const total = ref(0)
const currentPage = ref(1)
const pageSize = 20
const sortValue = ref('created_at:desc')
const filtersOpen = ref(false)

const showProductForm = ref(false)
const editingProduct = ref(null)
const deletingProduct = ref(null)
const showAnimalManager = ref(false)
const showCategoryManager = ref(false)

const selectedAnimal = computed(() => route.params.animalSlug || '')
const selectedCategory = computed(() => route.query.category || '')
const totalPages = computed(() => Math.ceil(total.value / pageSize))

const pageTitle = computed(() => {
  if (selectedAnimal.value) {
    const a = animals.value.find((x) => x.slug === selectedAnimal.value)
    return a ? `${t('catalog.productsPrefix')} ${a.name}` : t('catalog.title')
  }
  return t('catalog.title')
})

function toggleCategory(slug) {
  const query = { ...route.query }
  if (query.category === slug) {
    delete query.category
  } else {
    query.category = slug
  }
  query.page = '1'
  router.push({ path: route.path, query })
}

async function loadProducts() {
  loading.value = true
  try {
    const [sortBy, sortOrder] = sortValue.value.split(':')
    const params = {
      page: currentPage.value,
      page_size: pageSize,
      sort_by: sortBy,
      sort_order: sortOrder,
    }
    if (selectedAnimal.value) params.animal_slug = selectedAnimal.value
    if (selectedCategory.value) params.category_slug = selectedCategory.value

    const data = await api.getProducts(params)
    products.value = data.items
    total.value = data.total
  } catch {
    notify.error(t('notify.loadError'))
  } finally {
    loading.value = false
  }
}

function goToPage(page) {
  router.push({ path: route.path, query: { ...route.query, page: String(page) } })
}

function editProduct(product) {
  editingProduct.value = product
  showProductForm.value = true
}

function confirmDelete(product) {
  deletingProduct.value = product
}

async function doDelete() {
  try {
    await api.deleteProduct(deletingProduct.value.id)
    notify.success(t('notify.productDeleted'))
    deletingProduct.value = null
    loadProducts()
  } catch {
    notify.error(t('notify.deleteError'))
  }
}

function onProductSaved() {
  showProductForm.value = false
  editingProduct.value = null
  loadProducts()
}

// Animal management
async function onCreateAnimal(data) {
  await api.createAnimal(data)
  notify.success(t('notify.animalAdded'))
  refreshMeta()
}

async function onUpdateAnimal(id, data) {
  await api.updateAnimal(id, data)
  notify.success(t('notify.animalUpdated'))
  refreshMeta()
}

async function onDeleteAnimal(id) {
  await api.deleteAnimal(id)
  notify.success(t('notify.animalDeleted'))
  refreshMeta()
}

async function refreshMeta() {
  const [animalsData, categoriesData] = await Promise.all([
    api.getAnimals(),
    api.getCategories(),
  ])
  animals.value = animalsData
  categories.value = categoriesData
  allCategories.value = categoriesData.flatMap((c) => [
    { id: c.id, slug: c.slug, name: c.name },
    ...(c.children || []).map((ch) => ({ id: ch.id, slug: ch.slug, name: `— ${ch.name}` })),
  ])
}

watch(
  () => [route.params.animalSlug, route.query.category, route.query.page],
  () => {
    currentPage.value = parseInt(route.query.page) || 1
    loadProducts()
  }
)

onMounted(async () => {
  await refreshMeta()
  currentPage.value = parseInt(route.query.page) || 1
  loadProducts()
})
</script>

<style scoped>
.catalog__container {
  max-width: 1280px;
  margin: 0 auto;
  padding: 2rem 1rem;
  display: flex;
  gap: 2rem;
  position: relative;
}

/* Mobile filter toggle */
.catalog__filter-toggle {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  position: fixed;
  bottom: 1rem;
  left: 50%;
  transform: translateX(-50%);
  z-index: 90;
  padding: 0.75rem 1.5rem;
  background: var(--color-primary);
  color: white;
  border: none;
  border-radius: 24px;
  font-size: 0.9375rem;
  font-family: inherit;
  cursor: pointer;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.2);
}

@media (min-width: 788px) {
  .catalog__filter-toggle { display: none; }
}

/* Sidebar */
.catalog__sidebar {
  width: 240px;
  flex-shrink: 0;
  display: none;
}

@media (min-width: 788px) {
  .catalog__sidebar { display: block; }
}

/* Mobile sidebar slide-in */
@media (max-width: 787px) {
  .catalog__sidebar {
    position: fixed;
    top: 0;
    left: 0;
    width: 280px;
    height: 100vh;
    background: var(--color-bg);
    z-index: 200;
    padding: 1rem;
    overflow-y: auto;
    transform: translateX(-100%);
    transition: transform 0.25s ease;
    box-shadow: 4px 0 16px rgba(0, 0, 0, 0.1);
  }
  .catalog__sidebar--open {
    display: block;
    transform: translateX(0);
  }
}

.catalog__sidebar-overlay {
  display: none;
}

@media (max-width: 787px) {
  .catalog__sidebar-overlay {
    display: block;
    position: fixed;
    inset: 0;
    background: rgba(0, 0, 0, 0.4);
    z-index: 199;
  }
}

.sidebar__header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
}

.sidebar__title {
  font-size: 1.125rem;
}

.sidebar__close {
  display: none;
  background: none;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
  color: var(--color-text-secondary);
  width: 36px;
  height: 36px;
  align-items: center;
  justify-content: center;
  border-radius: 8px;
}

@media (max-width: 787px) {
  .sidebar__close { display: flex; }
}

.sidebar__close:hover { background: var(--color-bg-hover); }

.filter-group { margin-bottom: 1.5rem; }

.filter-group__title {
  font-size: 0.875rem;
  text-transform: uppercase;
  color: var(--color-text-secondary);
  margin-bottom: 0.5rem;
  letter-spacing: 0.05em;
}

.filter-list { list-style: none; }

.filter-link {
  display: block;
  width: 100%;
  text-align: left;
  padding: 0.375rem 0.75rem;
  border: none;
  background: none;
  color: var(--color-text);
  font-size: 0.875rem;
  border-radius: 6px;
  cursor: pointer;
  transition: background 0.15s, color 0.15s;
  text-decoration: none;
  font-family: inherit;
}

.filter-link--parent {
  font-weight: 700;
}

.filter-link:hover { background: var(--color-bg-hover); }
.filter-link.active { background: var(--color-primary); color: white; }
.filter-child { padding-left: 0.75rem; }

.sidebar__admin {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  margin-top: 1rem;
  padding-top: 1rem;
  border-top: 1px solid var(--color-border);
}

/* Main */
.catalog__main { flex: 1; min-width: 0; }

.catalog__header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 1.5rem;
  flex-wrap: wrap;
  gap: 1rem;
}

.catalog__title { font-size: 1.5rem; }

.catalog__sort {
  flex-shrink: 1;
  min-width: 0;
}

.sort-select {
  padding: 0.5rem 0.75rem;
  border: 1px solid var(--color-border);
  border-radius: 8px;
  font-size: 0.875rem;
  background: white;
  font-family: inherit;
  width: 100%;
  max-width: 220px;
  min-width: 0;
  box-sizing: border-box;
}

@media (max-width: 475px) {
  .catalog__header {
    flex-direction: column;
    align-items: stretch;
  }
  .catalog__sort {
    width: 100%;
  }
  .sort-select {
    max-width: 100%;
  }
}

.catalog__add-btn { margin-bottom: 1rem; }

.products-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
  gap: 1.5rem;
}

@media (max-width: 480px) {
  .products-grid { grid-template-columns: repeat(2, 1fr); gap: 0.75rem; }
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
.product-card__body { padding: 0.75rem; }

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
  margin-bottom: 0.5rem;
  line-height: 1.3;
}

.product-card__attrs { display: flex; flex-wrap: wrap; gap: 0.375rem; }

.product-card__attr {
  font-size: 0.75rem;
  padding: 0.125rem 0.5rem;
  background: var(--color-bg-hover);
  border-radius: 4px;
  color: var(--color-text-secondary);
}

.product-card__admin {
  padding: 0.75rem;
  border-top: 1px solid var(--color-border);
  display: flex;
  gap: 0.5rem;
}

.product-card--skeleton { pointer-events: none; }

.skeleton {
  background: linear-gradient(90deg, #f0f0f0 25%, #e0e0e0 50%, #f0f0f0 75%);
  background-size: 200% 100%;
  animation: shimmer 1.5s infinite;
  border-radius: 4px;
}

.skeleton--image { aspect-ratio: 1; }
.skeleton--text { height: 1rem; margin: 1rem 0.75rem; width: 80%; }
.skeleton--text-short { height: 0.75rem; margin: 0 0.75rem 0.75rem; width: 50%; }

@keyframes shimmer {
  0% { background-position: -200% 0; }
  100% { background-position: 200% 0; }
}

.catalog__empty {
  text-align: center;
  padding: 4rem 1rem;
  color: var(--color-text-secondary);
}

.catalog__empty p { margin-bottom: 1rem; font-size: 1.125rem; }

.pagination {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 1rem;
  margin-top: 2rem;
  padding: 1rem 0;
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

/* Shared buttons */
.btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 0.5rem 1rem;
  border: 1px solid var(--color-border);
  border-radius: 8px;
  background: white;
  font-size: 0.875rem;
  cursor: pointer;
  transition: background 0.15s;
  min-height: 36px;
  font-family: inherit;
}

.btn:hover { background: var(--color-bg-hover); }

.btn--primary {
  background: var(--color-primary);
  color: white;
  border-color: var(--color-primary);
}

.btn--primary:hover { background: var(--color-primary-dark); }

.btn--danger { color: var(--color-error); border-color: var(--color-error); }
.btn--danger:hover { background: #fef2f2; }

.btn--sm { padding: 0.25rem 0.75rem; font-size: 0.8125rem; min-height: 28px; }

/* Modal */
.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 200;
  padding: 1rem;
}

.modal {
  background: white;
  border-radius: 12px;
  padding: 2rem;
  max-width: 440px;
  width: 100%;
}

.modal h3 { margin-bottom: 0.5rem; }
.modal p { color: var(--color-text-secondary); margin-bottom: 1.5rem; }
.modal__actions { display: flex; gap: 0.75rem; justify-content: flex-end; }
</style>
