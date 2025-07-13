"""
简化的数据库初始化脚本
"""
import os
import sys

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def init_database():
    """初始化数据库"""
    try:
        print("🗄️  初始化数据库...")
        
        # 导入必要的模块
        from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Text
        from sqlalchemy.ext.declarative import declarative_base
        from sqlalchemy.orm import sessionmaker
        from datetime import datetime
        
        # 创建数据库引擎
        DATABASE_URL = "sqlite:///./sales_analyzer.db"
        engine = create_engine(
            DATABASE_URL,
            connect_args={"check_same_thread": False}
        )
        
        # 创建基础模型类
        Base = declarative_base()
        
        # 定义销售记录模型
        class SalesRecord(Base):
            __tablename__ = "sales_records"
            
            id = Column(Integer, primary_key=True, index=True)
            order_id = Column(String(100), index=True)
            product_name = Column(String(200), index=True)
            category = Column(String(100), index=True)
            customer_name = Column(String(100), index=True)
            region = Column(String(100), index=True)
            sales_amount = Column(Float)
            quantity = Column(Integer)
            unit_price = Column(Float)
            sales_date = Column(DateTime, index=True)
            sales_person = Column(String(100), index=True)
            payment_method = Column(String(50))
            created_at = Column(DateTime, default=datetime.now)
            updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
        
        # 定义数据导入日志模型
        class DataImportLog(Base):
            __tablename__ = "data_import_logs"
            
            id = Column(Integer, primary_key=True, index=True)
            filename = Column(String(255))
            file_size = Column(Integer)
            records_imported = Column(Integer)
            import_status = Column(String(50))
            error_message = Column(Text, nullable=True)
            imported_at = Column(DateTime, default=datetime.now)
        
        # 创建表
        Base.metadata.create_all(bind=engine)
        
        print("✅ 数据库表创建完成!")
        print("📁 数据库文件: sales_analyzer.db")
        
    except Exception as e:
        print(f"❌ 数据库初始化失败: {e}")
        print("请检查依赖是否正确安装")

if __name__ == "__main__":
    init_database() 