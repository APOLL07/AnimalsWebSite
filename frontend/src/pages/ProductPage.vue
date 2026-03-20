<template>
  <div class="product-page">
    <!-- Loading -->
    <div v-if="loading" class="product-page__container">
      <div class="product-detail product-detail--skeleton">
        <div class="skeleton" style="aspect-ratio:1; max-width:500px"></div>
        <div>
          <div class="skeleton" style="height:2rem; width:60%; margin-bottom:1rem"></div>
          <div class="skeleton" style="height:1rem; width:40%; margin-bottom:2rem"></div>
          <div class="skeleton" style="height:6rem; width:100%"></div>
        </div>
      </div>
    </div>

    <!-- Product detail -->
    <div v-else-if="product" class="product-page__container">
      <!-- Breadcrumbs -->
      <nav class="breadcrumbs" :aria-label="t('product.nav')">
        <RouterLink to="/">{{ t('product.home') }}</RouterLink>
        <span class="breadcrumbs__sep">/</span>
        <RouterLink to="/catalog">{{ t('product.catalog') }}</RouterLink>
        <template v-if="product.animals.length">
          <span class="breadcrumbs__sep">/</span>
          <RouterLink :to="`/catalog/${product.animals[0].slug}`">{{ product.animals[0].name }}</RouterLink>
        </template>
        <span class="breadcrumbs__sep">/</span>
        <span>{{ product.name }}</span>
      </nav>

      <div class="product-detail">
        <!-- Gallery -->
        <div class="gallery">
          <div class="gallery__main">
            <video
              v-if="activeImage && activeImage.media_type === 'video'"
              :src="activeImage.url"
              controls
              class="gallery__image"
            ></video>
            <img
              v-else-if="activeImage"
              :src="activeImage.url"
              :alt="product.name"
              class="gallery__image"
            />
            <div v-else class="gallery__placeholder">
              <svg width="80" height="80" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1">
                <rect x="3" y="3" width="18" height="18" rx="2" />
                <circle cx="8.5" cy="8.5" r="1.5" />
                <path d="m21 15-5-5L5 21" />
              </svg>
            </div>
            <!-- Gallery arrows -->
            <template v-if="product.images.length > 1">
              <button class="gallery__arrow gallery__arrow--left" @click="prevImage" :aria-label="t('product.prevPhoto')">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
                  <polyline points="15 18 9 12 15 6" />
                </svg>
              </button>
              <button class="gallery__arrow gallery__arrow--right" @click="nextImage" :aria-label="t('product.nextPhoto')">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
                  <polyline points="9 6 15 12 9 18" />
                </svg>
              </button>
            </template>
          </div>
          <div v-if="product.images.length > 1" class="gallery__thumbs" ref="thumbsRef">
            <button
              v-for="(img, idx) in product.images"
              :key="img.id"
              :class="['gallery__thumb', {
                active: activeImage?.id === img.id,
                'gallery__thumb--dragging': dragSrcIdx === idx,
                'gallery__thumb--drag-over': dragOverIdx === idx && dragSrcIdx !== idx,
                'gallery__thumb--draggable': auth.isLoggedIn,
              }]"
              @click="setActive(img)"
              :data-id="img.id"
              :draggable="auth.isLoggedIn"
              @dragstart="onDragStart($event, idx)"
              @dragover="onDragOver($event, idx)"
              @drop="onDrop($event, idx)"
              @dragend="onDragEnd"
            >
              <div v-if="img.media_type === 'video'" class="gallery__thumb-video">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="white">
                  <polygon points="5 3 19 12 5 21" />
                </svg>
              </div>
              <img v-else :src="img.url" :alt="product.name" />
              <span v-if="auth.isLoggedIn && idx === 0" class="gallery__thumb-main-badge">★</span>
            </button>
          </div>

          <!-- Admin: media upload -->
          <div v-if="auth.isLoggedIn" class="gallery__admin">
            <label class="btn btn--sm">
              {{ t('product.uploadPhoto') }}
              <input type="file" accept="image/*" hidden @change="onUploadImage" />
            </label>
            <label class="btn btn--sm">
              {{ t('product.uploadVideo') }}
              <input type="file" accept="video/mp4,video/webm,video/quicktime" hidden @change="onUploadVideo" />
            </label>
            <button
              v-if="activeImage"
              class="btn btn--sm btn--danger"
              @click="onDeleteMedia"
            >
              {{ activeImage.media_type === 'video' ? t('product.deleteVideo') : t('product.deletePhoto') }}
            </button>
          </div>
        </div>

        <!-- Info -->
        <div class="product-info">
          <p v-if="product.brand" class="product-info__brand">{{ product.brand }}</p>
          <h1 class="product-info__name">{{ product.name }}</h1>

          <!-- Admin actions -->
          <div v-if="auth.isLoggedIn" class="product-info__admin">
            <button class="btn btn--sm" @click="openEditForm">{{ t('product.edit') }}</button>
            <button class="btn btn--sm btn--danger" @click="showDeleteConfirm = true">{{ t('product.delete') }}</button>
          </div>

          <!-- Main attributes -->
          <div v-if="mainAttrs.length" class="product-info__main-attrs">
            <div v-for="attr in mainAttrs" :key="attr.id" class="attr-row">
              <span class="attr-row__key">{{ attr.key }}</span>
              <span class="attr-row__value">{{ attr.value }}</span>
            </div>
          </div>

          <!-- Description -->
          <div v-if="product.description" class="product-info__desc">
            <h2>{{ t('product.description') }}</h2>
            <p>{{ product.description }}</p>
          </div>

          <!-- All attributes -->
          <div v-if="otherAttrs.length" class="product-info__attrs">
            <h2>{{ t('product.attributes') }}</h2>
            <table class="attrs-table">
              <tr v-for="attr in otherAttrs" :key="attr.id">
                <td class="attrs-table__key">{{ attr.key }}</td>
                <td>{{ attr.value }}</td>
              </tr>
            </table>
          </div>

          <!-- Categories / Animals -->
          <div class="product-info__tags">
            <RouterLink
              v-for="animal in product.animals"
              :key="animal.id"
              :to="`/catalog/${animal.slug}`"
              class="tag"
            >
              {{ animal.name }}
            </RouterLink>
            <RouterLink
              v-for="cat in product.categories"
              :key="cat.id"
              :to="`/catalog?category=${cat.slug}`"
              class="tag tag--category"
            >
              {{ cat.name }}
            </RouterLink>
          </div>
        </div>
      </div>
    </div>

    <!-- Not found -->
    <div v-else class="product-page__container product-page__not-found">
      <h1>{{ t('product.notFound') }}</h1>
      <RouterLink to="/catalog" class="btn btn--primary">{{ t('product.backToCatalog') }}</RouterLink>
    </div>

    <!-- Edit form modal -->
    <ProductFormModal
      v-if="showEditForm && editingProduct"
      :product="editingProduct"
      :animals="allAnimals"
      :categories="allCategories"
      @close="showEditForm = false; editingProduct = null"
      @saved="onSaved"
    />

    <!-- Delete confirm -->
    <div v-if="showDeleteConfirm" class="modal-overlay" @click.self="showDeleteConfirm = false">
      <div class="modal">
        <h3>{{ t('product.deleteConfirm') }}</h3>
        <p>{{ t('common.cannotUndo') }}</p>
        <div class="modal__actions">
          <button class="btn" @click="showDeleteConfirm = false">{{ t('common.cancel') }}</button>
          <button class="btn btn--danger" @click="onDelete">{{ t('common.delete') }}</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch, nextTick } from 'vue'
