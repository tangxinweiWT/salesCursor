"""
销售数据模型定义
"""
from sqlalchemy import Column, Integer, String, Float, DateTime, Text
from sqlalchemy.sql import func
from app.core.database import Base

class SalesRecord(Base):
    """销售记录模型"""
    __tablename__ = "sales_records"
    
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(String(100), index=True, comment="订单ID")
    product_name = Column(String(200), index=True, comment="产品名称")
    category = Column(String(100), index=True, comment="产品类别")
    customer_name = Column(String(100), index=True, comment="客户名称")
    region = Column(String(100), index=True, comment="销售区域")
    sales_amount = Column(Float, comment="销售金额")
    quantity = Column(Integer, comment="销售数量")
    unit_price = Column(Float, comment="单价")
    sales_date = Column(DateTime, index=True, comment="销售日期")
    sales_person = Column(String(100), index=True, comment="销售人员")
    payment_method = Column(String(50), comment="支付方式")
    created_at = Column(DateTime, default=func.now(), comment="创建时间")
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), comment="更新时间")
    
    def __repr__(self):
        return f"<SalesRecord(id={self.id}, order_id='{self.order_id}', product='{self.product_name}')>"

class DataImportLog(Base):
    """数据导入日志模型"""
    __tablename__ = "data_import_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String(255), comment="文件名")
    file_size = Column(Integer, comment="文件大小(字节)")
    records_imported = Column(Integer, comment="导入记录数")
    import_status = Column(String(50), comment="导入状态")
    error_message = Column(Text, nullable=True, comment="错误信息")
    imported_at = Column(DateTime, default=func.now(), comment="导入时间")
    
    def __repr__(self):
        return f"<DataImportLog(id={self.id}, filename='{self.filename}', status='{self.import_status}')>" 