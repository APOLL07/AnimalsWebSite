<template>
  <header class="header">
    <div class="header__container">
      <RouterLink to="/" class="header__logo">
        <svg class="header__logo-icon" width="22" height="22" viewBox="0 0 100 100" fill="currentColor" aria-hidden="true">
          <!-- Paw print: 4 toes + palm -->
          <ellipse cx="30" cy="18" rx="10" ry="14" transform="rotate(-15 30 18)" />
          <ellipse cx="58" cy="12" rx="10" ry="14" transform="rotate(5 58 12)" />
          <ellipse cx="82" cy="28" rx="10" ry="14" transform="rotate(20 82 28)" />
          <ellipse cx="14" cy="42" rx="10" ry="14" transform="rotate(-25 14 42)" />
          <path d="M50 38 C24 38 14 56 18 72 C22 86 36 94 50 94 C64 94 78 86 82 72 C86 56 76 38 50 38 Z" />
        </svg>
        <span class="header__logo-text">fashion<strong>Animals</strong></span>
      </RouterLink>

      <nav class="header__nav">
        <div
          class="header__catalog-wrap"
          @mouseenter="openMega"
          @mouseleave="closeMegaDelayed"
        >
          <button class="header__link header__link--catalog" @click="onCatalogClick">
            {{ t('header.catalog') }}
            <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
              <polyline points="6 9 12 15 18 9" />
            </svg>
          </button>

          <!-- Mega menu -->
          <div
            v-show="megaOpen"
            class="mega-menu"
            @mouseenter="openMega"
            @mouseleave="closeMegaDelayed"
          >
            <div class="mega-menu__inner">
              <div class="mega-menu__section">
                <h3 class="mega-menu__heading">{{ t('header.byAnimals') }}</h3>
                <RouterLink
                  v-for="a in animals"
                  :key="a.slug"
                  :to="`/catalog/${a.slug}`"
                  class="mega-menu__link"
                  @click="megaOpen = false"
                >
                  {{ a.name }}
                </RouterLink>
              </div>
              <div v-for="cat in categories" :key="cat.id" class="mega-menu__section">
                <h3 class="mega-menu__heading">{{ cat.name }}</h3>
                <RouterLink
                  v-for="child in cat.children"
                  :key="child.id"
                  :to="`/catalog?category=${child.slug}`"
                  class="mega-menu__link"
                  @click="megaOpen = false"
                >
                  {{ child.name }}
                </RouterLink>
                <RouterLink
                  v-if="!cat.children?.length"
                  :to="`/catalog?category=${cat.slug}`"
                  class="mega-menu__link"
                  @click="megaOpen = false"
                >
                  {{ t('header.allPrefix') }} {{ cat.name.toLowerCase() }}
                </RouterLink>
              </div>
            </div>
          </div>
        </div>
      </nav>

      <div class="header__actions">
        <!-- Search -->
        <div class="header__search-wrap" ref="searchWrapRef">
          <button class="header__search-btn" @click="toggleSearch" :aria-label="t('header.search')">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <circle cx="11" cy="11" r="8" /><path d="m21 21-4.35-4.35" />
            </svg>
          </button>
          <!-- Desktop dropdown / Mobile fullscreen overlay -->
          <Teleport to="body" :disabled="!isMobile">
            <div v-if="searchOpen" :class="['header__search-dropdown', { 'header__search-dropdown--mobile': isMobile }]">
              <div v-if="isMobile" class="header__search-mobile-header">
                <span class="header__search-mobile-title">{{ t('header.search') }}</span>
                <button class="header__search-mobile-close" @click="searchOpen = false">&times;</button>
              </div>
              <form @submit.prevent="goSearch">
                <input
                  ref="searchInputRef"
                  v-model="searchQuery"
                  type="search"
                  class="header__search-input"
                  :placeholder="t('header.searchPlaceholder')"
                  @input="onSearchInput"
                />
              </form>
              <div v-if="suggestions.length" class="header__suggestions">
                <RouterLink
                  v-for="item in suggestions"
                  :key="item.id"
                  :to="`/product/${item.slug}`"
                  class="header__suggestion"
                  @click="searchOpen = false"
                >
                  <img
                    v-if="item.images?.length"
                    :src="item.images[0].url"
                    :alt="item.name"
                    class="header__suggestion-img"
                  />
                  <div v-else class="header__suggestion-img header__suggestion-img--empty"></div>
                  <div class="header__suggestion-info">
                    <span class="header__suggestion-brand">{{ item.brand }}</span>
                    <span class="header__suggestion-name">{{ item.name }}</span>
                  </div>
                </RouterLink>
              </div>
            </div>
          </Teleport>
        </div>

        <!-- Language switcher -->
        <button class="header__lang-btn" @click="toggleLocale">
          {{ t('lang.label') }}
        </button>

        <!-- Auth buttons -->
        <template v-if="auth.isLoggedIn">
          <span class="header__email">{{ auth.email }}</span>
          <button class="header__admin-btn" @click="auth.logout()" :aria-label="t('header.logout')">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4" />
              <polyline points="16 17 21 12 16 7" />
              <line x1="21" y1="12" x2="9" y2="12" />
            </svg>
          </button>
        </template>

        <button v-else class="header__admin-btn" @click="auth.showLoginModal = true" :aria-label="t('header.login')">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2" />
            <circle cx="12" cy="7" r="4" />
          </svg>
        </button>

        <!-- Mobile burger -->
        <button class="header__burger" @click="mobileMenuOpen = !mobileMenuOpen" :aria-label="t('header.menu')">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <template v-if="mobileMenuOpen">
              <line x1="18" y1="6" x2="6" y2="18" /><line x1="6" y1="6" x2="18" y2="18" />
            </template>
            <template v-else>
              <line x1="3" y1="6" x2="21" y2="6" /><line x1="3" y1="12" x2="21" y2="12" /><line x1="3" y1="18" x2="21" y2="18" />
            </template>
          </svg>
        </button>
      </div>
    </div>

    <!-- Mobile menu -->
    <Transition name="slide">
      <div v-if="mobileMenuOpen" class="mobile-menu">
        <RouterLink to="/catalog" class="mobile-menu__link" @click="mobileMenuOpen = false">{{ t('header.catalog') }}</RouterLink>
        <RouterLink
          v-for="a in animals"
          :key="a.slug"
          :to="`/catalog/${a.slug}`"
          class="mobile-menu__link mobile-menu__link--sub"
          @click="mobileMenuOpen = false"
        >
          {{ a.name }}
        </RouterLink>
        <RouterLink to="/search" class="mobile-menu__link" @click="mobileMenuOpen = false">{{ t('header.search') }}</RouterLink>
      </div>
    </Transition>
  </header>
