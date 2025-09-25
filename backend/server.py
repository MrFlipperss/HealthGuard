from fastapi import FastAPI, APIRouter, HTTPException
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path
from pydantic import BaseModel, Field
from typing import List, Optional
import uuid
from datetime import datetime, timezone, timedelta
from enum import Enum

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# Create the main app without a prefix
app = FastAPI()

# Create a router with the /api prefix
api_router = APIRouter(prefix="/api")

# Enums
class UserRole(str, Enum):
    CITIZEN = "citizen"
    DOCTOR = "doctor"
    CLINIC_STAFF = "clinic_staff"
    GOVERNMENT = "government"

class ReportType(str, Enum):
    DISEASE = "disease"
    WATER_QUALITY = "water_quality"
    COMPLAINT = "complaint"

class SeverityLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class StockStatus(str, Enum):
    ADEQUATE = "adequate"
    LOW = "low"
    CRITICAL = "critical"
    OUT_OF_STOCK = "out_of_stock"

# Pydantic Models
class User(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    email: str
    role: UserRole
    location: dict  # {"lat": float, "lng": float, "address": str}
    phone: Optional[str] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class UserCreate(BaseModel):
    name: str
    email: str
    role: UserRole
    location: dict
    phone: Optional[str] = None

class HealthReport(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    reporter_id: str
    reporter_name: str
    report_type: ReportType
    symptoms: str
    severity: SeverityLevel
    location: dict  # {"lat": float, "lng": float, "address": str}
    date_reported: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    status: str = Field(default="active")  # active, resolved, under_investigation
    is_anonymous: bool = Field(default=False)
    additional_info: Optional[str] = None

class HealthReportCreate(BaseModel):
    reporter_name: str
    report_type: ReportType
    symptoms: str
    severity: SeverityLevel
    location: dict
    is_anonymous: bool = Field(default=False)
    additional_info: Optional[str] = None

class WaterQualityData(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    location: dict
    tds_value: float
    ph_level: float
    turbidity: float
    chlorine_level: float
    status: str  # safe, moderate, unsafe
    tested_by: str
    test_date: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class WaterQualityDataCreate(BaseModel):
    location: dict
    tds_value: float
    ph_level: float
    turbidity: float
    chlorine_level: float
    tested_by: str

class Doctor(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    specialization: str
    location: dict
    phone: str
    email: str
    availability: str  # "24/7", "9AM-6PM", etc.
    clinic_name: Optional[str] = None

class DoctorCreate(BaseModel):
    name: str
    specialization: str
    location: dict
    phone: str
    email: str
    availability: str
    clinic_name: Optional[str] = None

class MedicalStock(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    item_name: str
    quantity: int
    unit: str
    status: StockStatus
    location: dict
    expiry_date: Optional[datetime] = None
    last_updated: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class MedicalStockCreate(BaseModel):
    item_name: str
    quantity: int
    unit: str
    location: dict
    expiry_date: Optional[datetime] = None

class DashboardStats(BaseModel):
    total_reports: int
    active_cases: int
    alerts: int
    water_quality_average: float
    doctors_available: int
    critical_stocks: int

# Helper functions
def prepare_for_mongo(data):
    if isinstance(data, dict):
        for key, value in data.items():
            if isinstance(value, datetime):
                data[key] = value.isoformat()
    return data

def calculate_water_status(tds: float, ph: float, turbidity: float, chlorine: float) -> str:
    """Calculate water quality status based on parameters"""
    if tds > 1000 or ph < 6.5 or ph > 8.5 or turbidity > 5 or chlorine < 0.2:
        return "unsafe"
    elif tds > 500 or turbidity > 2:
        return "moderate"
    else:
        return "safe"

def calculate_stock_status(quantity: int, item_name: str) -> StockStatus:
    """Calculate stock status based on quantity and item type"""
    if quantity == 0:
        return StockStatus.OUT_OF_STOCK
    elif quantity < 10:
        return StockStatus.CRITICAL
    elif quantity < 50:
        return StockStatus.LOW
    else:
        return StockStatus.ADEQUATE

# Routes
@api_router.get("/")
async def root():
    return {"message": "Rural Water Health Monitoring System API"}

# Dashboard Statistics
@api_router.get("/dashboard/stats", response_model=DashboardStats)
async def get_dashboard_stats():
    try:
        # Get counts from database
        total_reports = await db.health_reports.count_documents({})
        active_cases = await db.health_reports.count_documents({"status": "active"})
        
        # Count alerts (high severity reports in last 7 days)
        seven_days_ago = datetime.now(timezone.utc) - timedelta(days=7)
        alerts = await db.health_reports.count_documents({
            "severity": {"$in": ["high", "critical"]},
            "date_reported": {"$gte": seven_days_ago.isoformat()}
        })
        
        # Get average water quality
        water_data = await db.water_quality.find().to_list(1000)
        avg_tds = sum(w.get("tds_value", 0) for w in water_data) / len(water_data) if water_data else 0
        
        doctors_available = await db.doctors.count_documents({})
        critical_stocks = await db.medical_stock.count_documents({"status": "critical"})
        
        return DashboardStats(
            total_reports=total_reports,
            active_cases=active_cases,
            alerts=alerts,
            water_quality_average=round(avg_tds, 2),
            doctors_available=doctors_available,
            critical_stocks=critical_stocks
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching stats: {str(e)}")

# Health Reports
@api_router.post("/reports", response_model=HealthReport)
async def create_health_report(report: HealthReportCreate):
    try:
        report_dict = report.dict()
        # Add reporter_id (generate UUID for anonymous or use reporter name as ID)
        report_dict["reporter_id"] = str(uuid.uuid4()) if report.is_anonymous else report.reporter_name
        report_obj = HealthReport(**report_dict)
        report_data = prepare_for_mongo(report_obj.dict())
        await db.health_reports.insert_one(report_data)
        return report_obj
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating report: {str(e)}")

@api_router.get("/reports", response_model=List[HealthReport])
async def get_health_reports(limit: int = 50):
    try:
        reports = await db.health_reports.find().sort("date_reported", -1).limit(limit).to_list(limit)
        return [HealthReport(**report) for report in reports]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching reports: {str(e)}")

@api_router.get("/reports/{report_id}", response_model=HealthReport)
async def get_health_report(report_id: str):
    try:
        report = await db.health_reports.find_one({"id": report_id})
        if not report:
            raise HTTPException(status_code=404, detail="Report not found")
        return HealthReport(**report)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching report: {str(e)}")

# Water Quality
@api_router.post("/water-quality", response_model=WaterQualityData)
async def create_water_quality_data(data: WaterQualityDataCreate):
    try:
        data_dict = data.dict()
        status = calculate_water_status(data.tds_value, data.ph_level, data.turbidity, data.chlorine_level)
        data_dict["status"] = status
        
        quality_obj = WaterQualityData(**data_dict)
        quality_data = prepare_for_mongo(quality_obj.dict())
        await db.water_quality.insert_one(quality_data)
        return quality_obj
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating water quality data: {str(e)}")

@api_router.get("/water-quality", response_model=List[WaterQualityData])
async def get_water_quality_data(limit: int = 50):
    try:
        data = await db.water_quality.find().sort("test_date", -1).limit(limit).to_list(limit)
        return [WaterQualityData(**item) for item in data]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching water quality data: {str(e)}")

# Doctors
@api_router.post("/doctors", response_model=Doctor)
async def create_doctor(doctor: DoctorCreate):
    try:
        doctor_dict = doctor.dict()
        doctor_obj = Doctor(**doctor_dict)
        await db.doctors.insert_one(doctor_obj.dict())
        return doctor_obj
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating doctor: {str(e)}")

@api_router.get("/doctors", response_model=List[Doctor])
async def get_doctors():
    try:
        doctors = await db.doctors.find().to_list(1000)
        return [Doctor(**doctor) for doctor in doctors]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching doctors: {str(e)}")

# Medical Stock
@api_router.post("/medical-stock", response_model=MedicalStock)
async def create_medical_stock(stock: MedicalStockCreate):
    try:
        stock_dict = stock.dict()
        status = calculate_stock_status(stock.quantity, stock.item_name)
        stock_dict["status"] = status
        
        stock_obj = MedicalStock(**stock_dict)
        stock_data = prepare_for_mongo(stock_obj.dict())
        await db.medical_stock.insert_one(stock_data)
        return stock_obj
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating medical stock: {str(e)}")

@api_router.get("/medical-stock", response_model=List[MedicalStock])
async def get_medical_stock():
    try:
        stock = await db.medical_stock.find().sort("last_updated", -1).to_list(1000)
        return [MedicalStock(**item) for item in stock]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching medical stock: {str(e)}")

# Users
@api_router.post("/users", response_model=User)
async def create_user(user: UserCreate):
    try:
        user_dict = user.dict()
        user_obj = User(**user_dict)
        await db.users.insert_one(user_obj.dict())
        return user_obj
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating user: {str(e)}")

@api_router.get("/users", response_model=List[User])
async def get_users():
    try:
        users = await db.users.find().to_list(1000)
        return [User(**user) for user in users]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching users: {str(e)}")

# Include the router in the main app
app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=os.environ.get('CORS_ORIGINS', '*').split(','),
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()