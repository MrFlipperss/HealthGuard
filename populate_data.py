#!/usr/bin/env python3
"""
Reference Data Population Script for Rural Health Monitor
Adds realistic sample data to all categories
"""

import requests
import json
from datetime import datetime, timedelta
import random
import uuid

# Backend API URL
API_BASE = "http://localhost:8001/api"

class DataPopulator:
    def __init__(self):
        self.session = requests.Session()
        
    def populate_health_reports(self):
        """Add sample health reports"""
        print("📋 Adding sample health reports...")
        
        health_reports = [
            {
                "reporter_name": "Priya Sharma",
                "report_type": "disease",
                "symptoms": "High fever (101°F), severe headache, body ache, and fatigue. Multiple family members affected.",
                "severity": "high",
                "location": {
                    "lat": 28.7041,
                    "lng": 77.1025,
                    "address": "Village Rampur, Block Kharkhoda, Sonipat District"
                },
                "is_anonymous": False,
                "additional_info": "5 cases reported in the same village within 2 days. Possible outbreak."
            },
            {
                "reporter_name": "Dr. Rajesh Kumar",
                "report_type": "disease",
                "symptoms": "Diarrhea, vomiting, dehydration in children under 5 years. 8 cases in last 48 hours.",
                "severity": "critical",
                "location": {
                    "lat": 28.6139,
                    "lng": 77.2090,
                    "address": "Anganwadi Center, Village Sisana, Gurugram District"
                },
                "is_anonymous": False,
                "additional_info": "Suspected water contamination. Immediate medical intervention required."
            },
            {
                "reporter_name": "Anonymous Citizen",
                "report_type": "water_quality",
                "symptoms": "Strange taste and smell in village water supply. Yellow coloration observed.",
                "severity": "medium",
                "location": {
                    "lat": 28.5355,
                    "lng": 77.3910,
                    "address": "Village Palwal, Faridabad District"
                },
                "is_anonymous": True,
                "additional_info": "Water from community hand pump. Used by 200+ families daily."
            },
            {
                "reporter_name": "Sunita Devi",
                "report_type": "complaint",
                "symptoms": "No doctor available at PHC for last 3 days. Patients traveling 25km for basic treatment.",
                "severity": "high",
                "location": {
                    "lat": 28.4595,
                    "lng": 77.0266,
                    "address": "Primary Health Center, Village Nuh, Mewat District"
                },
                "is_anonymous": False,
                "additional_info": "Pregnant women and elderly patients particularly affected. Emergency services needed."
            },
            {
                "reporter_name": "Mohan Singh",
                "report_type": "disease",
                "symptoms": "Skin rashes, itching, and respiratory issues. Multiple villagers affected.",
                "severity": "medium",
                "location": {
                    "lat": 28.8386,
                    "lng": 77.1192,
                    "address": "Village Bahadurgarh, Jhajjar District"
                },
                "is_anonymous": False,
                "additional_info": "Possible allergic reaction to crop pesticides. 15+ people affected."
            },
            {
                "reporter_name": "Asha Worker",
                "report_type": "complaint",
                "symptoms": "Shortage of essential medicines. No ORS, paracetamol, or antibiotics available.",
                "severity": "high",
                "location": {
                    "lat": 28.9931,
                    "lng": 77.7085,
                    "address": "Sub Health Center, Village Panipat Rural"
                },
                "is_anonymous": False,
                "additional_info": "Stock out for 2 weeks. Local pharmacy 15km away."
            },
            {
                "reporter_name": "Village Sarpanch",
                "report_type": "water_quality",
                "symptoms": "High TDS levels detected in bore well water. Community concerned about long-term health effects.",
                "severity": "medium",
                "location": {
                    "lat": 28.6692,
                    "lng": 77.4538,
                    "address": "Village Ballabgarh, Faridabad District"
                },
                "is_anonymous": False,
                "additional_info": "Recent water quality test showed TDS >1000 ppm. 500+ people affected."
            },
            {
                "reporter_name": "Anonymous Health Worker",
                "report_type": "disease",
                "symptoms": "Suspected malaria cases increasing. Fever, chills, sweating pattern observed.",
                "severity": "high",
                "location": {
                    "lat": 28.7833,
                    "lng": 76.9167,
                    "address": "Village Rohtak Rural Area"
                },
                "is_anonymous": True,
                "additional_info": "Monsoon-related cases. Need mosquito control measures."
            }
        ]
        
        for report in health_reports:
            try:
                response = self.session.post(f"{API_BASE}/reports", json=report)
                if response.status_code == 200:
                    print(f"  ✅ Added report from {report['reporter_name']} - {report['report_type']}")
                else:
                    print(f"  ❌ Failed to add report: {response.status_code}")
            except Exception as e:
                print(f"  ❌ Error adding report: {e}")
    
    def populate_water_quality_data(self):
        """Add sample water quality data"""
        print("💧 Adding sample water quality data...")
        
        water_quality_data = [
            {
                "location": {
                    "lat": 28.7041,
                    "lng": 77.1025,
                    "address": "Village Rampur Hand Pump #1"
                },
                "tds_value": 350.5,
                "ph_level": 7.2,
                "turbidity": 1.5,
                "chlorine_level": 0.8,
                "tested_by": "Health Department Team A",
                "status": "safe"
            },
            {
                "location": {
                    "lat": 28.6139,
                    "lng": 77.2090,
                    "address": "Village Sisana Bore Well"
                },
                "tds_value": 1200.0,
                "ph_level": 8.8,
                "turbidity": 5.2,
                "chlorine_level": 0.1,
                "tested_by": "Mobile Testing Unit",
                "status": "unsafe"
            },
            {
                "location": {
                    "lat": 28.5355,
                    "lng": 77.3910,
                    "address": "Village Palwal Community Well"
                },
                "tds_value": 600.0,
                "ph_level": 6.8,
                "turbidity": 3.0,
                "chlorine_level": 0.4,
                "tested_by": "District Water Officer",
                "status": "moderate"
            },
            {
                "location": {
                    "lat": 28.4595,
                    "lng": 77.0266,
                    "address": "Nuh PHC Water Source"
                },
                "tds_value": 280.0,
                "ph_level": 7.5,
                "turbidity": 0.8,
                "chlorine_level": 1.2,
                "tested_by": "Health Inspector",
                "status": "safe"
            },
            {
                "location": {
                    "lat": 28.8386,
                    "lng": 77.1192,
                    "address": "Bahadurgarh School Water Tank"
                },
                "tds_value": 850.0,
                "ph_level": 8.2,
                "turbidity": 4.1,
                "chlorine_level": 0.2,
                "tested_by": "Education Dept. Inspector",
                "status": "moderate"
            },
            {
                "location": {
                    "lat": 28.9931,
                    "lng": 77.7085,
                    "address": "Panipat Rural Tube Well #3"
                },
                "tds_value": 1500.0,
                "ph_level": 9.1,
                "turbidity": 8.5,
                "chlorine_level": 0.0,
                "tested_by": "Environmental Lab",
                "status": "unsafe"
            },
            {
                "location": {
                    "lat": 28.6692,
                    "lng": 77.4538,
                    "address": "Ballabgarh Community Center"
                },
                "tds_value": 420.0,
                "ph_level": 7.0,
                "turbidity": 2.2,
                "chlorine_level": 0.6,
                "tested_by": "Community Health Worker",
                "status": "safe"
            },
            {
                "location": {
                    "lat": 28.7833,
                    "lng": 76.9167,
                    "address": "Rohtak Rural Hand Pump Network"
                },
                "tds_value": 750.0,
                "ph_level": 7.8,
                "turbidity": 3.8,
                "chlorine_level": 0.3,
                "tested_by": "Block Health Officer",
                "status": "moderate"
            },
            {
                "location": {
                    "lat": 28.5678,
                    "lng": 77.1234,
                    "address": "Village Sohna Water Treatment Plant"
                },
                "tds_value": 190.0,
                "ph_level": 7.3,
                "turbidity": 0.5,
                "chlorine_level": 1.5,
                "tested_by": "Water Treatment Authority",
                "status": "safe"
            },
            {
                "location": {
                    "lat": 28.8765,
                    "lng": 77.5432,
                    "address": "Village Karnal Outskirts"
                },
                "tds_value": 950.0,
                "ph_level": 8.5,
                "turbidity": 6.2,
                "chlorine_level": 0.15,
                "tested_by": "Regional Health Team",
                "status": "moderate"
            }
        ]
        
        for water_data in water_quality_data:
            try:
                response = self.session.post(f"{API_BASE}/water-quality", json=water_data)
                if response.status_code == 200:
                    print(f"  ✅ Added water quality data for {water_data['location']['address']} - {water_data['status']}")
                else:
                    print(f"  ❌ Failed to add water data: {response.status_code}")
            except Exception as e:
                print(f"  ❌ Error adding water data: {e}")
    
    def populate_doctor_directory(self):
        """Add sample doctor directory"""
        print("👨‍⚕️ Adding sample doctor directory...")
        
        doctors = [
            {
                "name": "Dr. Rajesh Kumar Sharma",
                "specialization": "General Medicine",
                "clinic_name": "Rural Health Center Rampur",
                "location": {
                    "lat": 28.7041,
                    "lng": 77.1025,
                    "address": "Village Rampur, Sonipat District"
                },
                "phone": "+91-9876543210",
                "email": "dr.rajesh@rhc-rampur.gov.in",
                "availability": "Mon-Fri: 9AM-5PM, Sat: 9AM-1PM",
                "experience_years": 12,
                "languages": ["Hindi", "English", "Punjabi"],
                "services": ["General Consultation", "Basic Surgery", "Emergency Care", "Vaccination"]
            },
            {
                "name": "Dr. Priya Gupta",
                "specialization": "Pediatrics",
                "clinic_name": "Child Health Center Sisana",
                "location": {
                    "lat": 28.6139,
                    "lng": 77.2090,
                    "address": "Village Sisana, Gurugram District"
                },
                "phone": "+91-9876543211",
                "email": "dr.priya@chc-sisana.gov.in",
                "availability": "Mon-Sat: 8AM-4PM, Emergency: 24/7",
                "experience_years": 8,
                "languages": ["Hindi", "English"],
                "services": ["Child Health", "Immunization", "Nutrition Counseling", "Growth Monitoring"]
            },
            {
                "name": "Dr. Suresh Singh",
                "specialization": "Gynecology",
                "clinic_name": "Women's Health Center Palwal",
                "location": {
                    "lat": 28.5355,
                    "lng": 77.3910,
                    "address": "Village Palwal, Faridabad District"
                },
                "phone": "+91-9876543212",
                "email": "dr.suresh@whc-palwal.gov.in",
                "availability": "Tue-Sat: 10AM-6PM, Emergency on call",
                "experience_years": 15,
                "languages": ["Hindi", "English", "Haryanvi"],
                "services": ["Prenatal Care", "Delivery", "Family Planning", "Women's Health"]
            },
            {
                "name": "Dr. Amit Patel",
                "specialization": "Orthopedics",
                "clinic_name": "Bone & Joint Clinic Nuh",
                "location": {
                    "lat": 28.4595,
                    "lng": 77.0266,
                    "address": "PHC Nuh, Mewat District"
                },
                "phone": "+91-9876543213",
                "email": "dr.amit@phc-nuh.gov.in",
                "availability": "Mon, Wed, Fri: 11AM-3PM",
                "experience_years": 10,
                "languages": ["Hindi", "English", "Urdu"],
                "services": ["Fracture Treatment", "Joint Pain", "Physiotherapy", "X-Ray"]
            },
            {
                "name": "Dr. Sunita Devi",
                "specialization": "General Medicine",
                "clinic_name": "Community Health Center Bahadurgarh",
                "location": {
                    "lat": 28.8386,
                    "lng": 77.1192,
                    "address": "Village Bahadurgarh, Jhajjar District"
                },
                "phone": "+91-9876543214",
                "email": "dr.sunita@chc-bahadurgarh.gov.in",
                "availability": "Mon-Fri: 9AM-5PM, Sat: 9AM-12PM",
                "experience_years": 18,
                "languages": ["Hindi", "English", "Punjabi"],
                "services": ["General Health", "Diabetes Care", "Hypertension", "Health Check-ups"]
            },
            {
                "name": "Dr. Mohammad Ali",
                "specialization": "Dermatology",
                "clinic_name": "Skin Care Clinic Panipat",
                "location": {
                    "lat": 28.9931,
                    "lng": 77.7085,
                    "address": "Sub Health Center, Panipat Rural"
                },
                "phone": "+91-9876543215",
                "email": "dr.ali@shc-panipat.gov.in",
                "availability": "Tue, Thu, Sat: 2PM-6PM",
                "experience_years": 6,
                "languages": ["Hindi", "English", "Urdu"],
                "services": ["Skin Diseases", "Allergies", "Wound Care", "Cosmetic Issues"]
            },
            {
                "name": "Dr. Kavita Sharma",
                "specialization": "Dentistry",
                "clinic_name": "Dental Care Unit Ballabgarh",
                "location": {
                    "lat": 28.6692,
                    "lng": 77.4538,
                    "address": "Village Ballabgarh, Faridabad District"
                },
                "phone": "+91-9876543216",
                "email": "dr.kavita@dcu-ballabgarh.gov.in",
                "availability": "Mon-Wed-Fri: 10AM-4PM",
                "experience_years": 9,
                "languages": ["Hindi", "English"],
                "services": ["Dental Check-up", "Tooth Extraction", "Filling", "Oral Health Education"]
            },
            {
                "name": "Dr. Ravi Kumar",
                "specialization": "Cardiology",
                "clinic_name": "Heart Care Center Rohtak",
                "location": {
                    "lat": 28.7833,
                    "lng": 76.9167,
                    "address": "District Hospital Rohtak Rural"
                },
                "phone": "+91-9876543217",
                "email": "dr.ravi@hcc-rohtak.gov.in",
                "availability": "Mon, Thu: 11AM-2PM (Visiting)",
                "experience_years": 20,
                "languages": ["Hindi", "English"],
                "services": ["Heart Disease", "ECG", "Blood Pressure", "Cardiac Emergency"]
            }
        ]
        
        for doctor in doctors:
            try:
                response = self.session.post(f"{API_BASE}/doctors", json=doctor)
                if response.status_code == 200:
                    print(f"  ✅ Added Dr. {doctor['name']} - {doctor['specialization']}")
                else:
                    print(f"  ❌ Failed to add doctor: {response.status_code}")
            except Exception as e:
                print(f"  ❌ Error adding doctor: {e}")
    
    def populate_medical_stock(self):
        """Add sample medical stock data"""
        print("💊 Adding sample medical stock data...")
        
        medical_stocks = [
            {
                "item_name": "Paracetamol Tablets (500mg)",
                "category": "Pain Relief",
                "quantity": 150,
                "unit": "tablets",
                "expiry_date": (datetime.now() + timedelta(days=365)).isoformat(),
                "location": {
                    "lat": 28.7041,
                    "lng": 77.1025,
                    "address": "Rural Health Center Rampur"
                },
                "supplier": "Government Medical Store",
                "batch_number": "PC2024-001",
                "cost_per_unit": 0.50,
                "status": "adequate"
            },
            {
                "item_name": "ORS Packets",
                "category": "Rehydration",
                "quantity": 25,
                "unit": "packets",
                "expiry_date": (datetime.now() + timedelta(days=730)).isoformat(),
                "location": {
                    "lat": 28.6139,
                    "lng": 77.2090,
                    "address": "Child Health Center Sisana"
                },
                "supplier": "WHO Supply Chain",
                "batch_number": "ORS2024-045",
                "cost_per_unit": 2.00,
                "status": "low"
            },
            {
                "item_name": "Amoxicillin Capsules (250mg)",
                "category": "Antibiotics",
                "quantity": 5,
                "unit": "capsules",
                "expiry_date": (datetime.now() + timedelta(days=180)).isoformat(),
                "location": {
                    "lat": 28.5355,
                    "lng": 77.3910,
                    "address": "Women's Health Center Palwal"
                },
                "supplier": "Central Medical Supply",
                "batch_number": "AMX2024-078",
                "cost_per_unit": 1.20,
                "status": "critical"
            },
            {
                "item_name": "Insulin Vials (100IU/ml)",
                "category": "Diabetes Care",
                "quantity": 0,
                "unit": "vials",
                "expiry_date": (datetime.now() + timedelta(days=90)).isoformat(),
                "location": {
                    "lat": 28.4595,
                    "lng": 77.0266,
                    "address": "PHC Nuh"
                },
                "supplier": "Diabetes Care Foundation",
                "batch_number": "INS2024-012",
                "cost_per_unit": 25.00,
                "status": "out_of_stock"
            },
            {
                "item_name": "Bandages (Sterile)",
                "category": "First Aid",
                "quantity": 80,
                "unit": "pieces",
                "expiry_date": (datetime.now() + timedelta(days=1095)).isoformat(),
                "location": {
                    "lat": 28.8386,
                    "lng": 77.1192,
                    "address": "Community Health Center Bahadurgarh"
                },
                "supplier": "Medical Supplies Ltd",
                "batch_number": "BND2024-156",
                "cost_per_unit": 3.50,
                "status": "adequate"
            },
            {
                "item_name": "Antiseptic Solution (500ml)",
                "category": "Disinfectant",
                "quantity": 12,
                "unit": "bottles",
                "expiry_date": (datetime.now() + timedelta(days=365)).isoformat(),
                "location": {
                    "lat": 28.9931,
                    "lng": 77.7085,
                    "address": "Sub Health Center Panipat"
                },
                "supplier": "Healthcare Products Inc",
                "batch_number": "ANT2024-089",
                "cost_per_unit": 8.00,
                "status": "low"
            },
            {
                "item_name": "Pregnancy Test Kits",
                "category": "Diagnostic",
                "quantity": 35,
                "unit": "kits",
                "expiry_date": (datetime.now() + timedelta(days=545)).isoformat(),
                "location": {
                    "lat": 28.6692,
                    "lng": 77.4538,
                    "address": "Village Ballabgarh Health Center"
                },
                "supplier": "Diagnostic Solutions",
                "batch_number": "PTK2024-023",
                "cost_per_unit": 15.00,
                "status": "adequate"
            },
            {
                "item_name": "Blood Pressure Monitors",
                "category": "Equipment",
                "quantity": 3,
                "unit": "devices",
                "expiry_date": (datetime.now() + timedelta(days=1825)).isoformat(),
                "location": {
                    "lat": 28.7833,
                    "lng": 76.9167,
                    "address": "Heart Care Center Rohtak"
                },
                "supplier": "Medical Equipment Co",
                "batch_number": "BPM2024-007",
                "cost_per_unit": 150.00,
                "status": "critical"
            },
            {
                "item_name": "Vitamin D Supplements",
                "category": "Nutrition",
                "quantity": 200,
                "unit": "tablets",
                "expiry_date": (datetime.now() + timedelta(days=420)).isoformat(),
                "location": {
                    "lat": 28.5678,
                    "lng": 77.1234,
                    "address": "Village Sohna Health Post"
                },
                "supplier": "Nutrition Council",
                "batch_number": "VTD2024-134",
                "cost_per_unit": 0.75,
                "status": "adequate"
            },
            {
                "item_name": "Thermometers (Digital)",
                "category": "Equipment",
                "quantity": 8,
                "unit": "devices",
                "expiry_date": (datetime.now() + timedelta(days=1095)).isoformat(),
                "location": {
                    "lat": 28.8765,
                    "lng": 77.5432,
                    "address": "Karnal Rural Health Unit"
                },
                "supplier": "Medical Instruments Ltd",
                "batch_number": "THM2024-056",
                "cost_per_unit": 12.50,
                "status": "low"
            }
        ]
        
        for stock in medical_stocks:
            try:
                response = self.session.post(f"{API_BASE}/medical-stock", json=stock)
                if response.status_code == 200:
                    print(f"  ✅ Added {stock['item_name']} - {stock['status']} ({stock['quantity']} {stock['unit']})")
                else:
                    print(f"  ❌ Failed to add stock item: {response.status_code}")
            except Exception as e:
                print(f"  ❌ Error adding stock item: {e}")
    
    def populate_users(self):
        """Add sample users"""
        print("👥 Adding sample users...")
        
        users = [
            {
                "name": "Priya Sharma",
                "email": "priya.sharma@village.gov.in",
                "role": "citizen",
                "location": {
                    "lat": 28.7041,
                    "lng": 77.1025,
                    "address": "Village Rampur, Sonipat District"
                },
                "phone": "+91-9876543220"
            },
            {
                "name": "Dr. Rajesh Kumar",
                "email": "dr.rajesh@rhc-rampur.gov.in",
                "role": "doctor",
                "location": {
                    "lat": 28.7041,
                    "lng": 77.1025,
                    "address": "Rural Health Center Rampur"
                },
                "phone": "+91-9876543210"
            },
            {
                "name": "Sunita Devi (ASHA Worker)",
                "email": "sunita.asha@health.gov.in",
                "role": "clinic_staff",
                "location": {
                    "lat": 28.4595,
                    "lng": 77.0266,
                    "address": "PHC Nuh, Mewat District"
                },
                "phone": "+91-9876543214"
            },
            {
                "name": "Block Health Officer",
                "email": "bho.sonipat@health.gov.in",
                "role": "government",
                "location": {
                    "lat": 28.7000,
                    "lng": 77.1000,
                    "address": "Block Health Office, Sonipat"
                },
                "phone": "+91-9876543230"
            }
        ]
        
        for user in users:
            try:
                response = self.session.post(f"{API_BASE}/users", json=user)
                if response.status_code == 200:
                    print(f"  ✅ Added user {user['name']} - {user['role']}")
                else:
                    print(f"  ❌ Failed to add user: {response.status_code}")
            except Exception as e:
                print(f"  ❌ Error adding user: {e}")
    
    def run_all(self):
        """Run all data population functions"""
        print("🚀 Starting reference data population...")
        print("=" * 60)
        
        self.populate_users()
        print()
        self.populate_health_reports()
        print()
        self.populate_water_quality_data()
        print()
        self.populate_doctor_directory()
        print()
        self.populate_medical_stock()
        print()
        
        print("=" * 60)
        print("✅ Reference data population completed!")
        print("📊 The Rural Health Monitor system now has comprehensive sample data")
        print("🎯 You can now see meaningful charts, maps, and statistics in the enhanced dashboard")

if __name__ == "__main__":
    populator = DataPopulator()
    populator.run_all()