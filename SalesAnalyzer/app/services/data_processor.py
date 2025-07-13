"""
数据处理服务
"""
import pandas as pd
import numpy as np
from datetime import datetime
from typing import List, Dict, Optional, Tuple
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.sales import SalesRecord, DataImportLog
from app.schemas.sales import SalesRecordCreate, DataImportResponse
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

class DataProcessor:
    """数据处理服务类"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def process_csv_file(self, file_path: str, filename: str) -> DataImportResponse:
        """处理CSV文件并导入数据库"""
        try:
            # 读取CSV文件
            df = pd.read_csv(file_path)
            
            # 数据清洗和验证
            cleaned_df = self._clean_data(df)
            
            # 转换为数据库记录
            records = self._convert_to_records(cleaned_df)
            
            # 批量插入数据库
            self.db.add_all(records)
            self.db.commit()
            
            # 记录导入日志
            import_log = DataImportLog(
                filename=filename,
                file_size=len(records),
                records_imported=len(records),
                import_status="success"
            )
            self.db.add(import_log)
            self.db.commit()
            
            return DataImportResponse(
                success=True,
                filename=filename,
                records_imported=len(records),
                message=f"成功导入 {len(records)} 条销售记录"
            )
            
        except Exception as e:
            logger.error(f"处理文件 {filename} 时发生错误: {str(e)}")
            self.db.rollback()
            
            # 记录错误日志
            import_log = DataImportLog(
                filename=filename,
                file_size=0,
                records_imported=0,
                import_status="failed",
                error_message=str(e)
            )
            self.db.add(import_log)
            self.db.commit()
            
            return DataImportResponse(
                success=False,
                filename=filename,
                records_imported=0,
                message=f"导入失败: {str(e)}",
                errors=[str(e)]
            )
    
    def _clean_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """数据清洗"""
        # 删除重复行
        df = df.drop_duplicates()
        
        # 删除空值行
        df = df.dropna()
        
        # 标准化列名
        df.columns = df.columns.str.strip().str.lower()
        
        # 数据类型转换
        if 'sales_amount' in df.columns:
            df['sales_amount'] = pd.to_numeric(df['sales_amount'], errors='coerce')
        
        if 'quantity' in df.columns:
            df['quantity'] = pd.to_numeric(df['quantity'], errors='coerce').astype(int)
        
        if 'unit_price' in df.columns:
            df['unit_price'] = pd.to_numeric(df['unit_price'], errors='coerce')
        
        if 'sales_date' in df.columns:
            df['sales_date'] = pd.to_datetime(df['sales_date'], errors='coerce')
        
        # 删除无效数据
        df = df.dropna()
        
        return df
    
    def _convert_to_records(self, df: pd.DataFrame) -> List[SalesRecord]:
        """将DataFrame转换为数据库记录"""
        records = []
        
        for _, row in df.iterrows():
            try:
                record = SalesRecord(
                    order_id=str(row.get('order_id', '')),
                    product_name=str(row.get('product_name', '')),
                    category=str(row.get('category', '')),
                    customer_name=str(row.get('customer_name', '')),
                    region=str(row.get('region', '')),
                    sales_amount=float(row.get('sales_amount', 0)),
                    quantity=int(row.get('quantity', 0)),
                    unit_price=float(row.get('unit_price', 0)),
                    sales_date=row.get('sales_date', datetime.now()),
                    sales_person=str(row.get('sales_person', '')),
                    payment_method=str(row.get('payment_method', ''))
                )
                records.append(record)
            except Exception as e:
                logger.warning(f"转换记录时跳过无效数据: {e}")
                continue
        
        return records
    
    def get_sales_statistics(self, query_params: Dict) -> Dict:
        """获取销售统计信息"""
        # 构建查询条件
        query = self.db.query(SalesRecord)
        
        if query_params.get('start_date'):
            query = query.filter(SalesRecord.sales_date >= query_params['start_date'])
        
        if query_params.get('end_date'):
            query = query.filter(SalesRecord.sales_date <= query_params['end_date'])
        
        if query_params.get('region'):
            query = query.filter(SalesRecord.region == query_params['region'])
        
        if query_params.get('category'):
            query = query.filter(SalesRecord.category == query_params['category'])
        
        # 获取基础统计
        total_sales = query.with_entities(
            func.sum(SalesRecord.sales_amount).label('total_sales'),
            func.sum(SalesRecord.quantity).label('total_quantity'),
            func.count(SalesRecord.id).label('total_orders')
        ).first()
        
        # 计算平均订单价值
        avg_order_value = total_sales.total_sales / total_sales.total_orders if total_sales.total_orders > 0 else 0
        
        # 获取热销产品
        top_products = self.db.query(
            SalesRecord.product_name,
            func.sum(SalesRecord.sales_amount).label('total_sales'),
            func.sum(SalesRecord.quantity).label('total_quantity')
        ).group_by(SalesRecord.product_name)\
         .order_by(func.sum(SalesRecord.sales_amount).desc())\
         .limit(10).all()
        
        # 获取热销区域
        top_regions = self.db.query(
            SalesRecord.region,
            func.sum(SalesRecord.sales_amount).label('total_sales')
        ).group_by(SalesRecord.region)\
         .order_by(func.sum(SalesRecord.sales_amount).desc())\
         .limit(10).all()
        
        return {
            "total_sales": float(total_sales.total_sales or 0),
            "total_quantity": int(total_sales.total_quantity or 0),
            "total_orders": int(total_sales.total_orders or 0),
            "avg_order_value": float(avg_order_value),
            "top_products": [
                {
                    "product_name": p.product_name,
                    "total_sales": float(p.total_sales),
                    "total_quantity": int(p.total_quantity)
                } for p in top_products
            ],
            "top_regions": [
                {
                    "region": r.region,
                    "total_sales": float(r.total_sales)
                } for r in top_regions
            ]
        } 