import { useRoute, useRouter, RouterLink } from 'vue-router'
import { api } from '../api/client'
import { useAuthStore } from '../stores/auth'
import { useNotifications } from '../stores/notifications'
import { useI18n } from '../i18n/index.js'
import ProductFormModal from '../components/ProductFormModal.vue'

const { t, locale } = useI18n()
const route = useRoute()
const router = useRouter()
const auth = useAuthStore()
const notify = useNotifications()

const product = ref(null)
const loading = ref(true)
const activeImage = ref(null)
const thumbsRef = ref(null)
const dragSrcIdx = ref(null)
const dragOverIdx = ref(null)
const showEditForm = ref(false)
const showDeleteConfirm = ref(false)
const editingProduct = ref(null)
const allAnimals = ref([])
const allCategories = ref([])

const mainAttrs = computed(() => (product.value?.attributes || []).filter((a) => a.is_main))
const otherAttrs = computed(() => (product.value?.attributes || []).filter((a) => !a.is_main))

const activeIndex = computed(() => {
  if (!product.value || !activeImage.value) return 0
  return product.value.images.findIndex((img) => img.id === activeImage.value.id)
})

function scrollThumbIntoView(img) {
  nextTick(() => {
    if (!thumbsRef.value) return
    const btn = thumbsRef.value.querySelector(`[data-id="${img.id}"]`)
    if (btn) btn.scrollIntoView({ block: 'nearest', inline: 'nearest', behavior: 'smooth' })
  })
}

