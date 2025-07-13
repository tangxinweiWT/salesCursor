import api from '@/api'

// API测试工具类
class ApiTester {
  constructor() {
    this.results = []
  }

  // 添加测试结果
  addResult(testName, success, data, error) {
    this.results.push({
      testName,
      success,
      data,
      error,
      timestamp: new Date().toISOString()
    })
  }

  // 测试基础连接
  async testBaseConnection() {
    try {
      console.log('🔍 测试基础连接...')
      const response = await api.get('/')
      console.log('✅ 基础连接成功:', response)
      this.addResult('基础连接', true, response, null)
      return { success: true, data: response }
    } catch (error) {
      console.error('❌ 基础连接失败:', error)
      this.addResult('基础连接', false, null, error)
      return { success: false, error }
    }
  }

  // 测试健康检查
  async testHealthCheck() {
    try {
      console.log('🔍 测试健康检查...')
      const response = await api.get('/health')
      console.log('✅ 健康检查成功:', response)
      this.addResult('健康检查', true, response, null)
      return { success: true, data: response }
    } catch (error) {
      console.error('❌ 健康检查失败:', error)
      this.addResult('健康检查', false, null, error)
      return { success: false, error }
    }
  }

  // 测试API文档
  async testApiDocs() {
    try {
      console.log('🔍 测试API文档...')
      const response = await api.get('/docs')
      console.log('✅ API文档访问成功:', response)
      this.addResult('API文档', true, response, null)
      return { success: true, data: response }
    } catch (error) {
      console.error('❌ API文档访问失败:', error)
      this.addResult('API文档', false, null, error)
      return { success: false, error }
    }
  }

  // 测试销售统计数据
  async testSalesStats() {
    try {
      console.log('🔍 测试销售统计数据...')
      const response = await api.get('/sales/stats')
      console.log('✅ 销售统计数据成功:', response)
      this.addResult('销售统计数据', true, response, null)
      return { success: true, data: response }
    } catch (error) {
      console.error('❌ 销售统计数据失败:', error)
      this.addResult('销售统计数据', false, null, error)
      return { success: false, error }
    }
  }

  // 测试销售趋势数据
  async testSalesTrend() {
    try {
      console.log('🔍 测试销售趋势数据...')
      const response = await api.get('/sales/trend', {
        params: { days: 30 }
      })
      console.log('✅ 销售趋势数据成功:', response)
      this.addResult('销售趋势数据', true, response, null)
      return { success: true, data: response }
    } catch (error) {
      console.error('❌ 销售趋势数据失败:', error)
      this.addResult('销售趋势数据', false, null, error)
      return { success: false, error }
    }
  }

  // 测试分类统计数据
  async testCategoryStats() {
    try {
      console.log('🔍 测试分类统计数据...')
      const response = await api.get('/sales/category-stats')
      console.log('✅ 分类统计数据成功:', response)
      this.addResult('分类统计数据', true, response, null)
      return { success: true, data: response }
    } catch (error) {
      console.error('❌ 分类统计数据失败:', error)
      this.addResult('分类统计数据', false, null, error)
      return { success: false, error }
    }
  }

  // 测试销售记录查询
  async testSalesQuery() {
    try {
      console.log('🔍 测试销售记录查询...')
      const response = await api.get('/sales/query', {
        params: { page: 1, size: 10 }
      })
      console.log('✅ 销售记录查询成功:', response)
      this.addResult('销售记录查询', true, response, null)
      return { success: true, data: response }
    } catch (error) {
      console.error('❌ 销售记录查询失败:', error)
      this.addResult('销售记录查询', false, null, error)
      return { success: false, error }
    }
  }

  // 测试销售记录列表
  async testSalesList() {
    try {
      console.log('🔍 测试销售记录列表...')
      const response = await api.get('/sales/list', {
        params: { page: 1, size: 10 }
      })
      console.log('✅ 销售记录列表成功:', response)
      this.addResult('销售记录列表', true, response, null)
      return { success: true, data: response }
    } catch (error) {
      console.error('❌ 销售记录列表失败:', error)
      this.addResult('销售记录列表', false, null, error)
      return { success: false, error }
    }
  }

