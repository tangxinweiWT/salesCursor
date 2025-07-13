"""
API v1 路由主文件
"""
from fastapi import APIRouter
from app.api.api_v1.endpoints import sales, upload, analytics

api_router = APIRouter()

# 注册各个模块的路由
api_router.include_router(sales.router, prefix="/sales", tags=["销售数据"])
api_router.include_router(upload.router, prefix="/upload", tags=["数据上传"])
api_router.include_router(analytics.router, prefix="/analytics", tags=["数据分析"]) 