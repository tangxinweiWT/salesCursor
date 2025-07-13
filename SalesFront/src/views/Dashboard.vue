<template>
  <div class="dashboard">
    <!-- 统计卡片 -->
    <el-row :gutter="20" class="stats-cards">
      <el-col :xs="24" :sm="12" :md="6" v-for="(stat, index) in statsData" :key="stat.title">
        <el-card class="stat-card" shadow="hover">
          <div class="stat-content">
            <div class="stat-icon" :style="{ backgroundColor: stat.color }">
              <el-icon><component :is="stat.icon" /></el-icon>
            </div>
            <div class="stat-info">
              <div class="stat-value">{{ stat.value }}</div>
              <div class="stat-title">{{ stat.title }}</div>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <!-- 图表区域 -->
    <el-row :gutter="20" class="charts-section">
      <el-col :xs="24" :lg="12">
        <el-card class="chart-card" shadow="hover">
          <template #header>
            <div class="card-header">
              <span>销售趋势</span>
              <el-select v-model="trendPeriod" size="small" style="width: 120px">
                <el-option label="最近7天" value="7" />
                <el-option label="最近30天" value="30" />
                <el-option label="最近90天" value="90" />
              </el-select>
            </div>
          </template>
          <div class="chart-container">
            <v-chart :option="salesTrendOption" style="height: 300px" />
          </div>
        </el-card>
      </el-col>
      
      <el-col :xs="24" :lg="12">
        <el-card class="chart-card" shadow="hover">
          <template #header>
            <div class="card-header">
              <span>分类统计</span>
            </div>
          </template>
          <div class="chart-container">
            <v-chart :option="categoryOption" style="height: 300px" />
          </div>
        </el-card>
      </el-col>
    </el-row>

    <!-- 最近销售记录 -->
    <el-card class="recent-sales" shadow="hover">
      <template #header>
        <div class="card-header">
          <span>最近销售记录</span>
          <el-button type="primary" size="small" @click="$router.push('/query')">
            查看更多
          </el-button>
        </div>
      </template>
      <el-table :data="recentSales" stripe style="width: 100%">
        <el-table-column prop="sales_date" label="日期" width="120">
          <template #default="scope">
            {{ formatDate(scope.row.sales_date) }}
          </template>
        </el-table-column>
        <el-table-column prop="product_name" label="产品" />
        <el-table-column prop="category" label="分类" width="120" />
        <el-table-column prop="sales_amount" label="金额" width="120">
          <template #default="scope">
            ¥{{ scope.row.sales_amount?.toLocaleString() }}
          </template>
        </el-table-column>
        <el-table-column prop="quantity" label="数量" width="100" />
      </el-table>
    </el-card>
  </div>
</template>

<script>
import { ref, reactive, onMounted, watch } from 'vue'
import { use } from 'echarts/core'
import { CanvasRenderer } from 'echarts/renderers'
import { LineChart, PieChart } from 'echarts/charts'
import { GridComponent, TooltipComponent, LegendComponent } from 'echarts/components'
import VChart from 'vue-echarts'
import { salesAPI } from '@/api'

use([CanvasRenderer, LineChart, PieChart, GridComponent, TooltipComponent, LegendComponent])

