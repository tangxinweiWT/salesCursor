<template>
  <div class="data-query">
    <!-- 查询条件 -->
    <el-card class="query-form" shadow="hover">
      <template #header>
        <div class="card-header">
          <span>查询条件</span>
          <el-button type="primary" size="small" @click="handleQuery">
            <el-icon><Search /></el-icon>
            查询
          </el-button>
        </div>
      </template>
      
      <el-form :model="queryForm" :inline="true" class="query-form-content">
        <el-form-item label="日期范围">
          <el-date-picker
            v-model="queryForm.dateRange"
            type="daterange"
            range-separator="至"
            start-placeholder="开始日期"
            end-placeholder="结束日期"
            format="YYYY-MM-DD"
            value-format="YYYY-MM-DD"
            style="width: 240px"
          />
        </el-form-item>
        
        <el-form-item label="产品名称">
          <el-input
            v-model="queryForm.product"
            placeholder="请输入产品名称"
            style="width: 200px"
            clearable
          />
        </el-form-item>
        
        <el-form-item label="产品分类">
          <el-select
            v-model="queryForm.category"
            placeholder="请选择分类"
            style="width: 150px"
            clearable
          >
            <el-option
              v-for="category in categoryOptions"
              :key="category"
              :label="category"
              :value="category"
            />
          </el-select>
        </el-form-item>
        
        <el-form-item label="金额范围">
          <el-input-number
            v-model="queryForm.minAmount"
            placeholder="最小金额"
            style="width: 120px"
            :min="0"
            :precision="2"
          />
          <span style="margin: 0 8px">-</span>
          <el-input-number
            v-model="queryForm.maxAmount"
            placeholder="最大金额"
            style="width: 120px"
            :min="0"
            :precision="2"
          />
        </el-form-item>
        
        <el-form-item label="数量范围">
          <el-input-number
            v-model="queryForm.minQuantity"
            placeholder="最小数量"
            style="width: 120px"
            :min="0"
            :precision="0"
          />
          <span style="margin: 0 8px">-</span>
          <el-input-number
            v-model="queryForm.maxQuantity"
            placeholder="最大数量"
            style="width: 120px"
            :min="0"
            :precision="0"
          />
        </el-form-item>
      </el-form>
      
      <div class="form-actions">
        <el-button @click="resetQuery">重置</el-button>
        <el-button type="primary" @click="handleQuery" :loading="loading">
          查询
        </el-button>
        <el-button type="success" @click="exportData" :disabled="!hasData">
          导出数据
        </el-button>
      </div>
    </el-card>

    <!-- 查询结果 -->
    <el-card class="query-results" shadow="hover">
      <template #header>
        <div class="card-header">
          <span>查询结果</span>
          <div class="result-info">
            <span>共找到 {{ total }} 条记录</span>
            <el-button type="text" size="small" @click="refreshData">
              刷新
            </el-button>
          </div>
        </div>
      </template>
      
      <el-table
        :data="tableData"
        stripe
        style="width: 100%"
        v-loading="loading"
        @sort-change="handleSortChange"
      >
        <el-table-column prop="sales_date" label="日期" width="120" sortable>
          <template #default="scope">
            {{ formatDate(scope.row.sales_date) }}
          </template>
        </el-table-column>
        <el-table-column prop="order_id" label="订单号" width="120" />
        <el-table-column prop="product_name" label="产品名称" min-width="150" />
        <el-table-column prop="category" label="分类" width="120" />
        <el-table-column prop="customer_name" label="客户姓名" width="120" />
        <el-table-column prop="region" label="地区" width="100" />
        <el-table-column prop="quantity" label="数量" width="80" sortable />
        <el-table-column prop="unit_price" label="单价" width="120" sortable>
          <template #default="scope">
            ¥{{ scope.row.unit_price?.toFixed(2) }}
          </template>
        </el-table-column>
        <el-table-column prop="sales_amount" label="总金额" width="120" sortable>
          <template #default="scope">
            ¥{{ scope.row.sales_amount?.toLocaleString() }}
          </template>
        </el-table-column>
        <el-table-column prop="sales_person" label="销售员" width="100" />
        <el-table-column prop="payment_method" label="支付方式" width="100" />
        <el-table-column label="操作" width="120" fixed="right">
          <template #default="scope">
            <el-button type="text" size="small" @click="viewDetail(scope.row)">
              查看详情
            </el-button>
          </template>
        </el-table-column>
      </el-table>
      
      <!-- 分页 -->
      <div class="pagination-wrapper">
        <el-pagination
          v-model:current-page="currentPage"
          v-model:page-size="pageSize"
          :page-sizes="[10, 20, 50, 100]"
          :total="total"
          layout="total, sizes, prev, pager, next, jumper"
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
        />
      </div>
    </el-card>

    <!-- 详情对话框 -->
    <el-dialog
      v-model="detailVisible"
      title="销售记录详情"
      width="600px"
      :before-close="handleCloseDetail"
    >
      <el-descriptions :column="2" border v-if="currentDetail">
        <el-descriptions-item label="订单号">{{ currentDetail.order_id }}</el-descriptions-item>
        <el-descriptions-item label="销售日期">{{ formatDate(currentDetail.sales_date) }}</el-descriptions-item>
        <el-descriptions-item label="产品名称">{{ currentDetail.product_name }}</el-descriptions-item>
        <el-descriptions-item label="产品分类">{{ currentDetail.category }}</el-descriptions-item>
        <el-descriptions-item label="客户姓名">{{ currentDetail.customer_name }}</el-descriptions-item>
        <el-descriptions-item label="地区">{{ currentDetail.region }}</el-descriptions-item>
        <el-descriptions-item label="数量">{{ currentDetail.quantity }}</el-descriptions-item>
        <el-descriptions-item label="单价">¥{{ currentDetail.unit_price?.toFixed(2) }}</el-descriptions-item>
        <el-descriptions-item label="总金额">¥{{ currentDetail.sales_amount?.toLocaleString() }}</el-descriptions-item>
        <el-descriptions-item label="销售员">{{ currentDetail.sales_person }}</el-descriptions-item>
        <el-descriptions-item label="支付方式">{{ currentDetail.payment_method }}</el-descriptions-item>
      </el-descriptions>
      
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="detailVisible = false">关闭</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script>
import { ref, reactive, computed, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { salesAPI } from '@/api'

export default {
  name: 'DataQuery',
  setup() {
    const loading = ref(false)
    const tableData = ref([])
    const total = ref(0)
    const currentPage = ref(1)
    const pageSize = ref(20)
    const detailVisible = ref(false)
    const currentDetail = ref(null)
    
    const queryForm = reactive({
      dateRange: [],
      product: '',
      category: '',
      minAmount: null,
      maxAmount: null,
      minQuantity: null,
      maxQuantity: null
    })
    
    const categoryOptions = ref([
      '电子产品',
      '办公用品'
    ])
    
    const hasData = computed(() => {
      return tableData.value.length > 0
    })
    
    // 处理查询
    const handleQuery = async () => {
      try {
        loading.value = true
        currentPage.value = 1
        
        const params = {
          page: currentPage.value,
          size: pageSize.value,
          ...buildQueryParams()
        }
        
        console.log('查询参数:', params)
        const result = await salesAPI.querySales(params)
        console.log('查询结果:', result)
        
        tableData.value = result.data || []
        total.value = result.pagination?.total || result.total || 0
        
        if (tableData.value.length === 0) {
          ElMessage.info('未找到符合条件的记录')
        }
        
      } catch (error) {
        console.error('查询失败:', error)
        console.error('错误详情:', error.response?.data || error.message)
        ElMessage.error('查询失败：' + (error.response?.data?.detail || error.message || '未知错误'))
      } finally {
        loading.value = false
      }
    }
    
    // 格式化日期
    const formatDate = (dateString) => {
      if (!dateString) return ''
      const date = new Date(dateString)
      return date.toLocaleDateString('zh-CN')
    }
    
    // 构建查询参数
    const buildQueryParams = () => {
      const params = {}
      
      if (queryForm.dateRange && queryForm.dateRange.length === 2) {
        params.start_date = queryForm.dateRange[0]
        params.end_date = queryForm.dateRange[1]
      }
      
      if (queryForm.product) {
        params.product_name = queryForm.product
      }
      
      if (queryForm.category) {
        params.category = queryForm.category
      }
      
      if (queryForm.minAmount !== null) {
        params.min_sales_amount = queryForm.minAmount
      }
      
      if (queryForm.maxAmount !== null) {
        params.max_sales_amount = queryForm.maxAmount
      }
      
      if (queryForm.minQuantity !== null) {
        params.min_quantity = queryForm.minQuantity
      }
      
      if (queryForm.maxQuantity !== null) {
        params.max_quantity = queryForm.maxQuantity
      }
      
      return params
    }
    
    // 重置查询
    const resetQuery = () => {
      Object.assign(queryForm, {
        dateRange: [],
        product: '',
        category: '',
        minAmount: null,
        maxAmount: null,
        minQuantity: null,
        maxQuantity: null
      })
      currentPage.value = 1
      tableData.value = []
      total.value = 0
    }
    
    // 刷新数据
    const refreshData = () => {
      if (hasData.value) {
        handleQuery()
      }
    }
    
    // 处理分页大小变化
    const handleSizeChange = (size) => {
      pageSize.value = size
      handleQuery()
    }
    
    // 处理当前页变化
    const handleCurrentChange = (page) => {
      currentPage.value = page
      handleQuery()
    }
    
    // 处理排序变化
    const handleSortChange = ({ prop, order }) => {
      // 这里可以添加排序逻辑
      console.log('排序变化:', prop, order)
    }
    
    // 查看详情
    const viewDetail = (row) => {
      currentDetail.value = row
      detailVisible.value = true
    }
    
    // 关闭详情
    const handleCloseDetail = () => {
      detailVisible.value = false
      currentDetail.value = null
    }
    
    // 导出数据
    const exportData = () => {
      try {
        const params = buildQueryParams()
        const queryString = new URLSearchParams(params).toString()
        const url = `/api/sales/export?${queryString}`
        
        const link = document.createElement('a')
        link.href = url
        link.download = `sales_data_${new Date().toISOString().split('T')[0]}.csv`
        document.body.appendChild(link)
        link.click()
        document.body.removeChild(link)
        
        ElMessage.success('数据导出成功')
      } catch (error) {
        ElMessage.error('数据导出失败')
      }
    }
    
    // 加载初始数据
    const loadInitialData = async () => {
      try {
        loading.value = true
        const params = {
          page: 1,
          size: pageSize.value
        }
        console.log('初始数据加载参数:', params)
        const result = await salesAPI.getSalesList(params)
        console.log('初始数据加载结果:', result)
        
        tableData.value = result.data || []
        total.value = result.pagination?.total || result.total || 0
        
        if (tableData.value.length === 0) {
          console.log('初始数据为空，可能的原因：1. 后端接口问题 2. 数据格式问题 3. 接口路径问题')
        }
      } catch (error) {
        console.error('加载初始数据失败:', error)
        console.error('错误详情:', error.response?.data || error.message)
        ElMessage.error('加载初始数据失败：' + (error.response?.data?.detail || error.message || '未知错误'))
      } finally {
        loading.value = false
      }
    }
    
    onMounted(() => {
      loadInitialData()
    })
    
    return {
      loading,
      tableData,
      total,
      currentPage,
      pageSize,
      detailVisible,
      currentDetail,
      queryForm,
      categoryOptions,
      hasData,
      formatDate,
      handleQuery,
      resetQuery,
      refreshData,
      handleSizeChange,
      handleCurrentChange,
      handleSortChange,
      viewDetail,
      handleCloseDetail,
      exportData
    }
  }
}
</script>

<style scoped>
.data-query {
  padding: 0;
}

.query-form,
.query-results {
  margin-bottom: 24px;
  transition: all 0.2s ease;
  border: 1px solid #f0f0f0;
}

.query-form:hover,
.query-results:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1) !important;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 20px;
  background: #fafafa;
  border-bottom: 1px solid #f0f0f0;
  margin: -20px -20px 20px -20px;
}

