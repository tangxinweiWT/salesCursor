import axios from 'axios'

// 创建axios实例
const api = axios.create({
  baseURL: '/api',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json'
  }
})

// 请求拦截器
api.interceptors.request.use(
  config => {
    return config
  },
  error => {
    return Promise.reject(error)
  }
)

// 响应拦截器
api.interceptors.response.use(
  response => {
    console.log('API响应成功:', response.config.url, response.data)
    return response.data
  },
  error => {
    console.error('API请求错误:', error.config?.url, error)
    console.error('错误状态码:', error.response?.status)
    console.error('错误响应数据:', error.response?.data)
    return Promise.reject(error)
  }
)

// 销售数据相关API
export const salesAPI = {
  // 获取销售统计数据
  getSalesStats: () => api.get('/sales/stats'),
  
  // 获取销售趋势数据
  getSalesTrend: (params) => api.get('/sales/trend', { params }),
  
  // 获取分类统计数据
  getCategoryStats: () => api.get('/sales/category-stats'),
  
  // 上传CSV文件
  uploadCSV: (file) => {
    const formData = new FormData()
    formData.append('file', file)
    return api.post('/sales/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    })
  },
  
  // 查询销售记录（统一使用这个接口）
  querySales: (params) => api.get('/sales/query', { params }),
  
  // 获取销售记录列表（兼容性，实际调用querySales）
  getSalesList: (params) => api.get('/sales/query', { params })
}

export default api 