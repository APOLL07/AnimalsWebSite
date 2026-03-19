<template>
  <div class="modal-overlay" @click.self="$emit('close')">
    <div class="modal modal--wide">
      <div class="modal__header">
        <h2>{{ title }}</h2>
        <button class="modal__close" @click="$emit('close')">&times;</button>
      </div>

      <div class="entity-list">
        <div v-for="item in items" :key="item.id" class="entity-row">
          <template v-if="editing === item.id">
            <input
              v-model="editForm.name"
              class="form-input"
              @keydown.enter="saveEdit(item.id)"
            />
            <div class="entity-row__actions">
              <button class="btn btn--sm btn--primary" @click="saveEdit(item.id)">OK</button>
              <button class="btn btn--sm" @click="editing = null">{{ t('common.cancel') }}</button>
            </div>
          </template>
          <template v-else>
            <span class="entity-row__name">{{ item.name }}</span>
            <span class="entity-row__slug">{{ item.slug }}</span>
            <div class="entity-row__actions">
              <button class="btn btn--sm" @click="startEdit(item)">{{ t('common.edit') }}</button>
              <button class="btn btn--sm btn--danger" @click="onDelete(item.id)">{{ t('common.delete') }}</button>
            </div>
          </template>
        </div>
      </div>

      <div class="entity-add">
        <input
          v-model="newName"
          class="form-input"
          :placeholder="t('entityManager.namePlaceholder')"
          @keydown.enter="onCreate"
        />
        <button class="btn btn--primary btn--sm" @click="onCreate" :disabled="!newName.trim()">
          {{ t('common.add') }}
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useI18n } from '../i18n/index.js'

const { t } = useI18n()

const props = defineProps({
  title: { type: String, required: true },
  items: { type: Array, default: () => [] },
})

const emit = defineEmits(['close', 'create', 'update', 'delete'])

const newName = ref('')
const editing = ref(null)
const editForm = ref({ name: '' })

function onCreate() {
  if (!newName.value.trim()) return
  emit('create', { name: newName.value.trim() })
  newName.value = ''
}

function startEdit(item) {
  editing.value = item.id
  editForm.value = { name: item.name }
}

function saveEdit(id) {
  if (!editForm.value.name.trim()) return
  emit('update', id, { name: editForm.value.name.trim() })
  editing.value = null
}

function onDelete(id) {
  emit('delete', id)
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
  max-width: 500px;
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
  max-height: 320px;
  overflow-y: auto;
  margin-bottom: 1rem;
}

.entity-row {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 0;
  border-bottom: 1px solid var(--color-border);
  flex-wrap: wrap;
}

.entity-row__name {
  font-weight: 500;
  flex: 1;
  min-width: 80px;
}

.entity-row__slug {
  font-size: 0.75rem;
  color: var(--color-text-secondary);
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
