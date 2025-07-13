"""
销售数据Pydantic模式定义
"""
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field

class SalesRecordBase(BaseModel):
    """销售记录基础模式"""
    order_id: str = Field(..., description="订单ID")
    product_name: str = Field(..., description="产品名称")
    category: str = Field(..., description="产品类别")
    customer_name: str = Field(..., description="客户名称")
    region: str = Field(..., description="销售区域")
    sales_amount: float = Field(..., description="销售金额")
    quantity: int = Field(..., description="销售数量")
    unit_price: float = Field(..., description="单价")
    sales_date: datetime = Field(..., description="销售日期")
    sales_person: str = Field(..., description="销售人员")
    payment_method: str = Field(..., description="支付方式")

class SalesRecordCreate(SalesRecordBase):
    """创建销售记录模式"""
    pass

class SalesRecord(SalesRecordBase):
    """销售记录完整模式"""
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class SalesRecordUpdate(BaseModel):
    """更新销售记录模式"""
    order_id: Optional[str] = None
    product_name: Optional[str] = None
    category: Optional[str] = None
    customer_name: Optional[str] = None
    region: Optional[str] = None
    sales_amount: Optional[float] = None
    quantity: Optional[int] = None
    unit_price: Optional[float] = None
    sales_date: Optional[datetime] = None
    sales_person: Optional[str] = None
    payment_method: Optional[str] = None

class SalesQuery(BaseModel):
    """销售数据查询模式"""
    start_date: Optional[datetime] = Field(None, description="开始日期")
    end_date: Optional[datetime] = Field(None, description="结束日期")
    region: Optional[str] = Field(None, description="销售区域")
    category: Optional[str] = Field(None, description="产品类别")
    sales_person: Optional[str] = Field(None, description="销售人员")
    customer_name: Optional[str] = Field(None, description="客户名称")
    limit: Optional[int] = Field(100, description="返回记录数限制")
    offset: Optional[int] = Field(0, description="偏移量")

class SalesStatistics(BaseModel):
    """销售统计信息模式"""
    total_sales: float = Field(..., description="总销售额")
    total_quantity: int = Field(..., description="总销售数量")
    total_orders: int = Field(..., description="总订单数")
    avg_order_value: float = Field(..., description="平均订单价值")
    top_products: List[dict] = Field(..., description="热销产品")
    top_regions: List[dict] = Field(..., description="热销区域")
    sales_trend: List[dict] = Field(..., description="销售趋势")

class DataImportResponse(BaseModel):
    """数据导入响应模式"""
    success: bool = Field(..., description="导入是否成功")
    filename: str = Field(..., description="文件名")
    records_imported: int = Field(..., description="导入记录数")
    message: str = Field(..., description="响应消息")
    errors: Optional[List[str]] = Field(None, description="错误信息列表") 