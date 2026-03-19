<template>
  <div class="modal-overlay" @click.self="$emit('close')">
    <div class="modal modal--wide">
      <div class="modal__header">
        <h2>{{ t('categoryManager.title') }}</h2>
        <button class="modal__close" @click="$emit('close')">&times;</button>
      </div>

      <div class="entity-list">
        <template v-for="cat in categories" :key="cat.id">
          <div class="entity-row entity-row--parent">
            <template v-if="editing === cat.id">
              <input v-model="editForm.name" class="form-input" @keydown.enter="saveEdit(cat.id)" />
              <div class="entity-row__actions">
                <button class="btn btn--sm btn--primary" @click="saveEdit(cat.id)">OK</button>
                <button class="btn btn--sm" @click="editing = null">{{ t('common.cancel') }}</button>
              </div>
            </template>
            <template v-else>
              <span class="entity-row__name entity-row__name--parent">{{ cat.name }}</span>
              <div class="entity-row__actions">
                <button class="btn btn--sm" @click="startEdit(cat)">{{ t('common.edit') }}</button>
                <button class="btn btn--sm btn--danger" @click="doDelete(cat.id)">{{ t('common.delete') }}</button>
              </div>
            </template>
          </div>

          <div v-for="child in cat.children" :key="child.id" class="entity-row entity-row--child">
            <template v-if="editing === child.id">
              <input v-model="editForm.name" class="form-input" @keydown.enter="saveEdit(child.id)" />
              <div class="entity-row__actions">
                <button class="btn btn--sm btn--primary" @click="saveEdit(child.id)">OK</button>
                <button class="btn btn--sm" @click="editing = null">{{ t('common.cancel') }}</button>
              </div>
            </template>
            <template v-else>
              <span class="entity-row__name">{{ child.name }}</span>
              <div class="entity-row__actions">
                <button class="btn btn--sm" @click="startEdit(child)">{{ t('common.edit') }}</button>
                <button class="btn btn--sm btn--danger" @click="doDelete(child.id)">{{ t('common.delete') }}</button>
              </div>
            </template>
          </div>

          <!-- Add subcategory inline -->
          <div class="entity-row entity-row--child entity-row--add">
            <input
              v-model="newChildName[cat.id]"
              class="form-input form-input--sm"
              :placeholder="t('categoryManager.newSubcategory')"
              @keydown.enter="createChild(cat.id)"
            />
            <button class="btn btn--sm" @click="createChild(cat.id)" :disabled="!newChildName[cat.id]?.trim()">+</button>
          </div>
        </template>
      </div>

      <div class="entity-add">
        <input
          v-model="newRootName"
          class="form-input"
          :placeholder="t('categoryManager.newRoot')"
          @keydown.enter="createRoot"
        />
        <button class="btn btn--primary btn--sm" @click="createRoot" :disabled="!newRootName.trim()">
          {{ t('common.add') }}
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { api } from '../api/client'
import { useNotifications } from '../stores/notifications'
import { useI18n } from '../i18n/index.js'

const { t } = useI18n()

const props = defineProps({
  categories: { type: Array, default: () => [] },
})

const emit = defineEmits(['close', 'refresh'])
const notify = useNotifications()

const newRootName = ref('')
const newChildName = reactive({})
const editing = ref(null)
const editForm = ref({ name: '' })

function startEdit(item) {
  editing.value = item.id
  editForm.value = { name: item.name }
}

async function saveEdit(id) {
  if (!editForm.value.name.trim()) return
  try {
    await api.updateCategory(id, { name: editForm.value.name.trim() })
    notify.success(t('notify.categoryUpdated'))
    editing.value = null
    emit('refresh')
  } catch (e) {
    notify.error(e.message)
  }
}

async function doDelete(id) {
  try {
    await api.deleteCategory(id)
    notify.success(t('notify.categoryDeleted'))
    emit('refresh')
  } catch (e) {
    notify.error(e.message)
  }
}

async function createRoot() {
  if (!newRootName.value.trim()) return
  try {
    await api.createCategory({ name: newRootName.value.trim() })
    notify.success(t('notify.categoryCreated'))
    newRootName.value = ''
    emit('refresh')
  } catch (e) {
    notify.error(e.message)
  }
}

async function createChild(parentId) {
  const name = newChildName[parentId]?.trim()
  if (!name) return
  try {
    await api.createCategory({ name, parent_id: parentId })
    notify.success(t('notify.subcategoryCreated'))
    newChildName[parentId] = ''
    emit('refresh')
  } catch (e) {
    notify.error(e.message)
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
  padding: 2rem 1rem;
  overflow-y: auto;
}

.modal--wide {
  background: white;
  border-radius: 12px;
  padding: 1.5rem;
  max-width: 540px;
  width: 100%;
}

.modal__header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.modal__header h2 { font-size: 1.25rem; }

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
}

.modal__close:hover { background: var(--color-bg-hover); }

.entity-list {
  max-height: 400px;
  overflow-y: auto;
  margin-bottom: 1rem;
}

.entity-row {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 0;
  border-bottom: 1px solid var(--color-border);
}

.entity-row--parent {
  background: var(--color-bg-hover);
  padding: 0.5rem;
  border-radius: 6px;
  margin-top: 0.5rem;
}

.entity-row--child {
  padding-left: 1.5rem;
}

.entity-row--add {
  border-bottom: none;
  opacity: 0.7;
}

.entity-row--add:hover { opacity: 1; }

.entity-row__name {
  flex: 1;
  min-width: 80px;
}

.entity-row__name--parent {
  font-weight: 700;
}

.entity-row__actions {
  display: flex;
  gap: 0.25rem;
  flex-shrink: 0;
}

.entity-add {
  display: flex;
  gap: 0.5rem;
}

.form-input {
  flex: 1;
  padding: 0.5rem 0.75rem;
  border: 1px solid var(--color-border);
  border-radius: 8px;
  font-size: 0.9375rem;
  font-family: inherit;
  outline: none;
  box-sizing: border-box;
}

.form-input--sm {
  padding: 0.375rem 0.5rem;
  font-size: 0.8125rem;
}

.form-input:focus { border-color: var(--color-primary); }

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
  white-space: nowrap;
}

.btn:hover { background: var(--color-bg-hover); }
.btn--primary { background: var(--color-primary); color: white; border-color: var(--color-primary); }
.btn--primary:hover { background: var(--color-primary-dark); }
.btn--primary:disabled { opacity: 0.5; cursor: not-allowed; }
.btn--danger { color: var(--color-error); border-color: var(--color-error); }
.btn--danger:hover { background: #fef2f2; }
.btn--sm { padding: 0.25rem 0.75rem; font-size: 0.8125rem; min-height: 28px; }
</style>
