"""
测试运行脚本
"""
import subprocess
import sys
import os
import time
from datetime import datetime

def run_test_command(command, description):
    """运行测试命令"""
    print(f"\n🧪 {description}")
    print("-" * 40)
    
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ 测试通过")
            if result.stdout:
                print(result.stdout)
        else:
            print("❌ 测试失败")
            if result.stderr:
                print(result.stderr)
            if result.stdout:
                print(result.stdout)
        
        return result.returncode == 0
    except Exception as e:
        print(f"❌ 测试执行错误: {e}")
        return False

def check_application_running():
    """检查应用是否在运行"""
    print("🔍 检查应用运行状态...")
    
    try:
        import httpx
        with httpx.Client(timeout=5.0) as client:
            response = client.get("http://localhost:8000/health")
            if response.status_code == 200:
                print("✅ 应用正在运行")
                return True
            else:
                print("❌ 应用未正常运行")
                return False
    except Exception as e:
        print(f"❌ 无法连接到应用: {e}")
        return False

def main():
    """主测试流程"""
    print("🚀 销售数据分析系统 - 测试执行")
    print("=" * 50)
    print(f"测试开始时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # 检查环境
    print("\n📋 环境检查")
    print("-" * 20)
    
    # 检查Python版本
    python_version = sys.version_info
    print(f"Python版本: {python_version.major}.{python_version.minor}.{python_version.micro}")
    
    # 检查必要文件
    required_files = [
        "simple_app.py",
        "simple_init_db.py", 
        "data/sample_sales_data.csv",
        "tests/test_comprehensive.py"
    ]
    
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"✅ {file_path}")
        else:
            print(f"❌ {file_path} - 文件不存在")
            return False
    
    # 检查应用是否运行
    if not check_application_running():
        print("\n⚠️  应用未运行，请先启动应用:")
        print("   python simple_app.py")
        return False
    
    # 运行测试
    print("\n🧪 开始执行测试")
    print("=" * 50)
    
    test_results = []
    
    # 1. 运行pytest测试
    test_results.append(
        run_test_command(
            "python -m pytest tests/test_comprehensive.py -v",
            "运行Pytest测试套件"
        )
    )
    
    # 2. 运行综合测试
    test_results.append(
        run_test_command(
            "python tests/test_comprehensive.py",
            "运行综合测试脚本"
        )
    )
    
    # 3. 运行API测试
    test_results.append(
        run_test_command(
            "python -c \"import httpx; response = httpx.get('http://localhost:8000/api/v1/sales/'); print(f'API测试: {response.status_code}')\"",
            "运行API连接测试"
        )
    )
    
    # 4. 检查数据库
    test_results.append(
        run_test_command(
            "python -c \"import sqlite3; conn = sqlite3.connect('sales_analyzer.db'); cursor = conn.cursor(); cursor.execute('SELECT COUNT(*) FROM sales_records'); print(f'数据库记录数: {cursor.fetchone()[0]}'); conn.close()\"",
            "检查数据库状态"
        )
    )
    
    # 输出测试结果摘要
    print("\n" + "=" * 50)
    print("📊 测试结果摘要")
    print(f"总测试数: {len(test_results)}")
    print(f"通过数: {sum(test_results)}")
    print(f"失败数: {len(test_results) - sum(test_results)}")
    print(f"通过率: {(sum(test_results)/len(test_results)*100):.1f}%")
    
    if all(test_results):
        print("\n🎉 所有测试通过！系统运行正常。")
        return True
    else:
        print("\n⚠️  部分测试失败，请检查系统配置。")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 