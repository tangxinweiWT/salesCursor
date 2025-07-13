"""
简化的应用启动脚本
"""
import uvicorn
import os
import sys

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def main():
    """启动应用"""
    print("🚀 启动销售数据分析系统...")
    print("📊 系统信息:")
    print("   - 应用名称: 销售数据分析系统")
    print("   - 版本: 1.0.0")
    print("   - 端口: 8000")
    print("   - 文档地址: http://localhost:8000/docs")
    print("   - 健康检查: http://localhost:8000/health")
    print()
    
    try:
        # 启动应用
        uvicorn.run(
            "app.main:app",
            host="0.0.0.0",
            port=8000,
            reload=True,
            log_level="info"
        )
    except KeyboardInterrupt:
        print("\n👋 应用已停止")
    except Exception as e:
        print(f"❌ 启动失败: {e}")
        print("请检查依赖是否正确安装")

if __name__ == "__main__":
    main() 