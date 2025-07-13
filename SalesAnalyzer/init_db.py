"""
数据库初始化脚本
"""
from app.core.database import engine, Base
from app.models.sales import SalesRecord, DataImportLog

def init_database():
    """初始化数据库表"""
    print("正在创建数据库表...")
    Base.metadata.create_all(bind=engine)
    print("数据库表创建完成!")

if __name__ == "__main__":
    init_database() 