</template>

<script setup>
import { ref, onMounted, onUnmounted, nextTick, watch, computed } from 'vue'
import { RouterLink, useRouter, useRoute } from 'vue-router'
import { api } from '../api/client'
import { useAuthStore } from '../stores/auth'
import { useI18n } from '../i18n/index.js'

const { t, locale, setLocale } = useI18n()
const auth = useAuthStore()
const router = useRouter()
const route = useRoute()

const megaOpen = ref(false)
const mobileMenuOpen = ref(false)
const searchOpen = ref(false)
const searchQuery = ref('')
const suggestions = ref([])
const searchWrapRef = ref(null)
const searchInputRef = ref(null)
const windowWidth = ref(typeof window !== 'undefined' ? window.innerWidth : 1024)

const isMobile = computed(() => windowWidth.value < 475)

let debounceTimer = null
let megaCloseTimer = null

const animals = ref([])
const categories = ref([])

function onResize() {
  windowWidth.value = window.innerWidth
}

onMounted(async () => {
  try {
    const [a, c] = await Promise.all([api.getAnimals(), api.getCategories()])
    animals.value = a
    categories.value = c
  } catch {}

  document.addEventListener('click', onClickOutside)
  window.addEventListener('resize', onResize)
})

onUnmounted(() => {
  document.removeEventListener('click', onClickOutside)
  window.removeEventListener('resize', onResize)
  clearTimeout(megaCloseTimer)
})

// Close mobile menu on route change
watch(() => route.path, () => {
  mobileMenuOpen.value = false
  megaOpen.value = false
})

// Mega menu with debounced close to prevent flickering
function openMega() {
  clearTimeout(megaCloseTimer)
  megaOpen.value = true
}