export default {
  name: 'Dashboard',
  components: {
    VChart
  },
  setup() {
    const trendPeriod = ref('30')
    const statsData = ref([
      { title: '总销售额', value: '¥0', icon: 'Money', color: '#67C23A' },
      { title: '订单数量', value: '0', icon: 'ShoppingCart', color: '#409EFF' },
      { title: '产品种类', value: '0', icon: 'Goods', color: '#E6A23C' },
      { title: '平均订单', value: '¥0', icon: 'TrendCharts', color: '#F56C6C' }
    ])
    
    const recentSales = ref([])
    
    // 格式化日期
    const formatDate = (dateString) => {
      if (!dateString) return ''
      const date = new Date(dateString)
      return date.toLocaleDateString('zh-CN')
    }
    
    // 销售趋势图表配置
    const salesTrendOption = ref({
      tooltip: {
        trigger: 'axis'
      },
      legend: {
        data: ['销售额', '订单数']
      },
      grid: {
        left: '3%',
        right: '4%',
        bottom: '3%',
        containLabel: true
      },
      xAxis: {
        type: 'category',
        boundaryGap: false,
        data: ['1月', '2月', '3月', '4月', '5月', '6月']
      },
      yAxis: [
        {
          type: 'value',
          name: '销售额',
          position: 'left'
        },
        {
          type: 'value',
          name: '订单数',
          position: 'right'
        }
      ],
      series: [
        {
          name: '销售额',
          type: 'line',
          data: [12000, 15000, 18000, 22000, 25000, 28000],
          smooth: true,
          itemStyle: { color: '#409EFF' }
        },
        {
          name: '订单数',
          type: 'line',
          yAxisIndex: 1,
          data: [10, 15, 18, 22, 25, 28],
          smooth: true,
          itemStyle: { color: '#67C23A' }
        }
      ]
    })
    
    // 分类统计图表配置
    const categoryOption = ref({
      tooltip: {
        trigger: 'item',
        formatter: '{a} <br/>{b}: {c} ({d}%)'
      },
      legend: {
        orient: 'vertical',
        left: 'left'
      },
      series: [
        {
          name: '销售分类',
          type: 'pie',
          radius: '50%',
          data: [
            { name: '电子产品', value: 45000 },
            { name: '办公用品', value: 28000 }
          ],
          emphasis: {
            itemStyle: {
              shadowBlur: 10,
              shadowOffsetX: 0,
              shadowColor: 'rgba(0, 0, 0, 0.5)'
            }
          }
        }
      ]
    })
    
    // 加载统计数据
    const loadStats = async () => {
      try {
        console.log('开始加载统计数据...')
        const stats = await salesAPI.getSalesStats()
        console.log('统计数据响应:', stats)
        
        // 如果接口返回的数据结构不同，尝试适配
        const totalSales = stats.totalSales || stats.total_sales || 0
        const totalOrders = stats.totalOrders || stats.total_orders || 0
        const productCount = stats.productCount || stats.product_count || 0
        const avgOrder = stats.avgOrder || stats.avg_order || 0
        
        statsData.value = [
          { title: '总销售额', value: `¥${totalSales.toLocaleString()}`, icon: 'Money', color: '#67C23A' },
          { title: '订单数量', value: totalOrders.toString(), icon: 'ShoppingCart', color: '#409EFF' },
          { title: '产品种类', value: productCount.toString(), icon: 'Goods', color: '#E6A23C' },
          { title: '平均订单', value: `¥${avgOrder.toLocaleString()}`, icon: 'TrendCharts', color: '#F56C6C' }
        ]
        console.log('更新后的统计数据:', statsData.value)
      } catch (error) {
        console.error('加载统计数据失败:', error)
        console.error('错误详情:', error.response?.data || error.message)
        // 设置默认数据
        statsData.value = [
          { title: '总销售额', value: '¥0', icon: 'Money', color: '#67C23A' },
          { title: '订单数量', value: '0', icon: 'ShoppingCart', color: '#409EFF' },
          { title: '产品种类', value: '0', icon: 'Goods', color: '#E6A23C' },
          { title: '平均订单', value: '¥0', icon: 'TrendCharts', color: '#F56C6C' }
        ]
      }
    }
    
    // 加载销售趋势
    const loadSalesTrend = async () => {
      try {
        console.log('开始加载销售趋势...')
        const trend = await salesAPI.getSalesTrend({ days: trendPeriod.value })
        console.log('销售趋势响应:', trend)
        
        // 如果接口返回的数据结构不同，尝试适配
        const dates = trend.dates || trend.date_list || ['1月', '2月', '3月', '4月', '5月', '6月']
        const sales = trend.sales || trend.sales_amount || [12000, 15000, 18000, 22000, 25000, 28000]
        const orders = trend.orders || trend.order_count || [10, 15, 18, 22, 25, 28]
        
        // 创建新的配置对象
        salesTrendOption.value = {
          tooltip: {
            trigger: 'axis'
          },
          legend: {
            data: ['销售额', '订单数']
          },
          grid: {
            left: '3%',
            right: '4%',
            bottom: '3%',
            containLabel: true
          },
          xAxis: {
            type: 'category',
            boundaryGap: false,
            data: dates
          },
          yAxis: [
            {
              type: 'value',
              name: '销售额',
              position: 'left'
            },
            {
              type: 'value',
              name: '订单数',
              position: 'right'
            }
          ],
          series: [
            {
              name: '销售额',
              type: 'line',
              data: sales,
              smooth: true,
              itemStyle: { color: '#409EFF' }
            },
            {
              name: '订单数',
              type: 'line',
              yAxisIndex: 1,
              data: orders,
              smooth: true,
              itemStyle: { color: '#67C23A' }
            }
          ]
        }
        
        console.log('更新后的销售趋势配置:', salesTrendOption.value)
      } catch (error) {
        console.error('加载销售趋势失败:', error)
        console.error('错误详情:', error.response?.data || error.message)
        // 保持默认测试数据
      }
    }
    
    // 加载分类统计
    const loadCategoryStats = async () => {
      try {
        console.log('开始加载分类统计...')
        const categories = await salesAPI.getCategoryStats()
        console.log('分类统计响应:', categories)
        
        // 如果接口返回的数据结构不同，尝试适配
        const categoryData = categories.map(item => ({
          name: item.category || item.name,
          value: item.sales || item.value || item.amount
        })) || [
          { name: '电子产品', value: 45000 },
          { name: '办公用品', value: 28000 }
        ]
        
        // 创建新的配置对象
        categoryOption.value = {
          tooltip: {
            trigger: 'item',
            formatter: '{a} <br/>{b}: {c} ({d}%)'
          },
          legend: {
            orient: 'vertical',
            left: 'left'
          },
          series: [
            {
              name: '销售分类',
              type: 'pie',
              radius: '50%',
              data: categoryData,
              emphasis: {
                itemStyle: {
                  shadowBlur: 10,
                  shadowOffsetX: 0,
                  shadowColor: 'rgba(0, 0, 0, 0.5)'
                }
              }
            }
          ]
        }
        
        console.log('更新后的分类统计配置:', categoryOption.value)
      } catch (error) {
        console.error('加载分类统计失败:', error)
        console.error('错误详情:', error.response?.data || error.message)
        // 保持默认测试数据
      }
    }
    
    // 加载最近销售记录
    const loadRecentSales = async () => {
      try {
        console.log('开始加载最近销售记录...')
        const sales = await salesAPI.getSalesList({ limit: 10 })
        console.log('最近销售记录响应:', sales)
        recentSales.value = sales.data || []
        console.log('更新后的最近销售记录:', recentSales.value)
      } catch (error) {
        console.error('加载最近销售记录失败:', error)
        console.error('错误详情:', error.response?.data || error.message)
        // 设置默认数据
        recentSales.value = []
      }
    }
    
    // 监听趋势周期变化
    watch(trendPeriod, () => {
      loadSalesTrend()
    })
    
    onMounted(() => {
      console.log('Dashboard组件已挂载')
      
      // 延迟加载数据，确保DOM完全渲染
      setTimeout(() => {
        loadStats()
        loadSalesTrend()
        loadCategoryStats()
        loadRecentSales()
        
        // 添加测试数据用于调试
        setTimeout(() => {
          console.log('当前统计数据:', statsData.value)
          console.log('当前最近销售记录:', recentSales.value)
          console.log('当前销售趋势配置:', salesTrendOption.value)
          console.log('当前分类统计配置:', categoryOption.value)
        }, 1000)
      }, 100)
    })
    
    return {
      trendPeriod,
      statsData,
      recentSales,
      salesTrendOption,
      categoryOption,
      formatDate
    }
  }
}
</script>

