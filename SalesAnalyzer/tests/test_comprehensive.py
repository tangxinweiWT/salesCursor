"""
销售数据分析系统 - 综合测试脚本
"""
import pytest
import httpx
import time
import os
import sqlite3
import pandas as pd
from datetime import datetime
import asyncio
import json

# 测试配置
BASE_URL = "http://localhost:8000"
TEST_CSV_FILE = "data/sample_sales_data.csv"
TEST_DB_FILE = "sales_analyzer.db"

class TestSalesAnalyzer:
    """销售数据分析系统综合测试类"""
    
    @pytest.fixture(autouse=True)
    def setup(self):
        """测试前准备"""
        # 确保测试数据文件存在
        assert os.path.exists(TEST_CSV_FILE), f"测试数据文件不存在: {TEST_CSV_FILE}"
        
        # 确保数据库文件存在
        if not os.path.exists(TEST_DB_FILE):
            os.system("python simple_init_db.py")
        
        yield
        
        # 测试后清理（可选）
        pass
    
    def test_application_startup(self):
        """测试应用启动"""
        print("🧪 测试应用启动...")
        
        # 检查应用是否在运行
        try:
            with httpx.Client(timeout=5.0) as client:
                response = client.get(f"{BASE_URL}/health")
                assert response.status_code == 200
                data = response.json()
                assert data["status"] == "healthy"
                print("✅ 应用启动测试通过")
        except Exception as e:
            pytest.fail(f"应用启动测试失败: {e}")
    
    def test_database_connection(self):
        """测试数据库连接"""
        print("🧪 测试数据库连接...")
        
        try:
            # 连接数据库
            conn = sqlite3.connect(TEST_DB_FILE)
            cursor = conn.cursor()
            
            # 检查表是否存在
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = [row[0] for row in cursor.fetchall()]
            
            assert "sales_records" in tables, "sales_records表不存在"
            assert "data_import_logs" in tables, "data_import_logs表不存在"
            
            # 检查表结构
            cursor.execute("PRAGMA table_info(sales_records)")
            columns = [row[1] for row in cursor.fetchall()]
            expected_columns = [
                "id", "order_id", "product_name", "category", "customer_name",
                "region", "sales_amount", "quantity", "unit_price", "sales_date",
                "sales_person", "payment_method", "created_at", "updated_at"
            ]
            
            for col in expected_columns:
                assert col in columns, f"缺少列: {col}"
            
            conn.close()
            print("✅ 数据库连接测试通过")
            
        except Exception as e:
            pytest.fail(f"数据库连接测试失败: {e}")
    
    def test_basic_apis(self):
        """测试基础API接口"""
        print("🧪 测试基础API接口...")
        
        with httpx.Client(timeout=10.0) as client:
            # 测试首页
            response = client.get(f"{BASE_URL}/")
            assert response.status_code == 200
            data = response.json()
            assert "message" in data
            assert "version" in data
            
            # 测试健康检查
            response = client.get(f"{BASE_URL}/health")
            assert response.status_code == 200
            data = response.json()
            assert data["status"] == "healthy"
            
            print("✅ 基础API测试通过")
    
    def test_sales_data_apis(self):
        """测试销售数据API"""
        print("🧪 测试销售数据API...")
        
        with httpx.Client(timeout=10.0) as client:
            # 测试获取销售记录
            response = client.get(f"{BASE_URL}/api/v1/sales/")
            assert response.status_code == 200
            data = response.json()
            assert isinstance(data, list)
            
            # 测试销售摘要
            response = client.get(f"{BASE_URL}/api/v1/sales/statistics/summary")
            assert response.status_code == 200
            data = response.json()
            assert "total_sales" in data
            assert "total_orders" in data
            assert "total_quantity" in data
            assert "avg_order_value" in data
            
            print("✅ 销售数据API测试通过")
    
    def test_file_upload(self):
        """测试文件上传功能"""
        print("🧪 测试文件上传功能...")
        
        with httpx.Client(timeout=30.0) as client:
            # 准备测试文件
            with open(TEST_CSV_FILE, "rb") as f:
                files = {"file": ("test_sales.csv", f, "text/csv")}
                response = client.post(f"{BASE_URL}/api/v1/upload/csv", files=files)
            
            assert response.status_code == 200
            data = response.json()
            assert data["success"] == True
            assert data["records_imported"] > 0
            
            print(f"✅ 文件上传测试通过，导入 {data['records_imported']} 条记录")
    
    def test_analytics_apis(self):
        """测试数据分析API"""
        print("🧪 测试数据分析API...")
        
        with httpx.Client(timeout=10.0) as client:
            # 测试热销产品
            response = client.get(f"{BASE_URL}/api/v1/analytics/top-products")
            assert response.status_code == 200
            data = response.json()
            assert isinstance(data, list)
            
            # 测试热销区域
            response = client.get(f"{BASE_URL}/api/v1/analytics/top-regions")
            assert response.status_code == 200
            data = response.json()
            assert isinstance(data, list)
            
            print("✅ 数据分析API测试通过")
    
    def test_error_handling(self):
        """测试错误处理"""
        print("🧪 测试错误处理...")
        
        with httpx.Client(timeout=10.0) as client:
            # 测试上传非CSV文件
            files = {"file": ("test.txt", b"invalid content", "text/plain")}
            response = client.post(f"{BASE_URL}/api/v1/upload/csv", files=files)
            assert response.status_code == 400
            
            # 测试无效的API路径
            response = client.get(f"{BASE_URL}/invalid/path")
            assert response.status_code == 404
            
            print("✅ 错误处理测试通过")
    
    def test_data_processing(self):
        """测试数据处理功能"""
        print("🧪 测试数据处理功能...")
        
        # 读取测试数据
        df = pd.read_csv(TEST_CSV_FILE)
        
        # 验证数据格式
        assert "order_id" in df.columns
        assert "product_name" in df.columns
        assert "sales_amount" in df.columns
        
        # 验证数据类型
        assert pd.api.types.is_numeric_dtype(df["sales_amount"])
        assert pd.api.types.is_numeric_dtype(df["quantity"])
        
        # 验证数据完整性
        assert not df.empty, "测试数据为空"
        
        print(f"✅ 数据处理测试通过，数据行数: {len(df)}")
    
    def test_performance(self):
        """测试性能"""
        print("🧪 测试性能...")
        
        with httpx.Client(timeout=10.0) as client:
            # 测试响应时间
            start_time = time.time()
            response = client.get(f"{BASE_URL}/api/v1/sales/")
            end_time = time.time()
            
            response_time = (end_time - start_time) * 1000  # 转换为毫秒
            assert response_time < 1000, f"响应时间过长: {response_time:.2f}ms"
            
            print(f"✅ 性能测试通过，响应时间: {response_time:.2f}ms")
    
    def test_concurrent_requests(self):
        """测试并发请求"""
        print("🧪 测试并发请求...")
        
        async def make_request():
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(f"{BASE_URL}/api/v1/sales/")
                return response.status_code
        
        # 并发发送5个请求
        async def test_concurrency():
            tasks = [make_request() for _ in range(5)]
            results = await asyncio.gather(*tasks)
            
            # 验证所有请求都成功
            for status_code in results:
                assert status_code == 200
            
            print("✅ 并发请求测试通过")
        
        # 运行异步测试
        asyncio.run(test_concurrency())
    
    def test_data_integrity(self):
        """测试数据完整性"""
        print("🧪 测试数据完整性...")
        
        # 连接数据库检查数据
        conn = sqlite3.connect(TEST_DB_FILE)
        
        # 检查销售记录数量
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM sales_records")
        record_count = cursor.fetchone()[0]
        
        # 检查数据一致性
        cursor.execute("SELECT COUNT(*) FROM sales_records WHERE sales_amount > 0")
        valid_amount_count = cursor.fetchone()[0]
        
        assert record_count > 0, "没有销售记录"
        assert valid_amount_count > 0, "没有有效的销售金额"
        
        # 检查导入日志
        cursor.execute("SELECT COUNT(*) FROM data_import_logs")
        log_count = cursor.fetchone()[0]
        
        assert log_count > 0, "没有导入日志"
        
        conn.close()
        print(f"✅ 数据完整性测试通过，记录数: {record_count}")

