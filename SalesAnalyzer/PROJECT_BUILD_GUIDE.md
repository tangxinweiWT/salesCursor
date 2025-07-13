# 📋 销售数据分析系统 - 项目构建说明

## 🎯 项目概述

销售数据分析系统是一个基于FastAPI的Web应用，提供销售数据的处理、分析和RESTful API服务。系统支持CSV文件上传、数据清洗、统计分析等功能。

## 🏗️ 技术架构

### 核心技术栈
- **Web框架**: FastAPI 0.116.1
- **ASGI服务器**: Uvicorn 0.35.0
- **数据库**: SQLite + SQLAlchemy 2.0.41
- **数据处理**: Pandas 2.3.1 + NumPy 2.3.1
- **数据验证**: Pydantic 2.11.7
- **测试框架**: Pytest 8.4.1
- **文档生成**: 自动生成Swagger/OpenAPI文档

### 项目结构
```
SalesAnalyzer/
├── app/                    # 主应用目录
│   ├── api/               # API路由层
│   ├── core/              # 核心配置
│   ├── models/            # 数据模型层
│   ├── schemas/           # Pydantic模式
│   ├── services/          # 业务逻辑层
│   ├── utils/             # 工具函数
│   └── main.py            # 应用入口
├── data/                  # 数据文件目录
├── tests/                 # 测试文件
├── notebooks/             # Jupyter notebooks
├── venv/                  # 虚拟环境
├── simple_app.py          # 简化版应用（推荐）
├── simple_init_db.py      # 简化版数据库初始化
├── run_app.py             # 完整版启动脚本
├── requirements.txt       # 项目依赖
└── README.md             # 项目说明
```

## 🚀 初始运行指南

### 1. 环境准备

#### 1.1 Python环境
- **Python版本**: 3.8+ (推荐3.11+)
- **操作系统**: Windows/Linux/MacOS
- **包管理器**: pip

#### 1.2 创建虚拟环境
```bash
# 创建虚拟环境
python -m venv venv

# 激活虚拟环境 (Windows)
venv\Scripts\Activate.ps1

# 激活虚拟环境 (Linux/Mac)
source venv/bin/activate
```

#### 1.3 安装依赖
```bash
# 升级基础工具
pip install --upgrade pip setuptools wheel

# 安装核心依赖
pip install fastapi uvicorn sqlalchemy pandas numpy pydantic

# 安装完整依赖列表
pip install -r requirements.txt
```

### 2. 数据库初始化

#### 2.1 数据库格式
- **数据库类型**: SQLite
- **数据库文件**: `sales_analyzer.db`
- **ORM框架**: SQLAlchemy
- **连接字符串**: `sqlite:///./sales_analyzer.db`

#### 2.2 数据表结构

**销售记录表 (sales_records)**
```sql
CREATE TABLE sales_records (
    id INTEGER PRIMARY KEY,
    order_id VARCHAR(100),
    product_name VARCHAR(200),
    category VARCHAR(100),
    customer_name VARCHAR(100),
    region VARCHAR(100),
    sales_amount FLOAT,
    quantity INTEGER,
    unit_price FLOAT,
    sales_date DATETIME,
    sales_person VARCHAR(100),
    payment_method VARCHAR(50),
    created_at DATETIME,
    updated_at DATETIME
);
```

**数据导入日志表 (data_import_logs)**
```sql
CREATE TABLE data_import_logs (
    id INTEGER PRIMARY KEY,
    filename VARCHAR(255),
    file_size INTEGER,
    records_imported INTEGER,
    import_status VARCHAR(50),
    error_message TEXT,
    imported_at DATETIME
);
```

#### 2.3 初始化数据库
```bash
# 使用简化版初始化
python simple_init_db.py

# 或使用完整版初始化
python init_db.py
```

### 3. 启动应用

#### 3.1 简化版启动（推荐）
```bash
python simple_app.py
```

#### 3.2 完整版启动
```bash
python run_app.py
```

#### 3.3 开发模式启动
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## 🔄 后续运行指南

### 1. 日常启动
```bash
# 1. 激活虚拟环境
venv\Scripts\Activate.ps1

# 2. 启动应用
python simple_app.py
```

### 2. 生产环境启动
```bash
# 使用uvicorn启动（多进程）
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4

# 使用gunicorn启动（Linux/Mac）
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker
```

