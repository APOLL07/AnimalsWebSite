import { getCurrentLocale } from '../i18n/index.js'

const BASE_URL = '/api/v1'

async function request(path, options = {}) {
  // Auto-append lang parameter for localization
  const separator = path.includes('?') ? '&' : '?'
  const lang = getCurrentLocale()
  const url = `${BASE_URL}${path}${separator}lang=${lang}`
  const config = { credentials: 'include', ...options }

  if (config.body && !(config.body instanceof FormData)) {
    config.headers = { 'Content-Type': 'application/json', ...config.headers }
    config.body = JSON.stringify(config.body)
  }

  const response = await fetch(url, config)

  if (response.status === 401 && !path.includes('/auth/')) {
    const refreshed = await fetch(`${BASE_URL}/auth/refresh`, {
      method: 'POST',
      credentials: 'include',
    })
    if (refreshed.ok) {
      return fetch(url, config).then((r) => {
        if (!r.ok) throw new Error(`HTTP ${r.status}`)
        return r.status === 204 ? null : r.json()
      })
    }
  }

  if (!response.ok) {
    const error = await response.json().catch(() => ({}))
    throw new Error(error.detail || `HTTP ${response.status}`)
  }

  if (response.status === 204) return null
  return response.json()
}

export const api = {
  // Public
  getAnimals: () => request('/animals/'),
  getCategories: () => request('/categories/'),
  getProducts: (params = {}) => {
    const query = new URLSearchParams(params).toString()
    return request(`/products/?${query}`)
  },
  getProduct: (slug) => request(`/products/${slug}`),
  search: (params = {}) => {
    const query = new URLSearchParams(params).toString()
    return request(`/search/?${query}`)
  },
  searchSuggest: (q) => request(`/search/suggest?q=${encodeURIComponent(q)}`),

  // Auth
  login: (email, password) =>
    request('/auth/login', { method: 'POST', body: { email, password } }),
  logout: () => request('/auth/logout', { method: 'POST' }),
  me: () => request('/auth/me'),

  // Admin - Products
  getProductAdmin: (id) => request(`/admin/products/${id}`),
  createProduct: (data) =>
    request('/admin/products', { method: 'POST', body: data }),
  updateProduct: (id, data) =>
    request(`/admin/products/${id}`, { method: 'PATCH', body: data }),
  deleteProduct: (id) =>
    request(`/admin/products/${id}`, { method: 'DELETE' }),
  uploadImage: (productId, file) => {
    const form = new FormData()
    form.append('file', file)
    return request(`/admin/products/${productId}/images`, {
      method: 'POST',
      body: form,
    })
  },
  uploadVideo: (productId, file) => {
    const form = new FormData()
    form.append('file', file)
    return request(`/admin/products/${productId}/videos`, {
      method: 'POST',
      body: form,
    })
  },
  deleteImage: (imageId) =>
    request(`/admin/images/${imageId}`, { method: 'DELETE' }),
  reorderImages: (productId, imageIds) =>
    request(`/admin/products/${productId}/images/reorder`, {
      method: 'PUT',
      body: { image_ids: imageIds },
    }),

  // Admin - Animals
  getAnimalsAdmin: () => request('/admin/animals'),
  createAnimal: (data) =>
    request('/admin/animals', { method: 'POST', body: data }),
  updateAnimal: (id, data) =>
    request(`/admin/animals/${id}`, { method: 'PATCH', body: data }),
  deleteAnimal: (id) =>
    request(`/admin/animals/${id}`, { method: 'DELETE' }),

  // Admin - Categories
  getCategoriesAdmin: () => request('/admin/categories'),
  createCategory: (data) =>
    request('/admin/categories', { method: 'POST', body: data }),
  updateCategory: (id, data) =>
    request(`/admin/categories/${id}`, { method: 'PATCH', body: data }),
  deleteCategory: (id) =>
    request(`/admin/categories/${id}`, { method: 'DELETE' }),
}