def run_comprehensive_test():
    """运行综合测试"""
    print("🚀 开始销售数据分析系统综合测试")
    print("=" * 50)
    
    # 创建测试实例
    tester = TestSalesAnalyzer()
    
    # 测试结果统计
    test_results = {
        "total": 0,
        "passed": 0,
        "failed": 0,
        "errors": []
    }
    
    # 获取所有测试方法
    test_methods = [method for method in dir(tester) if method.startswith('test_')]
    
    for method_name in test_methods:
        test_results["total"] += 1
        method = getattr(tester, method_name)
        
        try:
            # 运行测试
            method()
            test_results["passed"] += 1
            print(f"✅ {method_name} - 通过")
        except Exception as e:
            test_results["failed"] += 1
            error_msg = f"{method_name} - 失败: {str(e)}"
            test_results["errors"].append(error_msg)
            print(f"❌ {error_msg}")
    
    # 输出测试结果摘要
    print("\n" + "=" * 50)
    print("📊 测试结果摘要")
    print(f"总测试数: {test_results['total']}")
    print(f"通过数: {test_results['passed']}")
    print(f"失败数: {test_results['failed']}")
    print(f"通过率: {(test_results['passed']/test_results['total']*100):.1f}%")
    
    if test_results["errors"]:
        print("\n❌ 失败详情:")
        for error in test_results["errors"]:
            print(f"  - {error}")
    
    # 生成测试报告
    generate_test_report(test_results)
    
    return test_results["failed"] == 0

def generate_test_report(test_results):
    """生成测试报告"""
    report = {
        "test_date": datetime.now().isoformat(),
        "system": "销售数据分析系统",
        "version": "1.0.0",
        "results": test_results,
        "environment": {
            "python_version": "3.13.5",
            "database": "SQLite",
            "framework": "FastAPI"
        }
    }
    
    # 保存测试报告
    with open("test_report.json", "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    
    print(f"\n📄 测试报告已保存到: test_report.json")

if __name__ == "__main__":
    # 运行综合测试
    success = run_comprehensive_test()
    
    if success:
        print("\n🎉 所有测试通过！系统运行正常。")
        exit(0)
    else:
        print("\n⚠️  部分测试失败，请检查系统配置。")
        exit(1) 