.card-header span {
  font-weight: 600;
  color: #333333;
  font-size: 16px;
}

.query-form-content {
  margin-bottom: 24px;
  padding: 20px;
  background: #fafafa;
  border-radius: 8px;
  border: 1px solid #f0f0f0;
}

.form-actions {
  display: flex;
  gap: 16px;
  justify-content: center;
  padding: 20px;
  background: #fafafa;
  border-radius: 8px;
  margin-top: 24px;
  border: 1px solid #f0f0f0;
}

.result-info {
  display: flex;
  align-items: center;
  gap: 12px;
  color: #666666;
  font-weight: 500;
  padding: 8px 16px;
  background: #f6ffed;
  border-radius: 6px;
  border: 1px solid #b7eb8f;
}

.pagination-wrapper {
  margin-top: 24px;
  display: flex;
  justify-content: center;
  padding: 16px;
  background: #fafafa;
  border-radius: 8px;
  border: 1px solid #f0f0f0;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .query-form-content .el-form-item {
    display: block;
    margin-bottom: 15px;
  }
  
  .query-form-content .el-form-item .el-form-item__label {
    display: block;
    margin-bottom: 5px;
  }
  
  .form-actions {
    flex-direction: column;
  }
  
  .form-actions .el-button {
    width: 100%;
  }
}
</style> 