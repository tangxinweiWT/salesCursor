# 🧪 测试执行指南

## 📋 测试概述

本指南将帮助您执行销售数据分析系统的完整测试流程，包括功能测试、性能测试和集成测试。

## 🚀 快速测试

### 1. 环境准备

确保您已经：
- ✅ 激活虚拟环境
- ✅ 安装所有依赖
- ✅ 启动应用

```bash
# 激活虚拟环境
venv\Scripts\Activate.ps1

# 启动应用（在另一个终端窗口）
python simple_app.py
```

### 2. 运行自动化测试

```bash
# 运行完整测试套件
python run_tests.py
```

### 3. 手动测试

如果自动化测试通过，您还可以进行手动测试：

#### 3.1 访问API文档
- 打开浏览器访问：http://localhost:8000/docs
- 测试各个API接口

#### 3.2 上传测试数据
- 使用示例文件：`data/sample_sales_data.csv`
- 通过API文档界面上传文件

#### 3.3 查看分析结果
- 访问：http://localhost:8000/api/v1/analytics/top-products
- 访问：http://localhost:8000/api/v1/analytics/top-regions

## 🔧 详细测试步骤

### 阶段1：基础功能测试

#### 1.1 应用启动测试
```bash
# 检查应用是否正常运行
curl http://localhost:8000/health
```

**预期结果**：
```json
{
  "status": "healthy",
  "message": "系统运行正常"
}
```

#### 1.2 数据库连接测试
```bash
# 检查数据库文件
ls -la sales_analyzer.db

# 检查数据库表结构
sqlite3 sales_analyzer.db ".schema"
```

### 阶段2：API接口测试

#### 2.1 基础API测试
```bash
# 测试首页
curl http://localhost:8000/

# 测试健康检查
curl http://localhost:8000/health
```

#### 2.2 销售数据API测试
```bash
# 获取销售记录
curl http://localhost:8000/api/v1/sales/

# 获取销售摘要
curl http://localhost:8000/api/v1/sales/statistics/summary
```

#### 2.3 文件上传测试
```bash
# 上传CSV文件
curl -X POST "http://localhost:8000/api/v1/upload/csv" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@data/sample_sales_data.csv"
```

#### 2.4 数据分析API测试
```bash
# 获取热销产品
curl http://localhost:8000/api/v1/analytics/top-products

# 获取热销区域
curl http://localhost:8000/api/v1/analytics/top-regions
```

### 阶段3：错误处理测试

#### 3.1 文件上传错误测试
```bash
# 上传非CSV文件
echo "invalid content" > test.txt
curl -X POST "http://localhost:8000/api/v1/upload/csv" \
  -F "file=@test.txt"
```

**预期结果**：返回400错误

#### 3.2 无效API路径测试
```bash
# 访问不存在的路径
curl http://localhost:8000/invalid/path
```

**预期结果**：返回404错误

### 阶段4：性能测试

#### 4.1 响应时间测试
```bash
# 测试API响应时间
time curl http://localhost:8000/api/v1/sales/
```

#### 4.2 并发测试
```bash
# 使用Python脚本进行并发测试
python -c "
import asyncio
import httpx
import time

async def test_concurrent():
    async with httpx.AsyncClient() as client:
        start_time = time.time()
        tasks = [client.get('http://localhost:8000/api/v1/sales/') for _ in range(10)]
        responses = await asyncio.gather(*tasks)
        end_time = time.time()
        
        success_count = sum(1 for r in responses if r.status_code == 200)
        print(f'并发测试: {success_count}/10 成功, 耗时: {end_time-start_time:.2f}秒')

asyncio.run(test_concurrent())
"
```

## 📊 测试结果验证

### 功能测试检查清单

- [ ] 应用能够正常启动
- [ ] 数据库连接正常
- [ ] 基础API返回正确响应
- [ ] 文件上传功能正常
- [ ] 数据分析功能正常
- [ ] 错误处理机制有效

### 性能测试检查清单

- [ ] API响应时间 < 1秒
- [ ] 文件上传处理时间 < 5秒
- [ ] 支持并发请求
- [ ] 内存使用正常
- [ ] CPU使用率正常

### 数据完整性检查

- [ ] CSV数据正确导入
- [ ] 数据库记录数量正确
- [ ] 数据类型转换正确
- [ ] 统计计算结果准确

## 🐛 常见问题排查

### 1. 应用无法启动
```bash
# 检查端口占用
netstat -ano | findstr :8000

# 检查依赖安装
pip list | grep fastapi
```

### 2. 数据库连接失败
```bash
# 重新初始化数据库
python simple_init_db.py

# 检查数据库文件权限
ls -la sales_analyzer.db
```

### 3. 文件上传失败
```bash
# 检查文件格式
file data/sample_sales_data.csv

# 检查文件内容
head -5 data/sample_sales_data.csv
```

### 4. API响应错误
```bash
# 检查应用日志
# 查看控制台输出

# 测试网络连接
ping localhost
```

## 📈 测试报告

### 测试结果模板

```json
{
  "test_date": "2024-12-XX",
  "system": "销售数据分析系统",
  "version": "1.0.0",
  "test_results": {
    "total_tests": 10,
    "passed": 9,
    "failed": 1,
    "success_rate": "90%"
  },
  "performance_metrics": {
    "avg_response_time": "150ms",
    "max_response_time": "500ms",
    "concurrent_users": 10
  },
  "issues": [
    {
      "severity": "low",
      "description": "文件上传响应时间较长",
      "status": "open"
    }
  ]
}
```

## 🎯 测试完成标准

### 通过标准
- ✅ 所有功能测试通过
- ✅ 性能指标达标
- ✅ 错误处理有效
- ✅ 数据完整性验证通过

### 失败标准
- ❌ 核心功能无法使用
- ❌ 性能指标不达标
- ❌ 数据丢失或损坏
- ❌ 安全漏洞存在

## 📞 测试支持

如果在测试过程中遇到问题：

1. **查看日志**：检查应用控制台输出
2. **检查配置**：确认环境配置正确
3. **重启应用**：重新启动测试应用
4. **联系开发团队**：报告测试问题

---

**测试负责人**: 开发团队  
**最后更新**: 2024年12月 