function closeMegaDelayed() {
  clearTimeout(megaCloseTimer)
  megaCloseTimer = setTimeout(() => {
    megaOpen.value = false
  }, 120)
}

function onCatalogClick() {
  megaOpen.value = false
  router.push('/catalog')
}

function onClickOutside(e) {
  if (!isMobile.value && searchWrapRef.value && !searchWrapRef.value.contains(e.target)) {
    searchOpen.value = false
  }
}

async function toggleSearch() {
  searchOpen.value = !searchOpen.value
  if (searchOpen.value) {
    await nextTick()
    searchInputRef.value?.focus()
  }
}

function onSearchInput() {
  clearTimeout(debounceTimer)
  const q = searchQuery.value.trim()
  if (!q) {
    suggestions.value = []
    return
  }
  debounceTimer = setTimeout(async () => {
    try {
      suggestions.value = await api.searchSuggest(q)
    } catch {
      suggestions.value = []
    }
  }, 250)
}

function goSearch() {
  if (!searchQuery.value.trim()) return
  router.push({ path: '/search', query: { q: searchQuery.value.trim() } })
  searchOpen.value = false
}

function toggleLocale() {
  setLocale(locale.value === 'uk' ? 'ru' : 'uk')
}
</script>

<style scoped>
.header {
  position: sticky;
  top: 0;
  z-index: 100;
  background: var(--color-bg);
  border-bottom: 1px solid var(--color-border);
  padding: 0 1rem;
}

.header__container {
  max-width: 1280px;
  margin: 0 auto;
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 64px;
}

.header__logo {
  text-decoration: none;
  color: var(--color-text);
  font-size: 1.25rem;
  flex-shrink: 0;
  display: flex;
  align-items: center;
  gap: 0.4rem;
}

.header__logo-icon {
  flex-shrink: 0;
  color: var(--color-primary);
}

.header__nav {
  display: none;
  gap: 1.5rem;
}

@media (min-width: 768px) {
  .header__nav { display: flex; }
  .header__burger { display: none !important; }
}

.header__catalog-wrap {
  position: relative;
}

.header__link {
  text-decoration: none;
  color: var(--color-text-secondary);
  font-size: 0.875rem;
  transition: color 0.2s;
  display: flex;
  align-items: center;
  gap: 0.25rem;
  background: none;
  border: none;
  cursor: pointer;
  font-family: inherit;
  padding: 0.5rem 0;
}

.header__link:hover {
  color: var(--color-primary);
}

/* Mega menu — no gap, seamless hover zone */
.mega-menu {
  position: absolute;
  top: 100%;
  left: 50%;
  transform: translateX(-50%);
  padding-top: 0;
  z-index: 110;
}

.mega-menu__inner {
  background: white;
  border: 1px solid var(--color-border);
  border-radius: 12px;
  box-shadow: 0 12px 40px rgba(0, 0, 0, 0.12);
  display: flex;
  gap: 2rem;
  padding: 1.5rem 2rem;
  min-width: 400px;
  margin-top: 4px;
}

.mega-menu__section {
  min-width: 120px;
}

.mega-menu__heading {
  font-size: 0.75rem;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: var(--color-text-secondary);
  margin-bottom: 0.5rem;
  font-weight: 600;
}

.mega-menu__link {
  display: block;
  padding: 0.25rem 0;
  text-decoration: none;
  color: var(--color-text);
  font-size: 0.875rem;
  transition: color 0.15s;
}

.mega-menu__link:hover {
  color: var(--color-primary);
}

/* Header actions */
.header__actions {
  display: flex;
  align-items: center;
  gap: 0.25rem;
}

.header__email {
  font-size: 0.8125rem;
  color: var(--color-primary);
  display: none;
}

@media (min-width: 768px) {
  .header__email { display: inline; }
}

.header__search-btn,
.header__admin-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 44px;
  height: 44px;
  border: none;
  background: none;
  color: var(--color-text-secondary);
  cursor: pointer;
  border-radius: 8px;
  text-decoration: none;
  transition: background 0.2s, color 0.2s;
}

.header__search-btn:hover,
.header__admin-btn:hover {
  background: var(--color-bg-hover);
  color: var(--color-text);
}

