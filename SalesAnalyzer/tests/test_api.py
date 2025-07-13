"""
API测试用例
"""
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_root():
    """测试根路径"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert data["version"] == "1.0.0"

def test_health_check():
    """测试健康检查"""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"

def test_get_sales_records():
    """测试获取销售记录"""
    response = client.get("/api/v1/sales/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_sales_summary():
    """测试获取销售摘要"""
    response = client.get("/api/v1/sales/statistics/summary")
    assert response.status_code == 200
    data = response.json()
    assert "total_sales" in data
    assert "total_orders" in data
    assert "total_quantity" in data
    assert "avg_order_value" in data

def test_get_top_products():
    """测试获取热销产品"""
    response = client.get("/api/v1/analytics/top-products")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_top_regions():
    """测试获取热销区域"""
    response = client.get("/api/v1/analytics/top-regions")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_sales_trend():
    """测试获取销售趋势"""
    response = client.get("/api/v1/analytics/sales-trend")
    assert response.status_code == 200
    assert isinstance(response.json(), list) 