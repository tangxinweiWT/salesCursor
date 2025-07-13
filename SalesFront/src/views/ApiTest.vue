<template>
  <div class="api-test">
    <el-card class="test-card" shadow="hover">
      <template #header>
        <div class="card-header">
          <span>API接口测试</span>
        </div>
      </template>
      
      <div class="test-section">
        <h3>后端连接测试</h3>
        <el-button @click="testBackendConnection" :loading="testing">
          测试后端连接
        </el-button>
        <div v-if="connectionResult" class="result">
          <pre>{{ connectionResult }}</pre>
        </div>
      </div>
      
      <div class="test-section">
        <h3>销售数据接口测试</h3>
        <el-button @click="testSalesAPI" :loading="testing">
          测试销售数据接口
        </el-button>
        <div v-if="salesResult" class="result">
          <pre>{{ salesResult }}</pre>
        </div>
      </div>
      
      <div class="test-section">
        <h3>手动API调用</h3>
        <el-input
          v-model="apiUrl"
          placeholder="输入API路径，如: /sales/query"
          style="margin-bottom: 10px"
        />
        <el-button @click="testCustomAPI" :loading="testing">
          测试自定义API
        </el-button>
        <div v-if="customResult" class="result">
          <pre>{{ customResult }}</pre>
        </div>
      </div>

      <div class="test-section">
        <h3>完整API测试</h3>
        <el-button type="primary" @click="runFullApiTest" :loading="testing">
          运行完整API测试
        </el-button>
        <p style="margin-top: 10px; color: #666; font-size: 14px;">
          此测试将检查所有后端接口，包括：基础连接、健康检查、API文档、销售统计、趋势数据、分类统计、查询接口、上传接口等
        </p>
      </div>

      <!-- 测试报告 -->
      <div v-if="testReport" class="test-section">
        <h3>测试报告</h3>
        <div class="report-summary">
          <el-row :gutter="20">
            <el-col :span="6">
              <div class="summary-card">
                <div class="summary-number">{{ testReport.summary.total }}</div>
                <div class="summary-label">总测试数</div>
              </div>
            </el-col>
            <el-col :span="6">
              <div class="summary-card success">
                <div class="summary-number">{{ testReport.summary.passed }}</div>
                <div class="summary-label">通过</div>
              </div>
            </el-col>
            <el-col :span="6">
              <div class="summary-card error">
                <div class="summary-number">{{ testReport.summary.failed }}</div>
                <div class="summary-label">失败</div>
              </div>
            </el-col>
            <el-col :span="6">
              <div class="summary-card">
                <div class="summary-number">{{ testReport.summary.successRate }}</div>
                <div class="summary-label">成功率</div>
              </div>
            </el-col>
          </el-row>
        </div>

        <!-- 详细结果 -->
        <div class="detailed-results">
          <h4>详细测试结果</h4>
          <el-table :data="testReport.results" stripe style="width: 100%">
            <el-table-column prop="testName" label="测试项目" width="150" />
            <el-table-column prop="success" label="状态" width="100">
              <template #default="scope">
                <el-tag :type="scope.row.success ? 'success' : 'danger'">
                  {{ scope.row.success ? '通过' : '失败' }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="timestamp" label="时间" width="180" />
            <el-table-column label="详情">
              <template #default="scope">
                <div v-if="scope.row.success">
                  <pre style="font-size: 12px; color: #67C23A;">{{ JSON.stringify(scope.row.data, null, 2) }}</pre>
                </div>
                <div v-else>
                  <pre style="font-size: 12px; color: #F56C6C;">{{ JSON.stringify(scope.row.error?.response?.data || scope.row.error?.message, null, 2) }}</pre>
                </div>
              </template>
            </el-table-column>
          </el-table>
        </div>

        <!-- 改进建议 -->
        <div v-if="testReport.recommendations.length > 0" class="recommendations">
          <h4>改进建议</h4>
          <el-alert
            v-for="(rec, index) in testReport.recommendations"
            :key="index"
            :title="rec.issue"
            :type="rec.severity === '高' ? 'error' : 'warning'"
            :description="rec.description + ' | 解决方案: ' + rec.solution"
            show-icon
            style="margin-bottom: 10px"
          />
        </div>
      </div>
    </el-card>
  </div>
</template>

<script>
import { ref } from 'vue'
import { ElMessage } from 'element-plus'
import api from '@/api'
import ApiTester from '@/utils/apiTester'

export default {
  name: 'ApiTest',
  setup() {
    const testing = ref(false)
    const connectionResult = ref('')
    const salesResult = ref('')
    const customResult = ref('')
    const apiUrl = ref('/sales/query')
    const testReport = ref(null)
    const apiTester = new ApiTester()
    
    // 测试后端连接
    const testBackendConnection = async () => {
      try {
        testing.value = true
        connectionResult.value = '测试中...'
        
        const response = await api.get('/')
        connectionResult.value = JSON.stringify(response, null, 2)
        ElMessage.success('后端连接成功')
      } catch (error) {
        connectionResult.value = `连接失败: ${error.message}\n状态码: ${error.response?.status}\n响应数据: ${JSON.stringify(error.response?.data, null, 2)}`
        ElMessage.error('后端连接失败')
      } finally {
        testing.value = false
      }
    }
    
    // 测试销售数据接口
    const testSalesAPI = async () => {
      try {
        testing.value = true
        salesResult.value = '测试中...'
        
        const response = await api.get('/sales/query', {
          params: { page: 1, size: 10 }
        })
        salesResult.value = JSON.stringify(response, null, 2)
        ElMessage.success('销售数据接口测试成功')
      } catch (error) {
        salesResult.value = `接口失败: ${error.message}\n状态码: ${error.response?.status}\n响应数据: ${JSON.stringify(error.response?.data, null, 2)}`
        ElMessage.error('销售数据接口测试失败')
      } finally {
        testing.value = false
      }
    }
    
    // 测试自定义API
    const testCustomAPI = async () => {
      try {
        testing.value = true
        customResult.value = '测试中...'
        
        const response = await api.get(apiUrl.value)
        customResult.value = JSON.stringify(response, null, 2)
        ElMessage.success('自定义API测试成功')
      } catch (error) {
        customResult.value = `接口失败: ${error.message}\n状态码: ${error.response?.status}\n响应数据: ${JSON.stringify(error.response?.data, null, 2)}`
        ElMessage.error('自定义API测试失败')
      } finally {
        testing.value = false
      }
    }

    // 运行完整API测试
    const runFullApiTest = async () => {
      try {
        testing.value = true
        testReport.value = null
        ElMessage.info('开始运行完整API测试...')
        
        const report = await apiTester.runAllTests()
        testReport.value = report
        
        if (report.summary.failed === 0) {
          ElMessage.success('所有API测试通过！')
        } else {
          ElMessage.warning(`测试完成，${report.summary.failed}个接口存在问题`)
        }
      } catch (error) {
        console.error('API测试失败:', error)
        ElMessage.error('API测试执行失败')
      } finally {
        testing.value = false
      }
    }
    
    return {
      testing,
      connectionResult,
      salesResult,
      customResult,
      apiUrl,
      testReport,
      testBackendConnection,
      testSalesAPI,
      testCustomAPI,
      runFullApiTest
    }
  }
}
</script>

<style scoped>
.api-test {
  padding: 20px;
}

.test-card {
  max-width: 800px;
  margin: 0 auto;
}

.test-section {
  margin-bottom: 24px;
  padding: 20px;
  background: #ffffff;
  border-radius: 8px;
  border: 1px solid #f0f0f0;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
  transition: all 0.2s ease;
}

.test-section:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
}