<style scoped>
.dashboard {
  padding: 0;
}

.stats-cards {
  margin-bottom: 20px;
}

.stat-card {
  margin-bottom: 20px;
  transition: all 0.2s ease;
  border: 1px solid #f0f0f0;
}

.stat-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1) !important;
}

.stat-content {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 16px;
}

.stat-icon {
  width: 56px;
  height: 56px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 24px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.stat-info {
  flex: 1;
}

.stat-value {
  font-size: 24px;
  font-weight: 600;
  color: #1890ff;
  margin-bottom: 4px;
}

.stat-title {
  font-size: 14px;
  color: #666666;
  font-weight: 500;
}

.charts-section {
  margin-bottom: 20px;
}

.chart-card {
  margin-bottom: 20px;
  transition: all 0.2s ease;
  border: 1px solid #f0f0f0;
}

.chart-card:hover {
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

.chart-container {
  width: 100%;
  padding: 16px;
}

.recent-sales {
  margin-bottom: 20px;
  transition: all 0.2s ease;
  border: 1px solid #f0f0f0;
}

.recent-sales:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1) !important;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .stat-content {
    flex-direction: column;
    text-align: center;
    gap: 12px;
  }
  
  .stat-icon {
    width: 50px;
    height: 50px;
    font-size: 20px;
  }
  
  .stat-value {
    font-size: 20px;
  }
}
</style> 