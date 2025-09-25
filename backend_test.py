#!/usr/bin/env python3
"""
Comprehensive Backend Testing for Rural Water Health Monitoring System
Tests all API endpoints with realistic data scenarios
"""

import requests
import json
from datetime import datetime, timezone, timedelta
import uuid
import sys

# Backend URL from environment
BACKEND_URL = "https://aquahealth-2.preview.emergentagent.com/api"

class BackendTester:
    def __init__(self):
        self.session = requests.Session()
        self.test_results = {
            "passed": 0,
            "failed": 0,
            "errors": []
        }
        
    def log_result(self, test_name, success, message=""):
        if success:
            self.test_results["passed"] += 1
            print(f"✅ {test_name}: PASSED {message}")
        else:
            self.test_results["failed"] += 1
            self.test_results["errors"].append(f"{test_name}: {message}")
            print(f"❌ {test_name}: FAILED - {message}")
    
    def test_api_root(self):
        """Test the root API endpoint"""
        try:
            response = self.session.get(f"{BACKEND_URL}/")
            if response.status_code == 200:
                data = response.json()
                if "Rural Water Health Monitoring System API" in data.get("message", ""):
                    self.log_result("API Root", True, "API is accessible")
                    return True
                else:
                    self.log_result("API Root", False, f"Unexpected message: {data}")
                    return False
            else:
                self.log_result("API Root", False, f"Status code: {response.status_code}")
                return False
        except Exception as e:
            self.log_result("API Root", False, f"Connection error: {str(e)}")
            return False
    
    def test_users_api(self):
        """Test Users CRUD operations"""
        print("\n=== Testing Users API ===")
        
        # Test creating a user
        user_data = {
            "name": "Dr. Rajesh Kumar",
            "email": "rajesh.kumar@healthcenter.gov.in",
            "role": "doctor",
            "location": {
                "lat": 28.6139,
                "lng": 77.2090,
                "address": "Primary Health Center, New Delhi"
            },
            "phone": "+91-9876543210"
        }
        
        try:
            response = self.session.post(f"{BACKEND_URL}/users", json=user_data)
            if response.status_code == 200:
                created_user = response.json()
                if created_user.get("name") == user_data["name"] and "id" in created_user:
                    self.log_result("Create User", True, f"User created with ID: {created_user['id']}")
                    user_id = created_user["id"]
                else:
                    self.log_result("Create User", False, "Invalid user data returned")
                    return False
            else:
                self.log_result("Create User", False, f"Status: {response.status_code}, Response: {response.text}")
                return False
        except Exception as e:
            self.log_result("Create User", False, f"Error: {str(e)}")
            return False
        
        # Test getting all users
        try:
            response = self.session.get(f"{BACKEND_URL}/users")
            if response.status_code == 200:
                users = response.json()
                if isinstance(users, list) and len(users) > 0:
                    self.log_result("Get Users", True, f"Retrieved {len(users)} users")
                else:
                    self.log_result("Get Users", False, "No users returned or invalid format")
            else:
                self.log_result("Get Users", False, f"Status: {response.status_code}")
        except Exception as e:
            self.log_result("Get Users", False, f"Error: {str(e)}")
        
        return True
    
    def test_doctors_api(self):
        """Test Doctor Directory API"""
        print("\n=== Testing Doctors API ===")
        
        # Test creating doctors
        doctors_data = [
            {
                "name": "Dr. Priya Sharma",
                "specialization": "General Medicine",
                "location": {
                    "lat": 28.7041,
                    "lng": 77.1025,
                    "address": "Community Health Center, Rohini, Delhi"
                },
                "phone": "+91-9876543211",
                "email": "priya.sharma@chc.gov.in",
                "availability": "9AM-6PM Mon-Sat",
                "clinic_name": "Rohini Community Health Center"
            },
            {
                "name": "Dr. Amit Patel",
                "specialization": "Pediatrics",
                "location": {
                    "lat": 23.0225,
                    "lng": 72.5714,
                    "address": "District Hospital, Ahmedabad"
                },
                "phone": "+91-9876543212",
                "email": "amit.patel@hospital.gov.in",
                "availability": "24/7",
                "clinic_name": "District Hospital Ahmedabad"
            }
        ]
        
        created_doctors = []
        for doctor_data in doctors_data:
            try:
                response = self.session.post(f"{BACKEND_URL}/doctors", json=doctor_data)
                if response.status_code == 200:
                    created_doctor = response.json()
                    if created_doctor.get("name") == doctor_data["name"] and "id" in created_doctor:
                        created_doctors.append(created_doctor)
                        self.log_result(f"Create Doctor ({doctor_data['name']})", True, f"Doctor created with ID: {created_doctor['id']}")
                    else:
                        self.log_result(f"Create Doctor ({doctor_data['name']})", False, "Invalid doctor data returned")
                else:
                    self.log_result(f"Create Doctor ({doctor_data['name']})", False, f"Status: {response.status_code}, Response: {response.text}")
            except Exception as e:
                self.log_result(f"Create Doctor ({doctor_data['name']})", False, f"Error: {str(e)}")
        
        # Test getting all doctors
        try:
            response = self.session.get(f"{BACKEND_URL}/doctors")
            if response.status_code == 200:
                doctors = response.json()
                if isinstance(doctors, list) and len(doctors) >= len(created_doctors):
                    self.log_result("Get Doctors", True, f"Retrieved {len(doctors)} doctors")
                else:
                    self.log_result("Get Doctors", False, f"Expected at least {len(created_doctors)} doctors, got {len(doctors) if isinstance(doctors, list) else 'invalid format'}")
            else:
                self.log_result("Get Doctors", False, f"Status: {response.status_code}")
        except Exception as e:
            self.log_result("Get Doctors", False, f"Error: {str(e)}")
        
        return len(created_doctors) > 0
    
    def test_water_quality_api(self):
        """Test Water Quality Monitoring API"""
        print("\n=== Testing Water Quality API ===")
        
        # Test creating water quality data with different scenarios
        water_quality_data = [
            {
                "location": {
                    "lat": 28.6139,
                    "lng": 77.2090,
                    "address": "Yamuna River, Delhi"
                },
                "tds_value": 350.5,
                "ph_level": 7.2,
                "turbidity": 1.5,
                "chlorine_level": 0.5,
                "tested_by": "Water Quality Inspector - Delhi"
            },
            {
                "location": {
                    "lat": 23.0225,
                    "lng": 72.5714,
                    "address": "Sabarmati River, Ahmedabad"
                },
                "tds_value": 1200.0,  # High TDS - should be unsafe
                "ph_level": 8.8,      # High pH - should be unsafe
                "turbidity": 6.0,     # High turbidity - should be unsafe
                "chlorine_level": 0.1, # Low chlorine - should be unsafe
                "tested_by": "Water Quality Inspector - Gujarat"
            },
            {
                "location": {
                    "lat": 19.0760,
                    "lng": 72.8777,
                    "address": "Borewell, Mumbai Suburb"
                },
                "tds_value": 600.0,   # Moderate TDS
                "ph_level": 7.0,
                "turbidity": 3.0,     # Moderate turbidity
                "chlorine_level": 0.3,
                "tested_by": "Water Quality Inspector - Maharashtra"
            }
        ]
        
        created_water_data = []
        for data in water_quality_data:
            try:
                response = self.session.post(f"{BACKEND_URL}/water-quality", json=data)
                if response.status_code == 200:
                    created_data = response.json()
                    if "id" in created_data and "status" in created_data:
                        created_water_data.append(created_data)
                        expected_status = self.calculate_expected_water_status(data)
                        actual_status = created_data["status"]
                        if actual_status == expected_status:
                            self.log_result(f"Create Water Quality Data ({data['location']['address']})", True, 
                                          f"Status correctly calculated as '{actual_status}'")
                        else:
                            self.log_result(f"Create Water Quality Data ({data['location']['address']})", False, 
                                          f"Status calculation error: expected '{expected_status}', got '{actual_status}'")
                    else:
                        self.log_result(f"Create Water Quality Data ({data['location']['address']})", False, "Missing required fields in response")
                else:
                    self.log_result(f"Create Water Quality Data ({data['location']['address']})", False, 
                                  f"Status: {response.status_code}, Response: {response.text}")
            except Exception as e:
                self.log_result(f"Create Water Quality Data ({data['location']['address']})", False, f"Error: {str(e)}")
        
        # Test getting all water quality data
        try:
            response = self.session.get(f"{BACKEND_URL}/water-quality")
            if response.status_code == 200:
                water_data = response.json()
                if isinstance(water_data, list) and len(water_data) >= len(created_water_data):
                    self.log_result("Get Water Quality Data", True, f"Retrieved {len(water_data)} water quality records")
                else:
                    self.log_result("Get Water Quality Data", False, f"Expected at least {len(created_water_data)} records")
            else:
                self.log_result("Get Water Quality Data", False, f"Status: {response.status_code}")
        except Exception as e:
            self.log_result("Get Water Quality Data", False, f"Error: {str(e)}")
        
        return len(created_water_data) > 0
    
    def calculate_expected_water_status(self, data):
        """Calculate expected water quality status based on parameters"""
        tds = data["tds_value"]
        ph = data["ph_level"]
        turbidity = data["turbidity"]
        chlorine = data["chlorine_level"]
        
        if tds > 1000 or ph < 6.5 or ph > 8.5 or turbidity > 5 or chlorine < 0.2:
            return "unsafe"
        elif tds > 500 or turbidity > 2:
            return "moderate"
        else:
            return "safe"
    
    def test_medical_stock_api(self):
        """Test Medical Stock Management API"""
        print("\n=== Testing Medical Stock API ===")
        
        # Test creating medical stock with different quantities to test status calculation
        stock_data = [
            {
                "item_name": "Paracetamol Tablets",
                "quantity": 150,  # Should be adequate
                "unit": "tablets",
                "location": {
                    "lat": 28.6139,
                    "lng": 77.2090,
                    "address": "Primary Health Center, Delhi"
                },
                "expiry_date": "2025-12-31T00:00:00Z"
            },
            {
                "item_name": "Oral Rehydration Solution",
                "quantity": 25,   # Should be low
                "unit": "packets",
                "location": {
                    "lat": 23.0225,
                    "lng": 72.5714,
                    "address": "Community Health Center, Ahmedabad"
                }
            },
            {
                "item_name": "Antibiotics",
                "quantity": 5,    # Should be critical
                "unit": "vials",
                "location": {
                    "lat": 19.0760,
                    "lng": 72.8777,
                    "address": "District Hospital, Mumbai"
                },
                "expiry_date": "2024-06-30T00:00:00Z"
            },
            {
                "item_name": "Insulin",
                "quantity": 0,    # Should be out_of_stock
                "unit": "vials",
                "location": {
                    "lat": 12.9716,
                    "lng": 77.5946,
                    "address": "Government Hospital, Bangalore"
                }
            }
        ]
        
        created_stock_items = []
        for stock in stock_data:
            try:
                response = self.session.post(f"{BACKEND_URL}/medical-stock", json=stock)
                if response.status_code == 200:
                    created_stock = response.json()
                    if "id" in created_stock and "status" in created_stock:
                        created_stock_items.append(created_stock)
                        expected_status = self.calculate_expected_stock_status(stock["quantity"])
                        actual_status = created_stock["status"]
                        if actual_status == expected_status:
                            self.log_result(f"Create Medical Stock ({stock['item_name']})", True, 
                                          f"Status correctly calculated as '{actual_status}' for quantity {stock['quantity']}")
                        else:
                            self.log_result(f"Create Medical Stock ({stock['item_name']})", False, 
                                          f"Status calculation error: expected '{expected_status}', got '{actual_status}'")
                    else:
                        self.log_result(f"Create Medical Stock ({stock['item_name']})", False, "Missing required fields in response")
                else:
                    self.log_result(f"Create Medical Stock ({stock['item_name']})", False, 
                                  f"Status: {response.status_code}, Response: {response.text}")
            except Exception as e:
                self.log_result(f"Create Medical Stock ({stock['item_name']})", False, f"Error: {str(e)}")
        
        # Test getting all medical stock
        try:
            response = self.session.get(f"{BACKEND_URL}/medical-stock")
            if response.status_code == 200:
                stock_data = response.json()
                if isinstance(stock_data, list) and len(stock_data) >= len(created_stock_items):
                    self.log_result("Get Medical Stock", True, f"Retrieved {len(stock_data)} stock items")
                    
                    # Count critical stocks for dashboard validation
                    critical_count = sum(1 for item in stock_data if item.get("status") == "critical")
                    print(f"   📊 Critical stock items found: {critical_count}")
                else:
                    self.log_result("Get Medical Stock", False, f"Expected at least {len(created_stock_items)} stock items")
            else:
                self.log_result("Get Medical Stock", False, f"Status: {response.status_code}")
        except Exception as e:
            self.log_result("Get Medical Stock", False, f"Error: {str(e)}")
        
        return len(created_stock_items) > 0
    
    def calculate_expected_stock_status(self, quantity):
        """Calculate expected stock status based on quantity"""
        if quantity == 0:
            return "out_of_stock"
        elif quantity < 10:
            return "critical"
        elif quantity < 50:
            return "low"
        else:
            return "adequate"
    
    def test_health_reports_api(self):
        """Test Health Reports CRUD API"""
        print("\n=== Testing Health Reports API ===")
        
        # Test creating health reports with different types and severities
        reports_data = [
            {
                "reporter_name": "Sunita Devi",
                "report_type": "disease",
                "symptoms": "Fever, headache, body ache for 3 days. Suspected dengue outbreak in the area.",
                "severity": "high",
                "location": {
                    "lat": 28.6139,
                    "lng": 77.2090,
                    "address": "Slum Area, East Delhi"
                },
                "is_anonymous": False,
                "additional_info": "Multiple cases reported in the same locality"
            },
            {
                "reporter_name": "Anonymous Citizen",
                "report_type": "water_quality",
                "symptoms": "Water tastes bitter and has strange smell. Children getting stomach problems.",
                "severity": "critical",
                "location": {
                    "lat": 23.0225,
                    "lng": 72.5714,
                    "address": "Village Kheda, Gujarat"
                },
                "is_anonymous": True,
                "additional_info": "Entire village affected, urgent testing needed"
            },
            {
                "reporter_name": "Ramesh Kumar",
                "report_type": "complaint",
                "symptoms": "No doctor available at health center for past 2 weeks. Patients being turned away.",
                "severity": "medium",
                "location": {
                    "lat": 19.0760,
                    "lng": 72.8777,
                    "address": "Primary Health Center, Thane"
                },
                "is_anonymous": False,
                "additional_info": "Staff shortage causing service disruption"
            }
        ]
        
        created_reports = []
        for report_data in reports_data:
            try:
                response = self.session.post(f"{BACKEND_URL}/reports", json=report_data)
                if response.status_code == 200:
                    created_report = response.json()
                    if "id" in created_report and created_report.get("report_type") == report_data["report_type"]:
                        created_reports.append(created_report)
                        self.log_result(f"Create Health Report ({report_data['report_type']} - {report_data['severity']})", True, 
                                      f"Report created with ID: {created_report['id']}")
                    else:
                        self.log_result(f"Create Health Report ({report_data['report_type']})", False, "Invalid report data returned")
                else:
                    self.log_result(f"Create Health Report ({report_data['report_type']})", False, 
                                  f"Status: {response.status_code}, Response: {response.text}")
            except Exception as e:
                self.log_result(f"Create Health Report ({report_data['report_type']})", False, f"Error: {str(e)}")
        
        # Test getting all health reports
        try:
            response = self.session.get(f"{BACKEND_URL}/reports")
            if response.status_code == 200:
                reports = response.json()
                if isinstance(reports, list) and len(reports) >= len(created_reports):
                    self.log_result("Get Health Reports", True, f"Retrieved {len(reports)} reports")
                    
                    # Count high/critical severity reports for dashboard validation
                    high_severity_count = sum(1 for report in reports if report.get("severity") in ["high", "critical"])
                    active_count = sum(1 for report in reports if report.get("status") == "active")
                    print(f"   📊 High/Critical severity reports: {high_severity_count}")
                    print(f"   📊 Active reports: {active_count}")
                else:
                    self.log_result("Get Health Reports", False, f"Expected at least {len(created_reports)} reports")
            else:
                self.log_result("Get Health Reports", False, f"Status: {response.status_code}")
        except Exception as e:
            self.log_result("Get Health Reports", False, f"Error: {str(e)}")
        
        # Test getting individual report
        if created_reports:
            try:
                report_id = created_reports[0]["id"]
                response = self.session.get(f"{BACKEND_URL}/reports/{report_id}")
                if response.status_code == 200:
                    report = response.json()
                    if report.get("id") == report_id:
                        self.log_result("Get Individual Health Report", True, f"Retrieved report {report_id}")
                    else:
                        self.log_result("Get Individual Health Report", False, "Report ID mismatch")
                else:
                    self.log_result("Get Individual Health Report", False, f"Status: {response.status_code}")
            except Exception as e:
                self.log_result("Get Individual Health Report", False, f"Error: {str(e)}")
        
        return len(created_reports) > 0
    
    def test_dashboard_stats_api(self):
        """Test Dashboard Statistics API"""
        print("\n=== Testing Dashboard Statistics API ===")
        
        try:
            response = self.session.get(f"{BACKEND_URL}/dashboard/stats")
            if response.status_code == 200:
                stats = response.json()
                required_fields = ["total_reports", "active_cases", "alerts", "water_quality_average", "doctors_available", "critical_stocks"]
                
                missing_fields = [field for field in required_fields if field not in stats]
                if not missing_fields:
                    self.log_result("Dashboard Stats Structure", True, "All required fields present")
                    
                    # Validate data types
                    valid_types = True
                    for field in ["total_reports", "active_cases", "alerts", "doctors_available", "critical_stocks"]:
                        if not isinstance(stats[field], int):
                            valid_types = False
                            self.log_result(f"Dashboard Stats Type Check ({field})", False, f"Expected int, got {type(stats[field])}")
                    
                    if not isinstance(stats["water_quality_average"], (int, float)):
                        valid_types = False
                        self.log_result("Dashboard Stats Type Check (water_quality_average)", False, f"Expected number, got {type(stats['water_quality_average'])}")
                    
                    if valid_types:
                        self.log_result("Dashboard Stats Data Types", True, "All fields have correct data types")
                    
                    # Print stats for verification
                    print(f"   📊 Dashboard Statistics:")
                    print(f"      Total Reports: {stats['total_reports']}")
                    print(f"      Active Cases: {stats['active_cases']}")
                    print(f"      Alerts: {stats['alerts']}")
                    print(f"      Water Quality Average: {stats['water_quality_average']}")
                    print(f"      Doctors Available: {stats['doctors_available']}")
                    print(f"      Critical Stocks: {stats['critical_stocks']}")
                    
                    # Validate that stats make sense (non-negative values)
                    if all(stats[field] >= 0 for field in required_fields):
                        self.log_result("Dashboard Stats Values", True, "All values are non-negative")
                    else:
                        self.log_result("Dashboard Stats Values", False, "Some values are negative")
                        
                else:
                    self.log_result("Dashboard Stats Structure", False, f"Missing fields: {missing_fields}")
            else:
                self.log_result("Dashboard Stats", False, f"Status: {response.status_code}, Response: {response.text}")
        except Exception as e:
            self.log_result("Dashboard Stats", False, f"Error: {str(e)}")
    
    def run_all_tests(self):
        """Run all backend tests in sequence"""
        print("🚀 Starting Comprehensive Backend Testing for Rural Water Health Monitoring System")
        print(f"🔗 Testing Backend URL: {BACKEND_URL}")
        print("=" * 80)
        
        # Test API connectivity first
        if not self.test_api_root():
            print("\n❌ API is not accessible. Stopping tests.")
            return False
        
        # Run all API tests
        self.test_users_api()
        self.test_doctors_api()
        self.test_water_quality_api()
        self.test_medical_stock_api()
        self.test_health_reports_api()
        self.test_dashboard_stats_api()
        
        # Print final results
        print("\n" + "=" * 80)
        print("🏁 BACKEND TESTING COMPLETE")
        print("=" * 80)
        print(f"✅ Tests Passed: {self.test_results['passed']}")
        print(f"❌ Tests Failed: {self.test_results['failed']}")
        
        if self.test_results['errors']:
            print("\n🔍 FAILED TESTS DETAILS:")
            for error in self.test_results['errors']:
                print(f"   • {error}")
        
        success_rate = (self.test_results['passed'] / (self.test_results['passed'] + self.test_results['failed'])) * 100
        print(f"\n📊 Success Rate: {success_rate:.1f}%")
        
        if success_rate >= 90:
            print("🎉 EXCELLENT: Backend is working very well!")
        elif success_rate >= 75:
            print("✅ GOOD: Backend is mostly working with minor issues")
        elif success_rate >= 50:
            print("⚠️  MODERATE: Backend has some significant issues")
        else:
            print("🚨 CRITICAL: Backend has major issues that need immediate attention")
        
        return success_rate >= 75

if __name__ == "__main__":
    tester = BackendTester()
    success = tester.run_all_tests()
    sys.exit(0 if success else 1)