"""
简化的销售数据分析系统主应用
"""
from fastapi import FastAPI, HTTPException, UploadFile, File, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Text, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from datetime import datetime
from typing import List, Optional
import pandas as pd
import os
import shutil

# 创建FastAPI应用
app = FastAPI(
    title="销售数据分析系统",
    description="基于FastAPI的销售数据分析系统",
    version="1.0.0"
)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 数据库配置
DATABASE_URL = "sqlite:///./sales_analyzer.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# 数据模型
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

# 添加初始数据的函数
def load_sample_data():
    """加载示例数据"""
    db = SessionLocal()
    try:
        # 检查是否已有数据
        existing_count = db.query(func.count(SalesRecord.id)).scalar()
        if existing_count > 0:
            print(f"数据库中已有 {existing_count} 条记录，跳过初始数据加载")
            return
        
        # 示例数据
        sample_data = [
            {
                "order_id": "ORD001", "product_name": "笔记本电脑", "category": "电子产品",
                "customer_name": "张三", "region": "北京", "sales_amount": 8999.00,
                "quantity": 1, "unit_price": 8999.00, "sales_date": "2024-01-15",
                "sales_person": "李销售", "payment_method": "信用卡"
            },
            {
                "order_id": "ORD002", "product_name": "智能手机", "category": "电子产品",
                "customer_name": "李四", "region": "上海", "sales_amount": 5999.00,
                "quantity": 1, "unit_price": 5999.00, "sales_date": "2024-01-16",
                "sales_person": "王销售", "payment_method": "支付宝"
            },
            {
                "order_id": "ORD003", "product_name": "办公椅", "category": "办公用品",
                "customer_name": "王五", "region": "广州", "sales_amount": 899.00,
                "quantity": 2, "unit_price": 449.50, "sales_date": "2024-01-17",
                "sales_person": "赵销售", "payment_method": "微信支付"
            },
            {
                "order_id": "ORD004", "product_name": "打印机", "category": "办公用品",
                "customer_name": "赵六", "region": "深圳", "sales_amount": 1299.00,
                "quantity": 1, "unit_price": 1299.00, "sales_date": "2024-01-18",
                "sales_person": "钱销售", "payment_method": "银行转账"
            },
            {
                "order_id": "ORD005", "product_name": "平板电脑", "category": "电子产品",
                "customer_name": "孙七", "region": "杭州", "sales_amount": 3999.00,
                "quantity": 1, "unit_price": 3999.00, "sales_date": "2024-01-19",
                "sales_person": "孙销售", "payment_method": "信用卡"
            },
            {
                "order_id": "ORD006", "product_name": "办公桌", "category": "办公用品",
                "customer_name": "周八", "region": "南京", "sales_amount": 1599.00,
                "quantity": 1, "unit_price": 1599.00, "sales_date": "2024-01-20",
                "sales_person": "吴销售", "payment_method": "支付宝"
            },
            {
                "order_id": "ORD007", "product_name": "耳机", "category": "电子产品",
                "customer_name": "吴九", "region": "成都", "sales_amount": 299.00,
                "quantity": 3, "unit_price": 99.67, "sales_date": "2024-01-21",
                "sales_person": "郑销售", "payment_method": "微信支付"
            },
            {
                "order_id": "ORD008", "product_name": "显示器", "category": "电子产品",
                "customer_name": "郑十", "region": "武汉", "sales_amount": 1899.00,
                "quantity": 1, "unit_price": 1899.00, "sales_date": "2024-01-22",
                "sales_person": "王销售", "payment_method": "信用卡"
            },
            {
                "order_id": "ORD009", "product_name": "键盘", "category": "电子产品",
                "customer_name": "刘一", "region": "西安", "sales_amount": 199.00,
                "quantity": 5, "unit_price": 39.80, "sales_date": "2024-01-23",
                "sales_person": "李销售", "payment_method": "支付宝"
            },
            {
                "order_id": "ORD010", "product_name": "鼠标", "category": "电子产品",
                "customer_name": "陈二", "region": "重庆", "sales_amount": 89.00,
                "quantity": 10, "unit_price": 8.90, "sales_date": "2024-01-24",
                "sales_person": "赵销售", "payment_method": "微信支付"
            },
            {
                "order_id": "ORD011", "product_name": "笔记本电脑", "category": "电子产品",
                "customer_name": "杨三", "region": "北京", "sales_amount": 12999.00,
                "quantity": 1, "unit_price": 12999.00, "sales_date": "2024-01-25",
                "sales_person": "钱销售", "payment_method": "银行转账"
            },
            {
                "order_id": "ORD012", "product_name": "智能手机", "category": "电子产品",
                "customer_name": "黄四", "region": "上海", "sales_amount": 7999.00,
                "quantity": 1, "unit_price": 7999.00, "sales_date": "2024-01-26",
                "sales_person": "孙销售", "payment_method": "信用卡"
            },
            {
                "order_id": "ORD013", "product_name": "办公椅", "category": "办公用品",
                "customer_name": "胡五", "region": "广州", "sales_amount": 1299.00,
                "quantity": 1, "unit_price": 1299.00, "sales_date": "2024-01-27",
                "sales_person": "吴销售", "payment_method": "支付宝"
            },
            {
                "order_id": "ORD014", "product_name": "打印机", "category": "办公用品",
                "customer_name": "郭六", "region": "深圳", "sales_amount": 899.00,
                "quantity": 2, "unit_price": 449.50, "sales_date": "2024-01-28",
                "sales_person": "郑销售", "payment_method": "微信支付"
            },
            {
                "order_id": "ORD015", "product_name": "平板电脑", "category": "电子产品",
                "customer_name": "何七", "region": "杭州", "sales_amount": 2999.00,
                "quantity": 1, "unit_price": 2999.00, "sales_date": "2024-01-29",
                "sales_person": "王销售", "payment_method": "信用卡"
            }
        ]
        
        # 插入数据
        for data in sample_data:
            record = SalesRecord(
                order_id=data["order_id"],
                product_name=data["product_name"],
                category=data["category"],
                customer_name=data["customer_name"],
                region=data["region"],
                sales_amount=data["sales_amount"],
                quantity=data["quantity"],
                unit_price=data["unit_price"],
                sales_date=datetime.strptime(data["sales_date"], "%Y-%m-%d"),
                sales_person=data["sales_person"],
                payment_method=data["payment_method"]
            )
            db.add(record)
        
        db.commit()
        print(f"成功加载 {len(sample_data)} 条示例数据")
        
    except Exception as e:
        print(f"加载示例数据时出错: {e}")
        db.rollback()
    finally:
        db.close()

