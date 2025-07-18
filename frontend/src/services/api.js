import axios from 'axios'

// API based URL configuration
// In Kubernetes, you might want to use the service name directly
// For example, if your backend service is named 'backend-service' in the same namespace:
// const API_BASE_URL = process.env.NODE_ENV === 'production'
//   'http://quotes-api-service:8000'  // Nombre del servicio en Kubernetes
//   : 'http://172.17.0.3:8000'            // Para desarrollo local

const getApiUrl = () => {
  // Check if the config object is available in the global window object
  return window.APP_CONFIG?.API_URL || import.meta.env.VITE_API_URL || 'http://localhost:3000';
};

const api = axios.create({
  // baseURL: API_BASE_URL,
  baseURL: getApiUrl(),
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  }
})

// Interceptor para requests
api.interceptors.request.use(
  (config) => {
    console.log('Making request to:', config.url)
    return config
  },
  (error) => {
    console.error('Request error:', error)
    return Promise.reject(error)
  }
)

// Interceptor para responses
api.interceptors.response.use(
  (response) => {
    console.log('Response received:', response.status)
    return response
  },
  (error) => {
    console.error('Response error:', error.response?.status, error.message)

    // Manejo de errores específicos
    if (error.response?.status === 404) {
      console.error('Resource not found')
    } else if (error.response?.status === 500) {
      console.error('Server error')
    } else if (error.code === 'ECONNREFUSED') {
      console.error('Connection refused - check if backend is running')
    }

    return Promise.reject(error)
  }
)

export default api