### 3. 后台运行
```bash
# Windows (使用nssm)
nssm install SalesAnalyzer "python" "simple_app.py"

# Linux/Mac (使用systemd)
sudo systemctl enable sales-analyzer
sudo systemctl start sales-analyzer
```

## 📦 依赖包详解

### 核心依赖

| 包名 | 版本 | 用途 | 说明 |
|------|------|------|------|
| fastapi | 0.116.1 | Web框架 | 现代化Python Web框架，自动生成API文档 |
| uvicorn | 0.35.0 | ASGI服务器 | 高性能ASGI服务器，支持WebSocket |
| sqlalchemy | 2.0.41 | ORM框架 | 数据库ORM，支持多种数据库 |
| pandas | 2.3.1 | 数据处理 | 强大的数据分析库 |
| numpy | 2.3.1 | 数值计算 | 科学计算基础库 |
| pydantic | 2.11.7 | 数据验证 | 数据验证和序列化 |

### 扩展依赖

| 包名 | 版本 | 用途 | 说明 |
|------|------|------|------|
| python-multipart | 0.0.20 | 文件上传 | 处理multipart/form-data |
| python-jose | 3.5.0 | JWT处理 | JSON Web Token支持 |
| passlib | 1.7.4 | 密码加密 | 密码哈希和验证 |
| python-dotenv | 1.1.1 | 环境变量 | .env文件支持 |
| alembic | 1.16.4 | 数据库迁移 | 数据库版本管理 |
| pytest | 8.4.1 | 测试框架 | 单元测试和集成测试 |
| httpx | 0.27.0 | HTTP客户端 | 异步HTTP客户端 |
| plotly | 5.17.0 | 数据可视化 | 交互式图表库 |
| matplotlib | 3.8.2 | 数据可视化 | 静态图表库 |
| seaborn | 0.13.0 | 数据可视化 | 统计图表库 |
| jupyter | 1.0.0 | 数据分析 | Jupyter notebook支持 |
| openpyxl | 3.1.2 | Excel处理 | Excel文件读写 |
| xlrd | 2.0.1 | Excel处理 | 旧版Excel文件读取 |

### 依赖安装命令
```bash
# 安装所有依赖
pip install -r requirements.txt

# 安装核心依赖（最小安装）
pip install fastapi uvicorn sqlalchemy pandas numpy pydantic

# 安装开发依赖
pip install pytest pytest-asyncio httpx

# 安装可视化依赖
pip install plotly matplotlib seaborn

# 安装数据处理依赖
pip install openpyxl xlrd
```

## 🔧 实现原理

### 1. 架构设计

#### 1.1 分层架构
```
┌─────────────────┐
│   API Layer     │  FastAPI路由层
├─────────────────┤
│  Service Layer  │  业务逻辑层
├─────────────────┤
│  Model Layer    │  数据模型层
├─────────────────┤
│ Database Layer  │  数据库层
└─────────────────┘
```

#### 1.2 数据流
```
CSV文件 → 数据清洗 → 数据验证 → 数据库存储 → 统计分析 → API响应
```

### 2. 核心功能实现

#### 2.1 数据上传处理
```python
# 文件上传流程
1. 接收CSV文件
2. 验证文件格式和大小
3. 使用Pandas读取数据
4. 数据清洗和验证
5. 批量插入数据库
6. 记录导入日志
```

#### 2.2 数据分析实现
```python
# 统计分析流程
1. 构建SQLAlchemy查询
2. 使用聚合函数计算
3. 分组和排序
4. 格式化返回结果
```

#### 2.3 API文档生成
```python
# FastAPI自动生成文档
1. 基于函数签名生成OpenAPI规范
2. 自动生成Swagger UI
3. 支持在线测试
4. 自动类型验证
```

### 3. 数据库设计

#### 3.1 关系设计
- **一对多**: 客户 → 订单
- **一对多**: 产品 → 订单
- **一对多**: 区域 → 订单
- **一对多**: 销售人员 → 订单

#### 3.2 索引优化
```sql
-- 创建索引提高查询性能
CREATE INDEX idx_sales_date ON sales_records(sales_date);
CREATE INDEX idx_region ON sales_records(region);
CREATE INDEX idx_category ON sales_records(category);
CREATE INDEX idx_sales_person ON sales_records(sales_person);
```