# 依赖函数
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# API路由
@app.get("/")
async def root():
    """根路径"""
    return {
        "message": "欢迎使用销售数据分析系统",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health"
    }

@app.get("/health")
async def health_check():
    """健康检查"""
    return {"status": "healthy", "message": "系统运行正常"}

@app.get("/api/v1/sales/")
async def get_sales_records(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """获取销售记录列表"""
    records = db.query(SalesRecord).offset(skip).limit(limit).all()
    return [
        {
            "id": record.id,
            "order_id": record.order_id,
            "product_name": record.product_name,
            "category": record.category,
            "customer_name": record.customer_name,
            "region": record.region,
            "sales_amount": record.sales_amount,
            "quantity": record.quantity,
            "unit_price": record.unit_price,
            "sales_date": record.sales_date.isoformat() if record.sales_date else None,
            "sales_person": record.sales_person,
            "payment_method": record.payment_method
        }
        for record in records
    ]

@app.get("/api/v1/sales/statistics/summary")
async def get_sales_summary(db: Session = Depends(get_db)):
    """获取销售摘要"""
    total_sales = db.query(func.sum(SalesRecord.sales_amount)).scalar() or 0
    total_orders = db.query(func.count(SalesRecord.id)).scalar() or 0
    total_quantity = db.query(func.sum(SalesRecord.quantity)).scalar() or 0
    avg_order_value = total_sales / total_orders if total_orders > 0 else 0
    
    return {
        "total_sales": float(total_sales),
        "total_orders": int(total_orders),
        "total_quantity": int(total_quantity),
        "avg_order_value": float(avg_order_value)
    }

@app.post("/api/v1/upload/csv")
async def upload_csv(file: UploadFile = File(...), db: Session = Depends(get_db)):
    """上传CSV文件"""
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="只支持CSV文件")
    
    # 保存文件
    upload_dir = "data/uploads"
    os.makedirs(upload_dir, exist_ok=True)
    file_path = os.path.join(upload_dir, file.filename)
    
    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # 读取和处理CSV
        df = pd.read_csv(file_path)
        records_imported = 0
        
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
                    sales_date=pd.to_datetime(row.get('sales_date', datetime.now())),
                    sales_person=str(row.get('sales_person', '')),
                    payment_method=str(row.get('payment_method', ''))
                )
                db.add(record)
                records_imported += 1
            except Exception as e:
                continue
        
        db.commit()
        
        # 记录导入日志
        import_log = DataImportLog(
            filename=file.filename,
            file_size=len(df),
            records_imported=records_imported,
            import_status="success"
        )
        db.add(import_log)
        db.commit()
        
        # 清理临时文件
        os.remove(file_path)
        
        return {
            "success": True,
            "filename": file.filename,
            "records_imported": records_imported,
            "message": f"成功导入 {records_imported} 条记录"
        }
        
    except Exception as e:
        db.rollback()
        if os.path.exists(file_path):
            os.remove(file_path)
        raise HTTPException(status_code=500, detail=f"处理文件失败: {str(e)}")

