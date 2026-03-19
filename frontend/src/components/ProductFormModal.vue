<template>
  <div class="modal-overlay" @click.self="$emit('close')">
    <div class="modal modal--wide">
      <div class="modal__header">
        <h2>{{ isEdit ? t('productForm.editTitle') : t('productForm.createTitle') }}</h2>
        <button class="modal__close" @click="$emit('close')">&times;</button>
      </div>

      <form @submit.prevent="onSubmit" class="product-form">
        <!-- Language tabs -->
        <div class="lang-tabs">
          <button type="button" :class="['lang-tab', { active: editLang === 'uk' }]" @click="editLang = 'uk'">UA</button>
          <button type="button" :class="['lang-tab', { active: editLang === 'ru' }]" @click="editLang = 'ru'">RU</button>
        </div>

        <div class="form-group">
          <label>{{ t('productForm.name') }}</label>
          <input v-model="form.name[editLang]" required class="form-input" />
        </div>

        <div class="form-group">
          <label>{{ t('productForm.brand') }}</label>
          <input v-model="form.brand" class="form-input" />
        </div>

        <div class="form-group">
          <label>{{ t('productForm.description') }}</label>
          <textarea v-model="form.description[editLang]" rows="4" class="form-input"></textarea>
        </div>

        <div class="form-row">
          <div class="form-group">
            <label>{{ t('productForm.animals') }}</label>
            <div class="checkbox-group">
              <label v-for="a in animals" :key="a.id" class="checkbox-label">
                <input type="checkbox" :value="a.id" v-model="form.animal_ids" />
                {{ displayName(a.name) }}
              </label>
            </div>
          </div>
          <div class="form-group">
            <label>{{ t('productForm.categories') }}</label>
            <div class="checkbox-group">
              <label v-for="c in categories" :key="c.id" class="checkbox-label">
                <input type="checkbox" :value="c.id" v-model="form.category_ids" />
                {{ displayName(c.name) }}
              </label>
            </div>
          </div>
        </div>

        <div class="form-group">
          <label>{{ t('productForm.attributes') }}</label>
          <div v-for="(attr, idx) in form.attributes" :key="idx" class="attr-row">
            <input v-model="attr.key[editLang]" :placeholder="t('productForm.attrKeyPlaceholder')" class="form-input attr-input" />
            <input v-model="attr.value[editLang]" :placeholder="t('productForm.attrValuePlaceholder')" class="form-input attr-input" />
            <label class="checkbox-label checkbox-label--inline">
              <input type="checkbox" v-model="attr.is_main" /> {{ t('productForm.attrMain') }}
            </label>
            <button type="button" class="btn-icon" @click="form.attributes.splice(idx, 1)">&times;</button>
          </div>
          <button type="button" class="btn btn--sm" @click="addAttribute">{{ t('productForm.addAttribute') }}</button>
        </div>

        <!-- Image upload (for new products too) -->
        <div class="form-group">
          <label>{{ t('productForm.photos') }}</label>
          <div v-if="imagePreviews.length" class="image-previews">
            <div v-for="(img, idx) in imagePreviews" :key="idx" class="image-preview">
              <img :src="img.url" :alt="`${t('productForm.photoLabel')} ${idx + 1}`" />
              <button type="button" class="image-preview__remove" @click="removeImage(idx)">&times;</button>
            </div>
          </div>
          <label class="btn btn--sm upload-btn">
            {{ t('productForm.addPhoto') }}
            <input type="file" accept="image/*" multiple hidden @change="onFilesSelected" />
          </label>
        </div>

        <!-- Video upload -->
        <div class="form-group">
          <label>{{ t('productForm.videos') }}</label>
          <div v-if="videoPreviews.length" class="image-previews">
            <div v-for="(vid, idx) in videoPreviews" :key="idx" class="image-preview image-preview--video">
              <svg width="32" height="32" viewBox="0 0 24 24" fill="currentColor" class="video-icon">
                <polygon points="5 3 19 12 5 21" />
              </svg>
              <span class="image-preview__name">{{ vid.name }}</span>
              <button type="button" class="image-preview__remove" @click="removeVideo(idx)">&times;</button>
            </div>
          </div>
          <label class="btn btn--sm upload-btn">
            {{ t('productForm.addVideo') }}
            <input type="file" accept="video/mp4,video/webm,video/quicktime" hidden @change="onVideoSelected" />
          </label>
        </div>

        <div class="form-group">
          <label class="checkbox-label">
            <input type="checkbox" v-model="form.is_active" /> {{ t('productForm.isActive') }}
          </label>
        </div>

        <p v-if="error" class="form-error">{{ error }}</p>

        <div class="form-actions">
          <button type="button" class="btn" @click="$emit('close')">{{ t('common.cancel') }}</button>
          <button type="submit" class="btn btn--primary" :disabled="submitting">
            {{ submitting ? t('common.saving') : (isEdit ? t('common.save') : t('common.create')) }}
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed } from 'vue'
import { api } from '../api/client'
import { useNotifications } from '../stores/notifications'
import { useI18n } from '../i18n/index.js'

