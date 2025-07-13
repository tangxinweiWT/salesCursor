"""
文件上传API端点
"""
import os
import shutil
from typing import List
from fastapi import APIRouter, Depends, File, UploadFile, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.config import settings
from app.services.data_processor import DataProcessor
from app.schemas.sales import DataImportResponse

router = APIRouter()

@router.post("/csv", response_model=DataImportResponse)
async def upload_csv_file(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """上传CSV文件并处理"""
    # 验证文件类型
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="只支持CSV文件")
    
    # 验证文件大小
    if file.size and file.size > settings.MAX_FILE_SIZE:
        raise HTTPException(status_code=400, detail="文件大小超过限制")
    
    # 保存文件
    file_path = os.path.join(settings.UPLOAD_DIR, file.filename)
    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"文件保存失败: {str(e)}")
    
    # 处理文件
    processor = DataProcessor(db)
    result = processor.process_csv_file(file_path, file.filename)
    
    # 清理临时文件
    try:
        os.remove(file_path)
    except:
        pass
    
    return result

@router.get("/history")
async def get_upload_history(db: Session = Depends(get_db)):
    """获取上传历史"""
    from app.models.sales import DataImportLog
    
    logs = db.query(DataImportLog).order_by(DataImportLog.imported_at.desc()).limit(20).all()
    
    return [
        {
            "id": log.id,
            "filename": log.filename,
            "file_size": log.file_size,
            "records_imported": log.records_imported,
            "import_status": log.import_status,
            "imported_at": log.imported_at,
            "error_message": log.error_message
        }
        for log in logs
    ] 