  // 测试CSV文件上传（模拟）
  async testCsvUpload() {
    try {
      console.log('🔍 测试CSV文件上传...')
      // 创建一个模拟的CSV文件
      const csvContent = '日期,产品名称,分类,数量,单价,总金额\n2024-01-01,测试产品,电子产品,1,99.99,99.99'
      const blob = new Blob([csvContent], { type: 'text/csv' })
      const file = new File([blob], 'test.csv', { type: 'text/csv' })
      
      const formData = new FormData()
      formData.append('file', file)
      
      const response = await api.post('/sales/upload', formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      })
      console.log('✅ CSV文件上传成功:', response)
      this.addResult('CSV文件上传', true, response, null)
      return { success: true, data: response }
    } catch (error) {
      console.error('❌ CSV文件上传失败:', error)
      this.addResult('CSV文件上传', false, null, error)
      return { success: false, error }
    }
  }

  // 测试数据导出
  async testDataExport() {
    try {
      console.log('🔍 测试数据导出...')
      const response = await api.get('/sales/export', {
        params: { page: 1, size: 10 },
        responseType: 'blob'
      })
      console.log('✅ 数据导出成功:', response)
      this.addResult('数据导出', true, response, null)
      return { success: true, data: response }
    } catch (error) {
      console.error('❌ 数据导出失败:', error)
      this.addResult('数据导出', false, null, error)
      return { success: false, error }
    }
  }

  // 运行所有测试
  async runAllTests() {
    console.log('🚀 开始运行所有API测试...')
    
    const tests = [
      this.testBaseConnection(),
      this.testHealthCheck(),
      this.testApiDocs(),
      this.testSalesStats(),
      this.testSalesTrend(),
      this.testCategoryStats(),
      this.testSalesQuery(),
      this.testSalesList(),
      this.testCsvUpload(),
      this.testDataExport()
    ]

    const results = await Promise.allSettled(tests)
    
    console.log('📊 测试完成，生成报告...')
    return this.generateReport()
  }

  // 生成测试报告
  generateReport() {
    const totalTests = this.results.length
    const passedTests = this.results.filter(r => r.success).length
    const failedTests = totalTests - passedTests

    const report = {
      summary: {
        total: totalTests,
        passed: passedTests,
        failed: failedTests,
        successRate: ((passedTests / totalTests) * 100).toFixed(2) + '%'
      },
      results: this.results,
      recommendations: this.generateRecommendations()
    }

    console.log('📋 测试报告:', report)
    return report
  }

  // 生成改进建议
  generateRecommendations() {
    const recommendations = []
    const failedTests = this.results.filter(r => !r.success)

    failedTests.forEach(test => {
      const error = test.error
      const statusCode = error?.response?.status
      const errorMessage = error?.response?.data?.detail || error?.message

      switch (test.testName) {
        case '基础连接':
          recommendations.push({
            issue: '基础连接失败',
            severity: '高',
            description: '无法连接到后端服务器',
            solution: '检查后端服务器是否启动，确认端口配置'
          })
          break
        case '健康检查':
          recommendations.push({
            issue: '健康检查接口不可用',
            severity: '中',
            description: '健康检查接口返回错误',
            solution: '检查后端健康检查路由配置'
          })
          break
        case '销售统计数据':
          recommendations.push({
            issue: '销售统计数据接口错误',
            severity: '中',
            description: `状态码: ${statusCode}, 错误: ${errorMessage}`,
            solution: '检查销售统计接口实现和数据格式'
          })
          break
        case '销售记录查询':
          recommendations.push({
            issue: '销售记录查询接口错误',
            severity: '高',
            description: `状态码: ${statusCode}, 错误: ${errorMessage}`,
            solution: '检查查询接口参数和数据库连接'
          })
          break
        case 'CSV文件上传':
          recommendations.push({
            issue: 'CSV文件上传接口错误',
            severity: '中',
            description: `状态码: ${statusCode}, 错误: ${errorMessage}`,
            solution: '检查文件上传配置和存储路径'
          })
          break
        default:
          recommendations.push({
            issue: `${test.testName}接口错误`,
            severity: '中',
            description: `状态码: ${statusCode}, 错误: ${errorMessage}`,
            solution: '检查接口实现和参数配置'
          })
      }
    })

    return recommendations
  }
}

export default ApiTester 