function setActive(img) {
  activeImage.value = img
  scrollThumbIntoView(img)
}

function prevImage() {
  const images = product.value.images
  const idx = (activeIndex.value - 1 + images.length) % images.length
  setActive(images[idx])
}

function nextImage() {
  const images = product.value.images
  const idx = (activeIndex.value + 1) % images.length
  setActive(images[idx])
}

async function loadProduct() {
  loading.value = true
  try {
    const data = await api.getProduct(route.params.slug)
    product.value = data
    activeImage.value = data.images?.[0] || null

    document.title = `${data.name} — fashionAnimals`
  } catch {
    product.value = null
  } finally {
    loading.value = false
  }
}

async function onUploadImage(e) {
  const file = e.target.files[0]
  if (!file) return
  try {
    const updated = await api.uploadImage(product.value.id, file)
    // Only update images array — admin endpoint returns raw JSONB for text fields
    product.value.images = updated.images
    activeImage.value = updated.images[updated.images.length - 1]
    notify.success(t('notify.photoUploaded'))
  } catch (err) {
    notify.error(err.message)
  }
  e.target.value = ''
}

async function onUploadVideo(e) {
  const file = e.target.files[0]
  if (!file) return
  try {
    const updated = await api.uploadVideo(product.value.id, file)
    // Only update images array — admin endpoint returns raw JSONB for text fields
    product.value.images = updated.images
    activeImage.value = updated.images[updated.images.length - 1]
    notify.success(t('notify.videoUploaded'))
  } catch (err) {
    notify.error(err.message)
  }
  e.target.value = ''
}

function onDragStart(e, idx) {
  dragSrcIdx.value = idx
  e.dataTransfer.effectAllowed = 'move'
}

function onDragOver(e, idx) {
  e.preventDefault()
  e.dataTransfer.dropEffect = 'move'
  dragOverIdx.value = idx
}

function onDrop(e, idx) {
  e.preventDefault()
  if (dragSrcIdx.value === null || dragSrcIdx.value === idx) {
    dragSrcIdx.value = null
    dragOverIdx.value = null
    return
  }
  const images = [...product.value.images]
  const [moved] = images.splice(dragSrcIdx.value, 1)
  images.splice(idx, 0, moved)
  product.value.images = images
  dragSrcIdx.value = null
  dragOverIdx.value = null
  saveReorder()
}

function onDragEnd() {
  dragSrcIdx.value = null
  dragOverIdx.value = null
}

async function saveReorder() {
  try {
    await api.reorderImages(product.value.id, product.value.images.map((i) => i.id))
  } catch (err) {
    notify.error(err.message)
  }
}

