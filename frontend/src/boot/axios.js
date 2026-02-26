import { boot } from 'quasar/wrappers'
import axios from 'axios'

const api = axios.create({
  baseURL: 'http://127.0.0.1:8000/api',
})

// Interceptor para garantir que o token seja pego do localStorage EM CADA requisição
api.interceptors.request.use(config => {
  const token = localStorage.getItem('access_token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
}, error => {
  return Promise.reject(error)
})

export default boot(({ app }) => {
  // Isso permite usar this.$api em componentes Options API ou inject em Composition
  app.config.globalProperties.$api = api
})

export { api }
