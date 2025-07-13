# 销售数据分析系统 (Sales Analytics System)

一个完整的销售数据分析解决方案，包含基于FastAPI的后端API服务和基于Vue.js的前端界面，提供强大的数据处理、统计分析和可视化功能。

## 🚀 项目概述

本系统是一个企业级销售数据分析平台，支持CSV数据导入、数据清洗、多维度统计分析、可视化展示等功能。系统采用前后端分离架构，提供RESTful API接口和现代化的Web界面。

## ✨ 功能特性

### 后端功能 (SalesAnalyzer)
- 📊 **数据处理**: CSV文件导入、数据清洗和预处理
- 🔍 **数据分析**: 多维度统计分析、趋势分析、分类统计
- 📈 **API服务**: RESTful API接口，支持数据查询和统计
- 🗄️ **数据存储**: SQLite数据库，支持数据持久化
- 🧪 **测试覆盖**: 完整的单元测试和集成测试
- 📚 **API文档**: 自动生成的Swagger文档

### 前端功能 (SalesFront)
- 📊 **数据可视化**: 销售趋势图表、分类统计饼图、数据卡片
- 📁 **文件上传**: 拖拽式CSV文件上传，支持文件预览
- 🔍 **数据查询**: 多条件查询界面，支持分页和导出
- 📱 **响应式设计**: 适配各种设备尺寸
- 🎨 **现代化UI**: 基于Element Plus的美观界面

## 🛠️ 技术栈

### 后端技术栈
- **框架**: FastAPI 0.104.1
- **服务器**: Uvicorn 0.24.0
- **数据处理**: Pandas 2.1.3, NumPy 1.25.2
- **数据库**: SQLAlchemy 2.0.23 + SQLite
- **数据验证**: Pydantic 2.5.0
- **可视化**: Plotly 5.17.0, Matplotlib 3.8.2
- **测试**: Pytest 7.4.3
- **数据库迁移**: Alembic 1.12.1

### 前端技术栈
- **框架**: Vue.js 3.3.4
- **路由**: Vue Router 4.2.4
- **UI组件**: Element Plus 2.3.8
- **图表库**: ECharts 5.4.3
- **HTTP客户端**: Axios 1.4.0
- **构建工具**: Vite 4.4.5
- **代码规范**: ESLint + Prettier

## 📁 项目结构

```
Sales/
├── SalesAnalyzer/          # 后端API服务
│   ├── app/               # 主应用目录
│   │   ├── api/           # API路由和端点
│   │   ├── core/          # 核心配置
│   │   ├── models/        # 数据模型
│   │   ├── schemas/       # Pydantic模式
│   │   ├── services/      # 业务逻辑服务
│   │   ├── utils/         # 工具函数
│   │   └── main.py        # 应用入口
│   ├── data/              # 数据文件目录
│   ├── tests/             # 测试文件
│   ├── notebooks/         # Jupyter notebooks
│   ├── requirements.txt   # Python依赖
│   └── README.md          # 后端说明文档
├── SalesFront/            # 前端应用
│   ├── src/               # 源代码
│   │   ├── api/           # API接口配置
│   │   ├── components/    # 公共组件
│   │   ├── router/        # 路由配置
│   │   ├── views/         # 页面组件
│   │   ├── styles/        # 样式文件
│   │   ├── utils/         # 工具函数
│   │   ├── App.vue        # 根组件
│   │   └── main.js        # 入口文件
│   ├── package.json       # Node.js依赖
│   └── README.md          # 前端说明文档
└── doc/                   # 项目文档
```

## 🚀 快速开始

### 环境要求

- Python 3.8+
- Node.js 16+
- npm 或 yarn

### 1. 克隆项目

```bash
git clone <repository-url>
cd Sales
```

### 2. 后端设置

```bash
# 进入后端目录
cd SalesAnalyzer

# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt

# 初始化数据库
python init_db.py

# 启动后端服务
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 3. 前端设置

```bash
# 进入前端目录
cd SalesFront

# 安装依赖
npm install

# 启动开发服务器
npm run dev
```

### 4. 访问应用

- **前端界面**: http://localhost:5173
- **后端API文档**: http://localhost:8000/docs
- **后端API**: http://localhost:8000

## 📖 使用指南

### 数据上传

1. 在前端界面点击"数据上传"页面
2. 拖拽或选择CSV文件
3. 系统会自动处理并导入数据

### 数据查询

1. 在"数据查询"页面设置查询条件
2. 支持按日期、产品、分类、金额等条件筛选
3. 查看查询结果并支持导出

### 数据可视化

1. 在"数据看板"页面查看统计图表
2. 支持销售趋势、分类统计等可视化
3. 可切换不同的时间范围

## 🔧 开发指南

### 后端开发

```bash
# 运行测试
cd SalesAnalyzer
pytest

# 数据库迁移
alembic revision --autogenerate -m "description"
alembic upgrade head

# 代码格式化
black app/
isort app/
```

### 前端开发

```bash
# 代码检查
cd SalesFront
npm run lint

# 构建生产版本
npm run build

# 预览构建结果
npm run preview
```

## 📊 API接口

### 主要接口

- `GET /api/sales/stats` - 获取销售统计数据
- `GET /api/sales/trend` - 获取销售趋势数据
- `GET /api/sales/category-stats` - 获取分类统计数据
- `POST /api/sales/upload` - 上传CSV文件
- `GET /api/sales/query` - 查询销售记录
- `GET /api/sales/list` - 获取销售记录列表

详细API文档请访问: http://localhost:8000/docs

## 🧪 测试

### 后端测试

```bash
cd SalesAnalyzer
pytest tests/ -v
```

### 前端测试

```bash
cd SalesFront
npm run test
```

## 📦 部署

### 后端部署

```bash
# 生产环境启动
cd SalesAnalyzer
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

### 前端部署

```bash
# 构建生产版本
cd SalesFront
npm run build

# 部署dist目录到Web服务器
```

## 🤝 贡献指南

1. Fork 项目
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打开 Pull Request

## 📝 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情

## 📞 联系方式

如有问题或建议，请通过以下方式联系：

- 提交 Issue
- 发送邮件
- 项目讨论区

## 🙏 致谢

感谢所有为这个项目做出贡献的开发者和用户！

---

**注意**: 首次使用前请确保已正确配置数据库和依赖环境。 