.test-section h3 {
  margin-bottom: 16px;
  color: #333333;
  font-weight: 600;
  font-size: 16px;
}

.result {
  margin-top: 16px;
  padding: 16px;
  background: #fafafa;
  border-radius: 8px;
  border: 1px solid #f0f0f0;
}

.result pre {
  margin: 0;
  white-space: pre-wrap;
  word-wrap: break-word;
  font-family: 'Courier New', monospace;
  font-size: 12px;
  color: #333333;
  line-height: 1.5;
}

.report-summary {
  margin-bottom: 20px;
}

.summary-card {
  text-align: center;
  padding: 20px;
  background: #ffffff;
  border-radius: 8px;
  border: 1px solid #f0f0f0;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
  transition: all 0.2s ease;
}

.summary-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
}

.summary-card.success {
  background: #f6ffed;
  border-color: #b7eb8f;
}

.summary-card.error {
  background: #fff2f0;
  border-color: #ffccc7;
}

.summary-number {
  font-size: 24px;
  font-weight: 600;
  color: #1890ff;
  margin-bottom: 4px;
}

.summary-label {
  font-size: 14px;
  color: #666666;
  font-weight: 500;
}

.detailed-results {
  margin-bottom: 20px;
}

.detailed-results h4 {
  margin-bottom: 16px;
  color: #333333;
  font-weight: 600;
  font-size: 16px;
}

.recommendations h4 {
  margin-bottom: 16px;
  color: #333333;
  font-weight: 600;
  font-size: 16px;
}
</style> 