"""
数据分析API端点
"""
from typing import Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.sales import SalesRecord

router = APIRouter()

@router.get("/top-products")
async def get_top_products(
    limit: int = Query(10, description="返回产品数量"),
    db: Session = Depends(get_db)
):
    """获取热销产品排行"""
    from sqlalchemy import func
    
    top_products = db.query(
        SalesRecord.product_name,
        func.sum(SalesRecord.sales_amount).label('total_sales'),
        func.sum(SalesRecord.quantity).label('total_quantity'),
        func.count(SalesRecord.id).label('order_count')
    ).group_by(SalesRecord.product_name)\
     .order_by(func.sum(SalesRecord.sales_amount).desc())\
     .limit(limit).all()
    
    return [
        {
            "product_name": p.product_name,
            "total_sales": float(p.total_sales),
            "total_quantity": int(p.total_quantity),
            "order_count": int(p.order_count)
        }
        for p in top_products
    ]

@router.get("/top-regions")
async def get_top_regions(
    limit: int = Query(10, description="返回区域数量"),
    db: Session = Depends(get_db)
):
    """获取热销区域排行"""
    from sqlalchemy import func
    
    top_regions = db.query(
        SalesRecord.region,
        func.sum(SalesRecord.sales_amount).label('total_sales'),
        func.count(SalesRecord.id).label('order_count')
    ).group_by(SalesRecord.region)\
     .order_by(func.sum(SalesRecord.sales_amount).desc())\
     .limit(limit).all()
    
    return [
        {
            "region": r.region,
            "total_sales": float(r.total_sales),
            "order_count": int(r.order_count)
        }
        for r in top_regions
    ]

@router.get("/sales-trend")
async def get_sales_trend(
    start_date: Optional[str] = Query(None, description="开始日期 (YYYY-MM-DD)"),
    end_date: Optional[str] = Query(None, description="结束日期 (YYYY-MM-DD)"),
    db: Session = Depends(get_db)
):
    """获取销售趋势数据"""
    from sqlalchemy import func
    from datetime import datetime
    
    query = db.query(
        func.date(SalesRecord.sales_date).label('date'),
        func.sum(SalesRecord.sales_amount).label('daily_sales'),
        func.count(SalesRecord.id).label('daily_orders')
    ).group_by(func.date(SalesRecord.sales_date))
    
    if start_date:
        query = query.filter(SalesRecord.sales_date >= start_date)
    
    if end_date:
        query = query.filter(SalesRecord.sales_date <= end_date)
    
    trend_data = query.order_by(func.date(SalesRecord.sales_date)).all()
    
    return [
        {
            "date": str(t.date),
            "daily_sales": float(t.daily_sales),
            "daily_orders": int(t.daily_orders)
        }
        for t in trend_data
    ] 