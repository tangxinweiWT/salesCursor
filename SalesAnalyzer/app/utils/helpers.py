"""
辅助工具函数
"""
import os
import hashlib
from datetime import datetime
from typing import List, Dict, Any

def validate_file_extension(filename: str, allowed_extensions: List[str]) -> bool:
    """验证文件扩展名"""
    return any(filename.lower().endswith(ext.lower()) for ext in allowed_extensions)

def generate_file_hash(file_path: str) -> str:
    """生成文件哈希值"""
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def format_currency(amount: float) -> str:
    """格式化货币显示"""
    return f"¥{amount:,.2f}"

def format_percentage(value: float, total: float) -> str:
    """格式化百分比显示"""
    if total == 0:
        return "0.00%"
    return f"{(value / total * 100):.2f}%"

def safe_divide(numerator: float, denominator: float, default: float = 0.0) -> float:
    """安全除法，避免除零错误"""
    return numerator / denominator if denominator != 0 else default

def parse_date_range(start_date: str, end_date: str) -> tuple:
    """解析日期范围"""
    try:
        start = datetime.strptime(start_date, "%Y-%m-%d")
        end = datetime.strptime(end_date, "%Y-%m-%d")
        return start, end
    except ValueError:
        raise ValueError("日期格式错误，请使用 YYYY-MM-DD 格式")

def create_directory_if_not_exists(directory_path: str) -> None:
    """如果目录不存在则创建"""
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)

def clean_data_value(value: Any) -> Any:
    """清理数据值"""
    if isinstance(value, str):
        return value.strip()
    return value 