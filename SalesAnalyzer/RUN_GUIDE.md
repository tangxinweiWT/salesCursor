# 🚀 销售数据分析系统运行指南

## 快速启动

我已经为您创建了简化版本的应用，可以直接运行！

### 方法一：使用简化版本（推荐）

1. **激活虚拟环境**：
   ```bash
   venv\Scripts\Activate.ps1
   ```

2. **运行简化应用**：
   ```bash
   python simple_app.py
   ```

### 方法二：使用完整版本

1. **激活虚拟环境**：
   ```bash
   venv\Scripts\Activate.ps1
   ```

2. **初始化数据库**：
   ```bash
   python simple_init_db.py
   ```

3. **运行应用**：
   ```bash
   python run_app.py
   ```

## 🌐 访问应用

启动成功后，访问以下地址：

- **应用首页**: http://localhost:8000/
- **API文档**: http://localhost:8000/docs
- **健康检查**: http://localhost:8000/health

## 📊 测试功能

### 1. 查看API文档
访问 http://localhost:8000/docs 查看所有可用的API接口

### 2. 上传销售数据
使用示例文件 `data/sample_sales_data.csv` 测试数据上传功能

### 3. 查看销售统计
- 销售摘要: http://localhost:8000/api/v1/sales/statistics/summary
- 热销产品: http://localhost:8000/api/v1/analytics/top-products
- 热销区域: http://localhost:8000/api/v1/analytics/top-regions

## 🔧 可用API接口

### 基础接口
- `GET /` - 应用首页
- `GET /health` - 健康检查

### 销售数据管理
- `GET /api/v1/sales/` - 获取销售记录列表
- `GET /api/v1/sales/statistics/summary` - 获取销售摘要

### 数据上传
- `POST /api/v1/upload/csv` - 上传CSV文件

### 数据分析
- `GET /api/v1/analytics/top-products` - 获取热销产品
- `GET /api/v1/analytics/top-regions` - 获取热销区域

## 📁 项目文件说明

- `simple_app.py` - 简化版主应用（推荐使用）
- `simple_init_db.py` - 简化版数据库初始化
- `run_app.py` - 完整版启动脚本
- `data/sample_sales_data.csv` - 示例销售数据

## ⚠️ 注意事项

1. 确保虚拟环境已激活（命令提示符前显示 `(venv)`）
2. 如果遇到依赖问题，请先安装：`pip install fastapi uvicorn sqlalchemy pandas`
3. 应用默认运行在 8000 端口
4. 数据库文件会自动创建为 `sales_analyzer.db`

## 🎯 下一步

1. 运行应用并测试基本功能
2. 上传示例数据查看效果
3. 根据需求扩展功能
4. 添加更多数据分析功能

现在您可以开始运行和测试这个销售数据分析系统了！ 