async function onDeleteMedia() {
  if (!activeImage.value) return
  const isVideo = activeImage.value.media_type === 'video'
  try {
    await api.deleteImage(activeImage.value.id)
    product.value.images = product.value.images.filter((i) => i.id !== activeImage.value.id)
    activeImage.value = product.value.images[0] || null
    notify.success(isVideo ? t('notify.videoDeleted') : t('notify.photoDeleted'))
  } catch (err) {
    notify.error(err.message)
  }
}

async function onDelete() {
  try {
    await api.deleteProduct(product.value.id)
    notify.success(t('notify.productDeleted'))
    router.push('/catalog')
  } catch {
    notify.error(t('notify.deleteError'))
  }
}

async function openEditForm() {
  try {
    editingProduct.value = await api.getProductAdmin(product.value.id)
    showEditForm.value = true
  } catch {
    notify.error(t('notify.loadError'))
  }
}

function onSaved() {
  showEditForm.value = false
  editingProduct.value = null
  loadProduct()
}

watch(() => route.params.slug, loadProduct)

// Re-fetch when locale changes
watch(locale, () => loadProduct())

onMounted(async () => {
  loadProduct()
  if (auth.isLoggedIn) {
    const [a, c] = await Promise.all([api.getAnimals(), api.getCategories()])
    allAnimals.value = a
    allCategories.value = c.flatMap((cat) => [
      { id: cat.id, slug: cat.slug, name: cat.name },
      ...(cat.children || []).map((ch) => ({ id: ch.id, slug: ch.slug, name: `— ${ch.name}` })),
    ])
  }
})
</script>

<style scoped>
.product-page__container {
  max-width: 1280px;
  margin: 0 auto;
  padding: 2rem 1rem;
}

.breadcrumbs {
  margin-bottom: 2rem;
  font-size: 0.875rem;
  color: var(--color-text-secondary);
}

.breadcrumbs a {
  color: var(--color-text-secondary);
  text-decoration: none;
}

.breadcrumbs a:hover { color: var(--color-primary); }
.breadcrumbs__sep { margin: 0 0.5rem; }

.product-detail {
  display: grid;
  grid-template-columns: 1fr;
  gap: 2rem;
}

@media (min-width: 768px) {
  .product-detail { grid-template-columns: 1fr 1fr; }
}

.gallery__main {
  position: relative;
  aspect-ratio: 1;
  overflow: hidden;
  border-radius: 12px;
  background: #f5f5f5;
  display: flex;
  align-items: center;
  justify-content: center;
}

.gallery__arrow {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.85);
  border: none;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #333;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
  transition: background 0.2s, transform 0.2s;
  z-index: 2;
}

.gallery__arrow:hover {
  background: white;
  transform: translateY(-50%) scale(1.1);
}

.gallery__arrow--left { left: 0.75rem; }
.gallery__arrow--right { right: 0.75rem; }

.gallery__image { width: 100%; height: 100%; object-fit: cover; }
.gallery__placeholder { color: var(--color-border); }

.gallery__thumbs {
  display: flex;
  gap: 0.5rem;
  margin-top: 0.75rem;
  overflow-x: auto;
}

.gallery__thumb {
  width: 64px;
  height: 64px;
  border: 2px solid transparent;
  border-radius: 8px;
  overflow: hidden;
  cursor: pointer;
  padding: 0;
  background: #f5f5f5;
  flex-shrink: 0;
}

.gallery__thumb.active { border-color: var(--color-primary); }
.gallery__thumb img { width: 100%; height: 100%; object-fit: cover; }

.gallery__thumb-video {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #2c2c2c;
  color: #fff;
}

.gallery__thumb-main-badge {
  position: absolute;
  top: 2px;
  left: 3px;
  font-size: 10px;
  color: #f59e0b;
  line-height: 1;
  pointer-events: none;
  text-shadow: 0 0 2px rgba(0,0,0,0.4);
}

.gallery__thumb--draggable {
  cursor: grab;
  position: relative;
}

.gallery__thumb--draggable:active {
  cursor: grabbing;
}