@app.get("/api/v1/analytics/top-products")
async def get_top_products(limit: int = 10, db: Session = Depends(get_db)):
    """获取热销产品"""
    top_products = db.query(
        SalesRecord.product_name,
        func.sum(SalesRecord.sales_amount).label('total_sales'),
        func.sum(SalesRecord.quantity).label('total_quantity')
    ).group_by(SalesRecord.product_name)\
     .order_by(func.sum(SalesRecord.sales_amount).desc())\
     .limit(limit).all()
    
    return [
        {
            "product_name": p.product_name,
            "total_sales": float(p.total_sales),
            "total_quantity": int(p.total_quantity)
        }
        for p in top_products
    ]

@app.get("/api/v1/analytics/top-regions")
async def get_top_regions(limit: int = 10, db: Session = Depends(get_db)):
    """获取热销区域"""
    top_regions = db.query(
        SalesRecord.region,
        func.sum(SalesRecord.sales_amount).label('total_sales')
    ).group_by(SalesRecord.region)\
     .order_by(func.sum(SalesRecord.sales_amount).desc())\
     .limit(limit).all()
    
    return [
        {
            "region": r.region,
            "total_sales": float(r.total_sales)
        }
        for r in top_regions
    ]

# 添加前端期望的API端点
@app.get("/sales/stats")
async def get_sales_stats(db: Session = Depends(get_db)):
    """获取销售统计信息"""
    total_sales = db.query(func.sum(SalesRecord.sales_amount)).scalar() or 0
    total_orders = db.query(func.count(SalesRecord.id)).scalar() or 0
    total_quantity = db.query(func.sum(SalesRecord.quantity)).scalar() or 0
    avg_order_value = total_sales / total_orders if total_orders > 0 else 0
    
    return {
        "total_sales": float(total_sales),
        "total_orders": int(total_orders),
        "total_quantity": int(total_quantity),
        "avg_order_value": float(avg_order_value)
    }

@app.get("/sales/trend")
async def get_sales_trend(days: int = 30, db: Session = Depends(get_db)):
    """获取销售趋势"""
    from datetime import timedelta
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)
    
    # 按日期分组统计销售
    daily_sales = db.query(
        func.date(SalesRecord.sales_date).label('date'),
        func.sum(SalesRecord.sales_amount).label('daily_sales'),
        func.count(SalesRecord.id).label('daily_orders')
    ).filter(
        SalesRecord.sales_date >= start_date,
        SalesRecord.sales_date <= end_date
    ).group_by(func.date(SalesRecord.sales_date))\
     .order_by(func.date(SalesRecord.sales_date)).all()
    
    return [
        {
            "date": str(d.date),
            "sales": float(d.daily_sales),
            "orders": int(d.daily_orders)
        }
        for d in daily_sales
    ]