/* Language switcher */
.header__lang-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 32px;
  padding: 0 0.5rem;
  border: 1px solid var(--color-border);
  background: none;
  color: var(--color-text-secondary);
  cursor: pointer;
  border-radius: 6px;
  font-size: 0.75rem;
  font-weight: 600;
  font-family: inherit;
  letter-spacing: 0.05em;
  transition: background 0.2s, color 0.2s;
}

.header__lang-btn:hover {
  background: var(--color-bg-hover);
  color: var(--color-text);
}

/* Search dropdown — desktop */
.header__search-wrap {
  position: relative;
}

.header__search-dropdown {
  position: absolute;
  top: 100%;
  right: 0;
  width: 320px;
  background: white;
  border: 1px solid var(--color-border);
  border-radius: 12px;
  box-shadow: 0 8px 30px rgba(0, 0, 0, 0.12);
  margin-top: 0.25rem;
  overflow: hidden;
  z-index: 110;
}

/* Mobile fullscreen search overlay */
.header__search-dropdown--mobile {
  position: fixed;
  inset: 0;
  width: 100%;
  border-radius: 0;
  margin-top: 0;
  z-index: 300;
  display: flex;
  flex-direction: column;
}

.header__search-mobile-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0.75rem 1rem;
  border-bottom: 1px solid var(--color-border);
  flex-shrink: 0;
}

.header__search-mobile-title {
  font-size: 1.125rem;
  font-weight: 600;
}

.header__search-mobile-close {
  background: none;
  border: none;
  font-size: 1.75rem;
  cursor: pointer;
  color: var(--color-text-secondary);
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 8px;
}

.header__search-mobile-close:hover {
  background: var(--color-bg-hover);
}

.header__search-dropdown--mobile .header__search-input {
  font-size: 1.125rem;
  padding: 1rem;
}

.header__search-dropdown--mobile .header__suggestions {
  flex: 1;
  max-height: none;
}

.header__search-input {
  width: 100%;
  padding: 0.75rem 1rem;
  border: none;
  border-bottom: 1px solid var(--color-border);
  font-size: 0.9375rem;
  font-family: inherit;
  outline: none;
  box-sizing: border-box;
}

.header__suggestions {
  max-height: 320px;
  overflow-y: auto;
}

.header__suggestion {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.625rem 1rem;
  text-decoration: none;
  color: inherit;
  transition: background 0.1s;
}

.header__suggestion:hover {
  background: var(--color-bg-hover);
}

.header__suggestion-img {
  width: 44px;
  height: 44px;
  border-radius: 6px;
  object-fit: cover;
  flex-shrink: 0;
}

.header__suggestion-img--empty {
  background: #f0f0f0;
}

.header__suggestion-info {
  display: flex;
  flex-direction: column;
  min-width: 0;
}

.header__suggestion-brand {
  font-size: 0.6875rem;
  color: var(--color-text-secondary);
  text-transform: uppercase;
  letter-spacing: 0.04em;
}

.header__suggestion-name {
  font-size: 0.8125rem;
  font-weight: 500;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

/* Burger */
.header__burger {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 44px;
  height: 44px;
  border: none;
  background: none;
  color: var(--color-text);
  cursor: pointer;
  border-radius: 8px;
}

@media (min-width: 768px) {
  .header__burger { display: none; }
}

/* Mobile menu */
.mobile-menu {
  display: flex;
  flex-direction: column;
  padding: 0.5rem 1rem 1rem;
  border-top: 1px solid var(--color-border);
  background: var(--color-bg);
}

@media (min-width: 768px) {
  .mobile-menu { display: none; }
}

.mobile-menu__link {
  display: block;
  padding: 0.625rem 0;
  text-decoration: none;
  color: var(--color-text);
  font-size: 0.9375rem;
  border-bottom: 1px solid var(--color-border);
}

.mobile-menu__link--sub {
  padding-left: 1rem;
  color: var(--color-text-secondary);
  font-size: 0.875rem;
}

.mobile-menu__link:last-child {
  border-bottom: none;
}

.slide-enter-active,
.slide-leave-active {
  transition: max-height 0.2s ease, opacity 0.2s ease;
  max-height: 400px;
  overflow: hidden;
}

.slide-enter-from,
.slide-leave-to {
  max-height: 0;
  opacity: 0;
}
</style>