const { t } = useI18n()

const props = defineProps({
  product: { type: Object, default: null },
  animals: { type: Array, default: () => [] },
  categories: { type: Array, default: () => [] },
})

const emit = defineEmits(['close', 'saved'])
const notify = useNotifications()

const isEdit = computed(() => !!props.product)
const submitting = ref(false)
const error = ref('')
const editLang = ref('uk')

function toDict(val) {
  if (typeof val === 'object' && val !== null) return { uk: val.uk || '', ru: val.ru || '' }
  return { uk: val || '', ru: val || '' }
}

function displayName(name) {
  if (typeof name === 'object' && name !== null) return name.uk || name.ru || ''
  return name || ''
}

const form = reactive({
  name: toDict(props.product?.name),
  brand: props.product?.brand || '',
  description: toDict(props.product?.description),
  is_active: props.product?.is_active ?? true,
  animal_ids: props.product?.animals?.map((a) => a.id) || [],
  category_ids: props.product?.categories?.map((c) => c.id) || [],
  attributes: props.product?.attributes?.map((a) => ({
    key: toDict(a.key),
    value: toDict(a.value),
    is_main: a.is_main,
  })) || [],
})

// Image upload state
const pendingFiles = ref([])
const imagePreviews = ref([])

// Video upload state
const pendingVideos = ref([])
const videoPreviews = ref([])

function addAttribute() {
  form.attributes.push({ key: { uk: '', ru: '' }, value: { uk: '', ru: '' }, is_main: false })
}

function onFilesSelected(e) {
  const files = Array.from(e.target.files)
  for (const file of files) {
    pendingFiles.value.push(file)
    imagePreviews.value.push({ url: URL.createObjectURL(file), file })
  }
  e.target.value = ''
}

function removeImage(idx) {
  URL.revokeObjectURL(imagePreviews.value[idx].url)
  imagePreviews.value.splice(idx, 1)
  pendingFiles.value.splice(idx, 1)
}

function onVideoSelected(e) {
  const file = e.target.files[0]
  if (!file) return
  pendingVideos.value.push(file)
  videoPreviews.value.push({ name: file.name })
  e.target.value = ''
}

function removeVideo(idx) {
  videoPreviews.value.splice(idx, 1)
  pendingVideos.value.splice(idx, 1)
}

async function onSubmit() {
  if (!form.name.uk.trim() && !form.name.ru.trim()) return
  error.value = ''
  submitting.value = true

  const payload = {
    name: form.name,
    brand: form.brand,
    description: form.description,
    is_active: form.is_active,
    animal_ids: form.animal_ids,
    category_ids: form.category_ids,
    attributes: form.attributes.filter((a) => (a.key.uk || a.key.ru) && (a.value.uk || a.value.ru)),
  }

  try {
    let product
    if (isEdit.value) {
      product = await api.updateProduct(props.product.id, payload)
      notify.success(t('notify.productUpdated'))
    } else {
      product = await api.createProduct(payload)
      notify.success(t('notify.productCreated'))
    }

    // Upload images for the product
    if (pendingFiles.value.length && product?.id) {
      for (const file of pendingFiles.value) {
        try {
          await api.uploadImage(product.id, file)
        } catch (imgErr) {
          notify.error(`${t('notify.photoUploadError')}: ${imgErr.message}`)
        }
      }
    }

    // Upload videos for the product
    if (pendingVideos.value.length && product?.id) {
      for (const file of pendingVideos.value) {
        try {
          await api.uploadVideo(product.id, file)
        } catch (vidErr) {
          notify.error(`${t('notify.videoUploadError')}: ${vidErr.message}`)
        }
      }
    }

    emit('saved')
  } catch (e) {
    error.value = e.message
  } finally {
    submitting.value = false
  }
}
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: flex-start;
  justify-content: center;
  z-index: 200;
  padding: 1rem;
  overflow-y: auto;
}

