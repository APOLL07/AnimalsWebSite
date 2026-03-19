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
            <div class="entity-row__edit">
              <div class="lang-tabs lang-tabs--sm">
                <button type="button" :class="['lang-tab', { active: editLang === 'uk' }]" @click="editLang = 'uk'">UA</button>
                <button type="button" :class="['lang-tab', { active: editLang === 'ru' }]" @click="editLang = 'ru'">RU</button>
              </div>
              <input
                v-model="editForm.name[editLang]"
                class="form-input"
                @keydown.enter="saveEdit(item.id)"
              />
            </div>
            <div class="entity-row__actions">
              <button class="btn btn--sm btn--primary" @click="saveEdit(item.id)">OK</button>
              <button class="btn btn--sm" @click="editing = null">{{ t('common.cancel') }}</button>
            </div>
          </template>
          <template v-else>
            <span class="entity-row__name">{{ displayName(item.name) }}</span>
            <span class="entity-row__slug">{{ item.slug }}</span>
            <div class="entity-row__actions">
              <button class="btn btn--sm" @click="startEdit(item)">{{ t('common.edit') }}</button>
              <button class="btn btn--sm btn--danger" @click="onDelete(item.id)">{{ t('common.delete') }}</button>
            </div>
          </template>
        </div>
      </div>

      <div class="entity-add">
        <div class="lang-tabs lang-tabs--sm">
          <button type="button" :class="['lang-tab', { active: addLang === 'uk' }]" @click="addLang = 'uk'">UA</button>
          <button type="button" :class="['lang-tab', { active: addLang === 'ru' }]" @click="addLang = 'ru'">RU</button>
        </div>
        <div class="entity-add__row">
          <input
            v-model="newName[addLang]"
            class="form-input"
            :placeholder="t('entityManager.namePlaceholder')"
            @keydown.enter="onCreate"
          />
          <button class="btn btn--primary btn--sm" @click="onCreate" :disabled="!newName.uk.trim() && !newName.ru.trim()">
            {{ t('common.add') }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useI18n } from '../i18n/index.js'

const { t } = useI18n()

const props = defineProps({
  title: { type: String, required: true },
  items: { type: Array, default: () => [] },
})

const emit = defineEmits(['close', 'create', 'update', 'delete'])

const newName = reactive({ uk: '', ru: '' })
const addLang = ref('uk')
const editing = ref(null)
const editLang = ref('uk')
const editForm = ref({ name: { uk: '', ru: '' } })

function displayName(name) {
  if (typeof name === 'object' && name !== null) return name.uk || name.ru || ''
  return name || ''
}

function onCreate() {
  if (!newName.uk.trim() && !newName.ru.trim()) return
  emit('create', { name: { uk: newName.uk.trim(), ru: newName.ru.trim() } })
  newName.uk = ''
  newName.ru = ''
}

function startEdit(item) {
  editing.value = item.id
  editLang.value = 'uk'
  const name = typeof item.name === 'object' ? item.name : { uk: item.name, ru: item.name }
  editForm.value = { name: { uk: name.uk || '', ru: name.ru || '' } }
}

function saveEdit(id) {
  if (!editForm.value.name.uk.trim() && !editForm.value.name.ru.trim()) return
  emit('update', id, { name: editForm.value.name })
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

.lang-tabs {
  display: flex;
  gap: 0.25rem;
  margin-bottom: 0.5rem;
}

.lang-tabs--sm { margin-bottom: 0.375rem; }

.lang-tab {
  padding: 0.25rem 0.625rem;
  border: 1px solid var(--color-border);
  border-radius: 4px;
  background: white;
  font-size: 0.6875rem;
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

.entity-row__edit {
  flex: 1;
  min-width: 0;
}

.entity-add {
  display: flex;
  flex-direction: column;
  gap: 0;
}

.entity-add__row {
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
