# 销售数据分析系统前端

基于Vue.js 3 + Element Plus的销售数据分析系统前端项目。

## 功能特性

- 📊 **数据可视化展示**：展示销售趋势和分类统计数据
- 📁 **数据上传功能**：支持CSV文件的上传和处理
- 🔍 **数据查询页面**：支持用户按多个条件查询销售记录
- 📱 **响应式布局**：确保在各种设备上实现良好的显示效果

## 技术栈

- Vue.js 3
- Vue Router 4
- Element Plus
- ECharts
- Axios
- Vite

## 项目结构

```
src/
├── api/           # API接口配置
├── components/    # 公共组件
├── router/        # 路由配置
├── views/         # 页面组件
├── App.vue        # 根组件
└── main.js        # 入口文件
```

## 快速开始

### 安装依赖

```bash
npm install
```

### 开发环境运行

```bash
npm run dev
```

### 生产环境构建

```bash
npm run build
```

### 预览构建结果

```bash
npm run preview
```

## 项目配置

### 后端API配置

项目默认配置后端API地址为 `http://localhost:8000`，可在 `vite.config.js` 中修改代理配置：

```javascript
server: {
  proxy: {
    '/api': {
      target: 'http://localhost:8000', // 修改为你的后端地址
      changeOrigin: true,
      rewrite: (path) => path.replace(/^\/api/, '')
    }
  }
}
```

### 环境变量

创建 `.env` 文件来配置环境变量：

```env
VITE_API_BASE_URL=http://localhost:8000
```

## 页面说明

### 1. 数据可视化 (Dashboard)

- 销售统计卡片：显示总销售额、订单数量、产品种类、平均订单金额
- 销售趋势图表：支持7天、30天、90天的趋势查看
- 分类统计饼图：展示各产品分类的销售占比
- 最近销售记录：显示最新的销售数据

### 2. 数据上传 (DataUpload)

- CSV文件拖拽上传
- 文件预览功能
- 上传进度显示
- 上传历史记录
- CSV模板下载

### 3. 数据查询 (DataQuery)

- 多条件查询：日期范围、产品名称、分类、金额范围、数量范围
- 查询结果表格展示
- 分页功能
- 数据导出功能
- 记录详情查看

## API接口

### 销售数据相关接口

- `GET /api/sales/stats` - 获取销售统计数据
- `GET /api/sales/trend` - 获取销售趋势数据
- `GET /api/sales/category-stats` - 获取分类统计数据
- `POST /api/sales/upload` - 上传CSV文件
- `GET /api/sales/query` - 查询销售记录
- `GET /api/sales/list` - 获取销售记录列表

## 开发指南

### 添加新页面

1. 在 `src/views/` 目录下创建新的Vue组件
2. 在 `src/router/index.js` 中添加路由配置
3. 在 `src/components/Layout.vue` 中添加导航菜单项

### 添加新API接口

1. 在 `src/api/index.js` 中添加新的API方法
2. 在对应的页面组件中调用API

### 样式规范

- 使用Element Plus组件库
- 响应式设计，支持移动端
- 统一的颜色主题和间距

## 部署说明

### 构建生产版本

```bash
npm run build
```

构建完成后，`dist` 目录包含所有静态文件。

### 部署到服务器

将 `dist` 目录中的文件部署到Web服务器即可。

## 浏览器支持

- Chrome >= 87
- Firefox >= 78
- Safari >= 14
- Edge >= 88

## 许可证

MIT License 