.modal--wide {
  background: white;
  border-radius: 12px;
  padding: 1.5rem;
  max-width: 640px;
  width: 100%;
  margin: 1rem 0;
  max-height: calc(100vh - 2rem);
  display: flex;
  flex-direction: column;
}

.modal__header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.25rem;
  flex-shrink: 0;
}

.modal__header h2 { font-size: 1.25rem; }

.product-form {
  overflow-y: auto;
  flex: 1;
  min-height: 0;
}

.modal__close {
  background: none;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
  color: var(--color-text-secondary);
  width: 36px;
  height: 36px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 8px;
  flex-shrink: 0;
}

.modal__close:hover { background: var(--color-bg-hover); }

.lang-tabs {
  display: flex;
  gap: 0.25rem;
  margin-bottom: 1rem;
}

.lang-tab {
  padding: 0.375rem 1rem;
  border: 1px solid var(--color-border);
  border-radius: 6px;
  background: white;
  font-size: 0.8125rem;
  font-weight: 600;
  cursor: pointer;
  font-family: inherit;
  transition: all 0.15s;
}

.lang-tab:hover { background: var(--color-bg-hover); }

.lang-tab.active {
  background: var(--color-primary);
  color: white;
  border-color: var(--color-primary);
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
}

@media (max-width: 480px) {
  .form-row { grid-template-columns: 1fr; }
}

.form-group {
  margin-bottom: 1rem;
}

.form-group > label {
  display: block;
  font-size: 0.875rem;
  margin-bottom: 0.25rem;
  color: var(--color-text-secondary);
}

.form-input {
  width: 100%;
  padding: 0.5rem 0.75rem;
  border: 1px solid var(--color-border);
  border-radius: 8px;
  font-size: 0.9375rem;
  font-family: inherit;
  outline: none;
  transition: border-color 0.15s;
  box-sizing: border-box;
}

.form-input:focus { border-color: var(--color-primary); }

textarea.form-input { resize: vertical; }

.checkbox-group {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  max-height: 160px;
  overflow-y: auto;
  padding: 0.5rem;
  border: 1px solid var(--color-border);
  border-radius: 8px;
}

.checkbox-label {
  display: flex;
  align-items: center;
  gap: 0.375rem;
  font-size: 0.8125rem;
  cursor: pointer;
}

.checkbox-label--inline { white-space: nowrap; }

.attr-row {
  display: flex;
  gap: 0.5rem;
  align-items: center;
  margin-bottom: 0.5rem;
  flex-wrap: wrap;
}

.attr-input {
  flex: 1;
  min-width: 100px;
}

.btn-icon {
  background: none;
  border: none;
  font-size: 1.25rem;
  cursor: pointer;
  color: var(--color-error);
  width: 28px;
  height: 28px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 4px;
  flex-shrink: 0;
}

.btn-icon:hover { background: #fef2f2; }

/* Image previews */
.image-previews {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  margin-bottom: 0.5rem;
}

.image-preview {
  position: relative;
  width: 80px;
  height: 80px;
  border-radius: 8px;
  overflow: hidden;
  border: 1px solid var(--color-border);
}

.image-preview img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.image-preview__remove {
  position: absolute;
  top: 2px;
  right: 2px;
  width: 20px;
  height: 20px;
  border-radius: 50%;
  background: rgba(0,0,0,0.6);
  color: white;
  border: none;
  cursor: pointer;
  font-size: 14px;
  display: flex;
  align-items: center;
  justify-content: center;
  line-height: 1;
}

.image-preview--video {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  background: #f0f0f0;
  width: auto;
  min-width: 80px;
  padding: 0.25rem 0.5rem;
  gap: 0.125rem;
}

.video-icon { color: #666; }

.image-preview__name {
  font-size: 0.625rem;
  color: var(--color-text-secondary);
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  max-width: 70px;
}

.upload-btn { cursor: pointer; }

.form-error {
  color: var(--color-error);
  font-size: 0.875rem;
  margin-bottom: 0.75rem;
}

.form-actions {
  display: flex;
  gap: 0.75rem;
  justify-content: flex-end;
  margin-top: 1rem;
}

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
  font-family: inherit;
  min-height: 36px;
}

.btn:hover { background: var(--color-bg-hover); }

.btn--primary {
  background: var(--color-primary);
  color: white;
  border-color: var(--color-primary);
}

.btn--primary:hover { background: var(--color-primary-dark); }
.btn--primary:disabled { opacity: 0.6; cursor: not-allowed; }
.btn--sm { padding: 0.25rem 0.75rem; font-size: 0.8125rem; min-height: 28px; }
</style>