## 📚 API文档系统

### 1. 自动文档生成

#### 1.1 Swagger UI
- **访问地址**: http://localhost:8000/docs
- **功能**: 交互式API文档
- **特性**: 
  - 在线测试API
  - 自动参数验证
  - 响应示例
  - 认证支持

#### 1.2 ReDoc
- **访问地址**: http://localhost:8000/redoc
- **功能**: 静态API文档
- **特性**:
  - 更清晰的文档结构
  - 响应模式展示
  - 搜索功能

### 2. 文档配置

#### 2.1 FastAPI应用配置
```python
app = FastAPI(
    title="销售数据分析系统",
    description="基于FastAPI的销售数据分析系统",
    version="1.0.0",
    openapi_url="/api/v1/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc"
)
```

#### 2.2 API端点文档
```python
@app.get("/api/v1/sales/", 
         summary="获取销售记录",
         description="分页获取销售记录列表",
         response_model=List[SalesRecordSchema])
async def get_sales_records(
    skip: int = Query(0, description="跳过记录数"),
    limit: int = Query(100, description="返回记录数")
):
    """获取销售记录列表的详细说明"""
    pass
```

### 3. 文档依赖

#### 3.1 核心依赖
- **fastapi**: 自动生成OpenAPI规范
- **pydantic**: 数据模型验证和文档生成
- **uvicorn**: 提供文档访问服务

#### 3.2 可选依赖
- **python-multipart**: 文件上传文档支持
- **python-jose**: JWT认证文档支持

## 🔍 测试和调试

### 1. 单元测试
```bash
# 运行所有测试
pytest tests/

# 运行特定测试
pytest tests/test_api.py::test_get_sales_records

# 生成覆盖率报告
pytest --cov=app tests/
```

### 2. API测试
```bash
# 使用curl测试
curl http://localhost:8000/api/v1/sales/

# 使用httpx测试
python -c "
import httpx
response = httpx.get('http://localhost:8000/api/v1/sales/')
print(response.json())
"
```

### 3. 数据库调试
```bash
# 使用SQLite命令行工具
sqlite3 sales_analyzer.db

# 查看表结构
.schema sales_records

# 查询数据
SELECT * FROM sales_records LIMIT 10;
```

## 🚀 部署指南

### 1. 开发环境
```bash
# 本地开发
python simple_app.py
```

### 2. 生产环境
```bash
# 使用Docker
docker build -t sales-analyzer .
docker run -p 8000:8000 sales-analyzer

# 使用systemd (Linux)
sudo systemctl enable sales-analyzer
sudo systemctl start sales-analyzer
```

### 3. 反向代理配置
```nginx
# Nginx配置示例
server {
    listen 80;
    server_name your-domain.com;
    
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

## 📈 性能优化

### 1. 数据库优化
- 创建适当的索引
- 使用连接池
- 批量插入数据
- 定期清理日志

### 2. 应用优化
- 使用异步处理
- 实现缓存机制
- 分页查询
- 数据压缩

### 3. 监控和日志
- 添加日志记录
- 性能监控
- 错误追踪
- 健康检查

## 🔧 故障排除

### 1. 常见问题

#### 1.1 依赖安装失败
```bash
# 解决方案
pip install --upgrade pip
pip install -r requirements.txt --force-reinstall
```

#### 1.2 数据库连接错误
```bash
# 检查数据库文件权限
chmod 644 sales_analyzer.db

# 重新初始化数据库
python simple_init_db.py
```

#### 1.3 端口被占用
```bash
# 使用不同端口
uvicorn app.main:app --port 8001

# 或杀死占用进程
netstat -ano | findstr :8000
taskkill /PID <进程ID> /F
```

### 2. 日志查看
```bash
# 查看应用日志
tail -f logs/app.log

# 查看错误日志
tail -f logs/error.log
```

## 📞 技术支持

### 1. 文档资源
- [FastAPI官方文档](https://fastapi.tiangolo.com/)
- [SQLAlchemy文档](https://docs.sqlalchemy.org/)
- [Pandas文档](https://pandas.pydata.org/docs/)

### 2. 社区支持
- GitHub Issues
- Stack Overflow
- FastAPI Discord

---

**项目版本**: 1.0.0  
**最后更新**: 2024年12月  
**维护者**: 开发团队 