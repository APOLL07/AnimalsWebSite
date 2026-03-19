import { ref, computed } from 'vue'
import ru from './ru.js'
import uk from './uk.js'

const messages = { ru, uk }
const STORAGE_KEY = 'fa_locale'

const current = ref(localStorage.getItem(STORAGE_KEY) || 'uk')

export function useI18n() {
  function t(key) {
    return messages[current.value]?.[key] || messages.ru[key] || key
  }

  function setLocale(locale) {
    current.value = locale
    localStorage.setItem(STORAGE_KEY, locale)
  }

  const locale = computed(() => current.value)

  return { t, locale, setLocale }
}
