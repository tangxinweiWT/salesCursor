# 开发指南

## 项目概述

销售数据分析系统是一个基于FastAPI的Web应用，提供销售数据的处理、分析和API服务。

## 技术栈

- **后端框架**: FastAPI
- **数据库**: SQLAlchemy + SQLite
- **数据处理**: Pandas, NumPy
- **数据验证**: Pydantic
- **测试**: Pytest
- **文档**: 自动生成API文档

## 项目结构

```
SalesAnalyzer/
├── app/                    # 主应用目录
│   ├── api/               # API路由
│   │   └── api_v1/        # API版本1
│   │       ├── endpoints/ # API端点
│   │       └── api.py     # 路由注册
│   ├── core/              # 核心配置
│   │   ├── config.py      # 应用配置
│   │   └── database.py    # 数据库配置
│   ├── models/            # 数据模型
│   │   └── sales.py       # 销售数据模型
│   ├── schemas/           # Pydantic模式
│   │   └── sales.py       # 销售数据模式
│   ├── services/          # 业务逻辑
│   │   └── data_processor.py # 数据处理服务
│   ├── utils/             # 工具函数
│   │   └── helpers.py     # 辅助函数
│   └── main.py            # 应用入口
├── data/                  # 数据文件
│   └── sample_sales_data.csv # 示例数据
├── tests/                 # 测试文件
│   └── test_api.py        # API测试
├── notebooks/             # Jupyter notebooks
├── requirements.txt       # 项目依赖
└── README.md             # 项目说明
```

## 开发环境设置

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 初始化数据库

```bash
python init_db.py
```

### 3. 运行应用

```bash
uvicorn app.main:app --reload
```

### 4. 访问API文档

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## API端点

### 销售数据管理

- `GET /api/v1/sales/` - 获取销售记录列表
- `GET /api/v1/sales/{record_id}` - 获取单个销售记录
- `GET /api/v1/sales/statistics/summary` - 获取销售摘要

### 数据上传

- `POST /api/v1/upload/csv` - 上传CSV文件
- `GET /api/v1/upload/history` - 获取上传历史

### 数据分析

- `GET /api/v1/analytics/top-products` - 获取热销产品
- `GET /api/v1/analytics/top-regions` - 获取热销区域
- `GET /api/v1/analytics/sales-trend` - 获取销售趋势

## 数据模型

### SalesRecord (销售记录)

- `id`: 主键
- `order_id`: 订单ID
- `product_name`: 产品名称
- `category`: 产品类别
- `customer_name`: 客户名称
- `region`: 销售区域
- `sales_amount`: 销售金额
- `quantity`: 销售数量
- `unit_price`: 单价
- `sales_date`: 销售日期
- `sales_person`: 销售人员
- `payment_method`: 支付方式

### DataImportLog (数据导入日志)

- `id`: 主键
- `filename`: 文件名
- `file_size`: 文件大小
- `records_imported`: 导入记录数
- `import_status`: 导入状态
- `error_message`: 错误信息
- `imported_at`: 导入时间

## 开发步骤

### 第一步：环境搭建 ✅
- [x] 创建项目结构
- [x] 安装依赖
- [x] 配置数据库

### 第二步：数据模型设计 ✅
- [x] 设计销售记录模型
- [x] 设计导入日志模型
- [x] 创建Pydantic模式

### 第三步：数据处理服务
- [ ] 完善数据清洗逻辑
- [ ] 添加数据验证
- [ ] 实现批量处理

### 第四步：API接口开发
- [ ] 完善CRUD操作
- [ ] 添加查询过滤
- [ ] 实现分页功能

### 第五步：数据分析功能
- [ ] 实现统计计算
- [ ] 添加图表生成
- [ ] 支持导出功能

### 第六步：测试用例编写
- [ ] 单元测试
- [ ] 集成测试
- [ ] API测试

### 第七步：文档完善
- [ ] API文档
- [ ] 用户手册
- [ ] 部署指南

## 测试

运行测试：

```bash
pytest tests/
```

## 部署

### 开发环境

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 生产环境

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

## 贡献指南

1. Fork 项目
2. 创建功能分支
3. 提交更改
4. 推送到分支
5. 创建 Pull Request

## 许可证

MIT License 