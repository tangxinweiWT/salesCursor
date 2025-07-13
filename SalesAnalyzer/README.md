# 销售数据分析系统 (Sales Analyzer)

一个基于FastAPI的销售数据分析系统，提供数据处理、统计分析和RESTful API服务。

## 功能特性

- 📊 CSV销售数据导入和处理
- 🧹 数据清洗和预处理
- 📈 销售数据统计分析
- 🔍 多维度数据查询
- 📱 RESTful API接口
- 📊 数据可视化支持

## 技术栈

- **后端框架**: FastAPI
- **数据处理**: Pandas, NumPy
- **数据库**: SQLAlchemy + SQLite
- **数据验证**: Pydantic
- **可视化**: Plotly, Matplotlib
- **测试**: Pytest

## 项目结构

```
SalesAnalyzer/
├── app/                    # 主应用目录
│   ├── api/               # API路由
│   ├── core/              # 核心配置
│   ├── models/            # 数据模型
│   ├── services/          # 业务逻辑
│   ├── utils/             # 工具函数
│   └── main.py            # 应用入口
├── data/                  # 数据文件目录
├── tests/                 # 测试文件
├── notebooks/             # Jupyter notebooks
├── requirements.txt       # 项目依赖
└── README.md             # 项目说明
```

## 快速开始

1. 安装依赖
```bash
pip install -r requirements.txt
```

2. 运行应用
```bash
uvicorn app.main:app --reload
```

3. 访问API文档
```
http://localhost:8000/docs
```

## 开发步骤

1. **环境搭建** ✅
2. **数据模型设计**
3. **数据处理服务**
4. **API接口开发**
5. **数据分析功能**
6. **测试用例编写**
7. **文档完善**

## 许可证

MIT License 