@app.get("/sales/category-stats")
async def get_category_stats(db: Session = Depends(get_db)):
    """获取分类统计"""
    category_stats = db.query(
        SalesRecord.category,
        func.sum(SalesRecord.sales_amount).label('total_sales'),
        func.count(SalesRecord.id).label('total_orders'),
        func.sum(SalesRecord.quantity).label('total_quantity')
    ).group_by(SalesRecord.category)\
     .order_by(func.sum(SalesRecord.sales_amount).desc()).all()
    
    return [
        {
            "category": c.category,
            "total_sales": float(c.total_sales),
            "total_orders": int(c.total_orders),
            "total_quantity": int(c.total_quantity)
        }
        for c in category_stats
    ]

@app.get("/sales/list")
async def get_sales_list(
    page: int = 1,
    size: int = 20,
    limit: int = None,
    db: Session = Depends(get_db)
):
    """获取销售记录列表（支持分页）"""
    if limit:
        # 如果指定了limit，使用limit而不是分页
        records = db.query(SalesRecord).limit(limit).all()
        return [
            {
                "id": record.id,
                "order_id": record.order_id,
                "product_name": record.product_name,
                "category": record.category,
                "customer_name": record.customer_name,
                "region": record.region,
                "sales_amount": record.sales_amount,
                "quantity": record.quantity,
                "unit_price": record.unit_price,
                "sales_date": record.sales_date.isoformat() if record.sales_date else None,
                "sales_person": record.sales_person,
                "payment_method": record.payment_method
            }
            for record in records
        ]
    else:
        # 使用分页
        skip = (page - 1) * size
        records = db.query(SalesRecord).offset(skip).limit(size).all()
        total = db.query(func.count(SalesRecord.id)).scalar()
        
        return {
            "data": [
                {
                    "id": record.id,
                    "order_id": record.order_id,
                    "product_name": record.product_name,
                    "category": record.category,
                    "customer_name": record.customer_name,
                    "region": record.region,
                    "sales_amount": record.sales_amount,
                    "quantity": record.quantity,
                    "unit_price": record.unit_price,
                    "sales_date": record.sales_date.isoformat() if record.sales_date else None,
                    "sales_person": record.sales_person,
                    "payment_method": record.payment_method
                }
                for record in records
            ],
            "pagination": {
                "page": page,
                "size": size,
                "total": total,
                "pages": (total + size - 1) // size
            }
        }

@app.get("/sales/query")
async def query_sales(
    page: int = 1,
    size: int = 20,
    db: Session = Depends(get_db)
):
    """查询销售记录（别名，与list相同）"""
    return await get_sales_list(page=page, size=size, db=db)

@app.post("/sales/upload")
async def upload_sales_file(file: UploadFile = File(...), db: Session = Depends(get_db)):
    """上传销售数据文件（别名，与/api/v1/upload/csv相同）"""
    return await upload_csv(file=file, db=db)

@app.get("/sales/export")
async def export_sales(
    page: int = 1,
    size: int = 20,
    db: Session = Depends(get_db)
):
    """导出销售数据"""
    skip = (page - 1) * size
    records = db.query(SalesRecord).offset(skip).limit(size).all()
    
    # 转换为CSV格式
    import io
    import csv
    
    output = io.StringIO()
    writer = csv.writer(output)
    
    # 写入表头
    writer.writerow([
        'ID', '订单ID', '产品名称', '分类', '客户名称', '区域', 
        '销售金额', '数量', '单价', '销售日期', '销售人员', '支付方式'
    ])
    
    # 写入数据
    for record in records:
        writer.writerow([
            record.id, record.order_id, record.product_name, record.category,
            record.customer_name, record.region, record.sales_amount, record.quantity,
            record.unit_price, record.sales_date.strftime('%Y-%m-%d') if record.sales_date else '',
            record.sales_person, record.payment_method
        ])
    
    from fastapi.responses import StreamingResponse
    
    output.seek(0)
    return StreamingResponse(
        io.BytesIO(output.getvalue().encode('utf-8')),
        media_type="text/csv",
        headers={"Content-Disposition": f"attachment; filename=sales_export_page_{page}.csv"}
    )

if __name__ == "__main__":
    import uvicorn
    # 启动时加载示例数据
    load_sample_data()
    uvicorn.run(app, host="0.0.0.0", port=8000) 