.gallery__thumb--dragging {
  opacity: 0.35;
}

.gallery__thumb--drag-over {
  outline: 2px solid var(--color-primary);
  outline-offset: 2px;
}

.gallery__admin {
  display: flex;
  gap: 0.5rem;
  margin-top: 0.75rem;
}

.product-info__brand {
  font-size: 0.875rem;
  color: var(--color-text-secondary);
  text-transform: uppercase;
  letter-spacing: 0.05em;
  margin-bottom: 0.25rem;
}

.product-info__name {
  font-size: 1.75rem;
  margin-bottom: 1rem;
  line-height: 1.2;
}

.product-info__admin {
  display: flex;
  gap: 0.5rem;
  margin-bottom: 1.5rem;
}

.product-info__main-attrs {
  margin-bottom: 1.5rem;
  padding: 1rem;
  background: var(--color-bg-hover);
  border-radius: 8px;
}

.attr-row {
  display: flex;
  justify-content: space-between;
  padding: 0.375rem 0;
}

.attr-row__key { color: var(--color-text-secondary); font-size: 0.875rem; }
.attr-row__value { font-weight: 500; font-size: 0.875rem; }

.product-info__desc { margin-bottom: 1.5rem; }
.product-info__desc h2 { font-size: 1.125rem; margin-bottom: 0.5rem; }
.product-info__desc p { color: var(--color-text-secondary); line-height: 1.7; }

.product-info__attrs { margin-bottom: 1.5rem; }
.product-info__attrs h2 { font-size: 1.125rem; margin-bottom: 0.75rem; }

.attrs-table { width: 100%; border-collapse: collapse; }

.attrs-table td {
  padding: 0.5rem 0;
  border-bottom: 1px solid var(--color-border);
  font-size: 0.875rem;
}

.attrs-table__key { color: var(--color-text-secondary); width: 40%; }

.product-info__tags {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.tag {
  display: inline-block;
  padding: 0.25rem 0.75rem;
  border: 1px solid var(--color-primary);
  border-radius: 20px;
  font-size: 0.8125rem;
  color: var(--color-primary);
  text-decoration: none;
  transition: background 0.15s;
}

.tag:hover { background: var(--color-primary); color: white; }
.tag--category { border-color: var(--color-text-secondary); color: var(--color-text-secondary); }
.tag--category:hover { background: var(--color-text-secondary); color: white; }

.product-page__not-found { text-align: center; padding: 4rem 1rem; }
.product-page__not-found h1 { margin-bottom: 1rem; }

.product-detail--skeleton { pointer-events: none; }

.skeleton {
  background: linear-gradient(90deg, #f0f0f0 25%, #e0e0e0 50%, #f0f0f0 75%);
  background-size: 200% 100%;
  animation: shimmer 1.5s infinite;
  border-radius: 8px;
}

@keyframes shimmer {
  0% { background-position: -200% 0; }
  100% { background-position: 200% 0; }
}

/* Shared */
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
  min-height: 36px;
  font-family: inherit;
}

.btn:hover { background: var(--color-bg-hover); }
.btn--primary { background: var(--color-primary); color: white; border-color: var(--color-primary); }
.btn--primary:hover { background: var(--color-primary-dark); }
.btn--danger { color: var(--color-error); border-color: var(--color-error); }
.btn--danger:hover { background: #fef2f2; }
.btn--sm { padding: 0.25rem 0.75rem; font-size: 0.8125rem; min-height: 28px; }

.modal-overlay {
  position: fixed; inset: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex; align-items: center; justify-content: center;
  z-index: 200; padding: 1rem;
}

.modal {
  background: white; border-radius: 12px;
  padding: 2rem; max-width: 440px; width: 100%;
}

.modal h3 { margin-bottom: 0.5rem; }
.modal p { color: var(--color-text-secondary); margin-bottom: 1.5rem; }
.modal__actions { display: flex; gap: 0.75rem; justify-content: flex-end; }
</style>
