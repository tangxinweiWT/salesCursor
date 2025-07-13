"""
销售数据API端点
"""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.sales import SalesRecord
from app.schemas.sales import SalesRecord as SalesRecordSchema, SalesQuery

router = APIRouter()

@router.get("/", response_model=List[SalesRecordSchema])
async def get_sales_records(
    skip: int = Query(0, description="跳过记录数"),
    limit: int = Query(100, description="返回记录数"),
    region: Optional[str] = Query(None, description="销售区域"),
    category: Optional[str] = Query(None, description="产品类别"),
    db: Session = Depends(get_db)
):
    """获取销售记录列表"""
    query = db.query(SalesRecord)
    
    if region:
        query = query.filter(SalesRecord.region == region)
    
    if category:
        query = query.filter(SalesRecord.category == category)
    
    records = query.offset(skip).limit(limit).all()
    return records

@router.get("/{record_id}", response_model=SalesRecordSchema)
async def get_sales_record(record_id: int, db: Session = Depends(get_db)):
    """根据ID获取销售记录"""
    record = db.query(SalesRecord).filter(SalesRecord.id == record_id).first()
    if not record:
        raise HTTPException(status_code=404, detail="销售记录不存在")
    return record

@router.get("/statistics/summary")
async def get_sales_summary(db: Session = Depends(get_db)):
    """获取销售数据摘要"""
    from sqlalchemy import func
    
    # 基础统计
    total_sales = db.query(func.sum(SalesRecord.sales_amount)).scalar() or 0
    total_orders = db.query(func.count(SalesRecord.id)).scalar() or 0
    total_quantity = db.query(func.sum(SalesRecord.quantity)).scalar() or 0
    
    # 平均订单价值
    avg_order_value = total_sales / total_orders if total_orders > 0 else 0
    
    return {
        "total_sales": float(total_sales),
        "total_orders": int(total_orders),
        "total_quantity": int(total_quantity),
        "avg_order_value": float(avg_order_value)
    } 