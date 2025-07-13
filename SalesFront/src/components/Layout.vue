<template>
  <el-container class="layout-container">
    <!-- 侧边栏 -->
    <el-aside width="250px" class="sidebar">
              <div class="logo">
          <h2>销售数据分析系统</h2>
        </div>
      <el-menu
        :key="activeMenu"
        :default-active="activeMenu"
        background-color="#304156"
        text-color="#bfcbd9"
        active-text-color="#409EFF"
        class="sidebar-menu"
        @select="handleMenuSelect"
      >
        <el-menu-item index="/dashboard" @click="navigateTo('/dashboard')">
          <el-icon><DataBoard /></el-icon>
          <span>数据可视化</span>
        </el-menu-item>
        <el-menu-item index="/upload" @click="navigateTo('/upload')">
          <el-icon><Upload /></el-icon>
          <span>数据上传</span>
        </el-menu-item>
        <el-menu-item index="/query" @click="navigateTo('/query')">
          <el-icon><Search /></el-icon>
          <span>数据查询</span>
        </el-menu-item>
        <el-menu-item index="/test" @click="navigateTo('/test')">
          <el-icon><Tools /></el-icon>
          <span>API测试</span>
        </el-menu-item>
      </el-menu>
    </el-aside>

    <!-- 主内容区 -->
    <el-container>
      <el-header class="header">
        <div class="header-content">
          <h3>{{ currentPageTitle }}</h3>
          <div class="user-info">
            <el-avatar size="small" icon="UserFilled" />
            <span>管理员</span>
          </div>
        </div>
      </el-header>
      
      <el-main class="main-content">
        <router-view />
      </el-main>
    </el-container>
  </el-container>
</template>

<script>
import { computed, ref, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'

export default {
  name: 'Layout',
  setup() {
    const route = useRoute()
    const router = useRouter()
    const activeMenu = ref(route.path)
    
    const currentPageTitle = computed(() => {
      return route.meta.title || '销售数据分析系统'
    })

    // 监听路由变化，更新菜单激活状态
    watch(() => route.path, (newPath) => {
      activeMenu.value = newPath
    }, { immediate: true, flush: 'post' })

    // 处理菜单选择
    const handleMenuSelect = (index) => {
      activeMenu.value = index
    }

    // 导航函数
    const navigateTo = (path) => {
      if (route.path !== path) {
        router.push(path)
      }
    }

    return {
      currentPageTitle,
      activeMenu,
      handleMenuSelect,
      navigateTo
    }
  }
}
</script>

<style scoped>
.layout-container {
  height: 100vh;
}

.sidebar {
  background: #ffffff;
  color: #333333;
  box-shadow: 2px 0 8px rgba(0, 0, 0, 0.06);
  border-right: 1px solid #f0f0f0;
}

.logo {
  height: 64px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #ffffff;
  color: #1890ff;
  border-bottom: 1px solid #f0f0f0;
  margin: 0;
  padding: 0 16px;
}

.logo h2 {
  font-size: 16px;
  font-weight: 600;
  color: #1890ff;
}

.sidebar-menu {
  border-right: none;
  background: #ffffff !important;
}

.header {
  background: #ffffff;
  border-bottom: 1px solid #f0f0f0;
  padding: 0 24px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
}

.header-content {
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.header-content h3 {
  color: #333333;
  font-weight: 500;
  font-size: 18px;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 8px;
  color: #666666;
  padding: 6px 12px;
  background: #f5f5f5;
  border-radius: 6px;
  border: 1px solid #e0e0e0;
}

.main-content {
  background: #fafafa;
  padding: 24px;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .sidebar {
    width: 200px !important;
  }
  
  .header-content h3 {
    font-size: 16px;
  }
}
</style> 