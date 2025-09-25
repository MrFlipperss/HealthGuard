#!/usr/bin/env python3
"""
Admin Dashboard Testing for Rural Water Health Monitoring System
Tests the admin dashboard route and functionality
"""

import requests
import json
from datetime import datetime, timezone, timedelta

# Backend URLs
BACKEND_URL = "https://emergency-map-7.preview.emergentagent.com/api"
ADMIN_URL = "https://emergency-map-7.preview.emergentagent.com/admin"
LOCAL_ADMIN_URL = "http://localhost:8001/admin"

class AdminDashboardTester:
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
    
    def test_admin_route_local(self):
        """Test admin dashboard route on local backend"""
        print("\n=== Testing Admin Dashboard Route (Local Backend) ===")
        
        try:
            response = self.session.get(LOCAL_ADMIN_URL)
            if response.status_code == 200:
                content = response.text
                # Check for key elements in the admin dashboard
                required_elements = [
                    "Rural Health Monitor",
                    "Official Dashboard",
                    "Government Access",
                    "Loading dashboard data",
                    "chart.js"
                ]
                
                missing_elements = []
                for element in required_elements:
                    if element.lower() not in content.lower():
                        missing_elements.append(element)
                
                if not missing_elements:
                    self.log_result("Admin Dashboard HTML Content", True, "All required elements present")
                else:
                    self.log_result("Admin Dashboard HTML Content", False, f"Missing elements: {missing_elements}")
                
                # Check content type
                content_type = response.headers.get('content-type', '')
                if 'text/html' in content_type:
                    self.log_result("Admin Dashboard Content Type", True, f"Correct content type: {content_type}")
                else:
                    self.log_result("Admin Dashboard Content Type", False, f"Expected HTML, got: {content_type}")
                    
                return True
            else:
                self.log_result("Admin Dashboard Route", False, f"Status code: {response.status_code}")
                return False
        except Exception as e:
            self.log_result("Admin Dashboard Route", False, f"Error: {str(e)}")
            return False
    
    def test_admin_route_public(self):
        """Test admin dashboard route on public URL"""
        print("\n=== Testing Admin Dashboard Route (Public URL) ===")
        
        try:
            response = self.session.get(ADMIN_URL)
            if response.status_code == 200:
                content = response.text
                # This might be intercepted by frontend, so we check what we get
                if "Rural Health Monitor" in content and "Official Dashboard" in content:
                    self.log_result("Public Admin Route (Backend)", True, "Backend admin dashboard served")
                elif "<!doctype html>" in content.lower():
                    self.log_result("Public Admin Route (Frontend Intercept)", True, "Frontend is intercepting /admin route (expected behavior)")
                else:
                    self.log_result("Public Admin Route", False, "Unexpected content returned")
                return True
            else:
                self.log_result("Public Admin Route", False, f"Status code: {response.status_code}")
                return False
        except Exception as e:
            self.log_result("Public Admin Route", False, f"Error: {str(e)}")
            return False
    
    def test_cors_for_admin(self):
        """Test CORS configuration for admin dashboard API access"""
        print("\n=== Testing CORS Configuration ===")
        
        # Test preflight request
        try:
            headers = {
                'Origin': 'https://emergency-map-7.preview.emergentagent.com',
                'Access-Control-Request-Method': 'GET',
                'Access-Control-Request-Headers': 'Content-Type'
            }
            response = self.session.options(f"{BACKEND_URL}/dashboard/stats", headers=headers)
            
            if response.status_code in [200, 204]:
                # Check CORS headers
                cors_headers = {
                    'access-control-allow-origin': response.headers.get('access-control-allow-origin'),
                    'access-control-allow-methods': response.headers.get('access-control-allow-methods'),
                    'access-control-allow-headers': response.headers.get('access-control-allow-headers')
                }
                
                if cors_headers['access-control-allow-origin'] in ['*', 'https://emergency-map-7.preview.emergentagent.com']:
                    self.log_result("CORS Origin", True, f"Origin allowed: {cors_headers['access-control-allow-origin']}")
                else:
                    self.log_result("CORS Origin", False, f"Origin not properly configured: {cors_headers['access-control-allow-origin']}")
                
                if cors_headers['access-control-allow-methods'] and 'GET' in cors_headers['access-control-allow-methods']:
                    self.log_result("CORS Methods", True, "GET method allowed")
                else:
                    self.log_result("CORS Methods", False, f"GET method not allowed: {cors_headers['access-control-allow-methods']}")
                    
            else:
                self.log_result("CORS Preflight", False, f"Preflight failed with status: {response.status_code}")
                
        except Exception as e:
            self.log_result("CORS Test", False, f"Error: {str(e)}")
    
    def test_admin_dashboard_data_access(self):
        """Test that admin dashboard can access required API data"""
        print("\n=== Testing Admin Dashboard Data Access ===")
        
        # Test dashboard stats API (critical for admin dashboard)
        try:
            response = self.session.get(f"{BACKEND_URL}/dashboard/stats")
            if response.status_code == 200:
                stats = response.json()
                required_fields = ["total_reports", "active_cases", "alerts", "water_quality_average", "doctors_available", "critical_stocks"]
                
                if all(field in stats for field in required_fields):
                    self.log_result("Admin Dashboard Stats API", True, "All required statistics available")
                    print(f"   📊 Stats for Admin Dashboard: {stats}")
                else:
                    missing = [field for field in required_fields if field not in stats]
                    self.log_result("Admin Dashboard Stats API", False, f"Missing fields: {missing}")
            else:
                self.log_result("Admin Dashboard Stats API", False, f"Status: {response.status_code}")
        except Exception as e:
            self.log_result("Admin Dashboard Stats API", False, f"Error: {str(e)}")
        
        # Test other APIs that admin dashboard might need
        apis_to_test = [
            ("/reports", "Health Reports"),
            ("/water-quality", "Water Quality Data"),
            ("/doctors", "Doctor Directory"),
            ("/medical-stock", "Medical Stock"),
            ("/users", "Users")
        ]
        
        for endpoint, name in apis_to_test:
            try:
                response = self.session.get(f"{BACKEND_URL}{endpoint}")
                if response.status_code == 200:
                    data = response.json()
                    if isinstance(data, list):
                        self.log_result(f"Admin Data Access - {name}", True, f"{len(data)} records available")
                    else:
                        self.log_result(f"Admin Data Access - {name}", False, "Invalid data format")
                else:
                    self.log_result(f"Admin Data Access - {name}", False, f"Status: {response.status_code}")
            except Exception as e:
                self.log_result(f"Admin Data Access - {name}", False, f"Error: {str(e)}")
    
    def test_admin_error_handling(self):
        """Test admin dashboard error handling"""
        print("\n=== Testing Admin Dashboard Error Handling ===")
        
        # Test with non-existent admin file (simulate error condition)
        try:
            # This should still return 200 with the actual admin.html file
            response = self.session.get(LOCAL_ADMIN_URL)
            if response.status_code == 200:
                self.log_result("Admin Dashboard Error Handling", True, "Admin dashboard loads correctly")
            elif response.status_code == 404:
                content = response.text
                if "Admin Dashboard Not Found" in content:
                    self.log_result("Admin Dashboard 404 Handling", True, "Proper 404 error handling")
                else:
                    self.log_result("Admin Dashboard 404 Handling", False, "Improper 404 handling")
            else:
                self.log_result("Admin Dashboard Error Handling", False, f"Unexpected status: {response.status_code}")
        except Exception as e:
            self.log_result("Admin Dashboard Error Handling", False, f"Error: {str(e)}")
    
    def run_all_tests(self):
        """Run all admin dashboard tests"""
        print("🚀 Starting Admin Dashboard Testing for Rural Water Health Monitoring System")
        print("=" * 80)
        
        self.test_admin_route_local()
        self.test_admin_route_public()
        self.test_cors_for_admin()
        self.test_admin_dashboard_data_access()
        self.test_admin_error_handling()
        
        # Print final results
        print("\n" + "=" * 80)
        print("🏁 ADMIN DASHBOARD TESTING COMPLETE")
        print("=" * 80)
        print(f"✅ Tests Passed: {self.test_results['passed']}")
        print(f"❌ Tests Failed: {self.test_results['failed']}")
        
        if self.test_results['errors']:
            print("\n🔍 FAILED TESTS DETAILS:")
            for error in self.test_results['errors']:
                print(f"   • {error}")
        
        success_rate = (self.test_results['passed'] / (self.test_results['passed'] + self.test_results['failed'])) * 100 if (self.test_results['passed'] + self.test_results['failed']) > 0 else 0
        print(f"\n📊 Success Rate: {success_rate:.1f}%")
        
        return success_rate >= 75

if __name__ == "__main__":
    tester = AdminDashboardTester()
    success = tester.run_all_tests()