# 🚀 销售数据分析系统 - 快速参考

## 📋 项目信息
- **项目名称**: 销售数据分析系统
- **版本**: 1.0.0
- **技术栈**: FastAPI + SQLite + Pandas
- **数据库**: SQLite (`sales_analyzer.db`)

## ⚡ 快速启动

### 1. 激活环境
```bash
venv\Scripts\Activate.ps1
```

### 2. 启动应用
```bash
python simple_app.py
```

### 3. 访问应用
- **首页**: http://localhost:8000/
- **API文档**: http://localhost:8000/docs
- **健康检查**: http://localhost:8000/health

## 🔧 核心依赖

| 包名 | 版本 | 用途 |
|------|------|------|
| fastapi | 0.116.1 | Web框架 |
| uvicorn | 0.35.0 | ASGI服务器 |
| sqlalchemy | 2.0.41 | ORM框架 |
| pandas | 2.3.1 | 数据处理 |
| numpy | 2.3.1 | 数值计算 |
| pydantic | 2.11.7 | 数据验证 |

## 📊 数据库结构

### 销售记录表 (sales_records)
```sql
- id (主键)
- order_id (订单ID)
- product_name (产品名称)
- category (产品类别)
- customer_name (客户名称)
- region (销售区域)
- sales_amount (销售金额)
- quantity (销售数量)
- unit_price (单价)
- sales_date (销售日期)
- sales_person (销售人员)
- payment_method (支付方式)
- created_at (创建时间)
- updated_at (更新时间)
```

### 导入日志表 (data_import_logs)
```sql
- id (主键)
- filename (文件名)
- file_size (文件大小)
- records_imported (导入记录数)
- import_status (导入状态)
- error_message (错误信息)
- imported_at (导入时间)
```

## 🌐 API接口

### 基础接口
- `GET /` - 应用首页
- `GET /health` - 健康检查

### 销售数据
- `GET /api/v1/sales/` - 获取销售记录
- `GET /api/v1/sales/statistics/summary` - 销售摘要

### 数据上传
- `POST /api/v1/upload/csv` - 上传CSV文件

### 数据分析
- `GET /api/v1/analytics/top-products` - 热销产品
- `GET /api/v1/analytics/top-regions` - 热销区域

## 📁 重要文件

| 文件 | 用途 | 说明 |
|------|------|------|
| `simple_app.py` | 主应用 | 简化版应用（推荐） |
| `simple_init_db.py` | 数据库初始化 | 创建数据库表 |
| `data/sample_sales_data.csv` | 示例数据 | 测试用销售数据 |
| `sales_analyzer.db` | 数据库文件 | SQLite数据库 |
| `requirements.txt` | 依赖列表 | Python包依赖 |

## 🔍 常用命令

### 开发命令
```bash
# 激活虚拟环境
venv\Scripts\Activate.ps1

# 启动应用
python simple_app.py

# 初始化数据库
python simple_init_db.py

# 安装依赖
pip install -r requirements.txt
```

### 测试命令
```bash
# 运行测试
pytest tests/

# API测试
curl http://localhost:8000/api/v1/sales/
```

### 数据库命令
```bash
# 查看数据库
sqlite3 sales_analyzer.db

# 查看表结构
.schema sales_records

# 查询数据
SELECT * FROM sales_records LIMIT 10;
```

## 🚨 故障排除

### 常见问题
1. **端口被占用**: 使用 `--port 8001` 参数
2. **依赖安装失败**: 升级pip后重新安装
3. **数据库错误**: 重新运行 `python simple_init_db.py`

### 日志查看
```bash
# 查看应用日志
tail -f logs/app.log

# 查看错误日志
tail -f logs/error.log
```

## 📚 文档资源

- **详细文档**: `PROJECT_BUILD_GUIDE.md`
- **运行指南**: `RUN_GUIDE.md`
- **开发指南**: `DEVELOPMENT.md`
- **API文档**: http://localhost:8000/docs

## 🎯 下一步

1. 运行应用并测试基本功能
2. 上传示例数据查看效果
3. 根据需求扩展功能
4. 添加更多数据分析功能

---

**快速启动**: `python simple_app.py`  
**访问地址**: http://localhost:8000/docs 