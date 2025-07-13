<template>
  <div id="app">
    <router-view />
  </div>
</template>

<script>
export default {
  name: 'App'
}
</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: 'Helvetica Neue', Helvetica, 'PingFang SC', 'Hiragino Sans GB', 'Microsoft YaHei', '微软雅黑', Arial, sans-serif;
  background: #fafafa;
  min-height: 100vh;
}

#app {
  min-height: 100vh;
}

/* 全局圆角样式 */
.el-card {
  border-radius: 12px !important;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06) !important;
  border: 1px solid #f0f0f0 !important;
  background: #ffffff !important;
  transition: all 0.2s ease !important;
}

.el-card:hover {
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1) !important;
}

.el-button {
  border-radius: 8px !important;
  font-weight: 500 !important;
  transition: all 0.2s ease !important;
  border: 1px solid #e0e0e0 !important;
}

.el-button:hover {
  transform: translateY(-1px) !important;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1) !important;
}

.el-button--primary {
  background: #1890ff !important;
  border-color: #1890ff !important;
}

.el-button--success {
  background: #52c41a !important;
  border-color: #52c41a !important;
}

.el-input__wrapper {
  border-radius: 8px !important;
  border: 1px solid #d9d9d9 !important;
  box-shadow: none !important;
}

.el-input__wrapper:hover {
  border-color: #40a9ff !important;
}

.el-input__wrapper.is-focus {
  border-color: #1890ff !important;
  box-shadow: 0 0 0 2px rgba(24, 144, 255, 0.2) !important;
}

.el-select .el-input__wrapper {
  border-radius: 8px !important;
}

.el-table {
  border-radius: 8px !important;
  overflow: hidden !important;
  border: 1px solid #f0f0f0 !important;
}

.el-pagination {
  border-radius: 8px !important;
  padding: 12px !important;
  background: #ffffff !important;
  border: 1px solid #f0f0f0 !important;
}

.el-menu-item {
  border-radius: 8px !important;
  margin: 2px 8px !important;
  transition: all 0.2s ease !important;
  color: #666666 !important;
}

.el-menu-item:hover {
  background: #f5f5f5 !important;
  color: #1890ff !important;
}

.el-menu-item.is-active {
  background: #e6f7ff !important;
  color: #1890ff !important;
  border-right: 3px solid #1890ff !important;
}
</style> 