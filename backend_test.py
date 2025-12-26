#!/usr/bin/env python3
"""
Backend API Tests for DryFruto E-commerce Application
Testing bulk order settings and theme customizer functionality
"""

import requests
import json
import sys
import tempfile
import os
from typing import Dict, Any

# Get backend URL from frontend .env file
BACKEND_URL = "https://healthy-bites-49.preview.emergentagent.com/api"

class BackendTester:
    def __init__(self):
        self.backend_url = BACKEND_URL
        self.session = requests.Session()
        self.test_results = []
        
    def log_test(self, test_name: str, success: bool, details: str = ""):
        """Log test results"""
        status = "✅ PASS" if success else "❌ FAIL"
        self.test_results.append({
            "test": test_name,
            "status": status,
            "success": success,
            "details": details
        })
        print(f"{status}: {test_name}")
        if details:
            print(f"   Details: {details}")
    
    def test_get_site_settings(self) -> Dict[Any, Any]:
        """Test GET /api/site-settings endpoint"""
        try:
            response = self.session.get(f"{self.backend_url}/site-settings")
            
            if response.status_code != 200:
                self.log_test("GET /api/site-settings", False, f"Status code: {response.status_code}, Response: {response.text}")
                return {}
            
            data = response.json()
            
            # Check if required bulk order fields exist
            required_fields = ["bulkOrderProductTypes", "bulkOrderBenefits"]
            missing_fields = []
            
            for field in required_fields:
                if field not in data:
                    missing_fields.append(field)
            
            if missing_fields:
                self.log_test("GET /api/site-settings", False, f"Missing fields: {missing_fields}")
                return {}
            
            # Verify field types
            if not isinstance(data["bulkOrderProductTypes"], list):
                self.log_test("GET /api/site-settings", False, "bulkOrderProductTypes is not a list")
                return {}
            
            if not isinstance(data["bulkOrderBenefits"], list):
                self.log_test("GET /api/site-settings", False, "bulkOrderBenefits is not a list")
                return {}
            
            self.log_test("GET /api/site-settings", True, 
                         f"Found {len(data['bulkOrderProductTypes'])} product types and {len(data['bulkOrderBenefits'])} benefits")
            
            return data
            
        except requests.exceptions.RequestException as e:
            self.log_test("GET /api/site-settings", False, f"Request error: {str(e)}")
            return {}
        except json.JSONDecodeError as e:
            self.log_test("GET /api/site-settings", False, f"JSON decode error: {str(e)}")
            return {}
        except Exception as e:
            self.log_test("GET /api/site-settings", False, f"Unexpected error: {str(e)}")
            return {}
    
    def test_update_site_settings_product_types(self, current_settings: Dict[Any, Any]) -> bool:
        """Test updating bulkOrderProductTypes"""
        try:
            # Add a new product type
            new_product_types = current_settings.get("bulkOrderProductTypes", []).copy()
            new_product_types.append("Spices")
            
            update_data = {
                "bulkOrderProductTypes": new_product_types
            }
            
            response = self.session.put(
                f"{self.backend_url}/site-settings",
                json=update_data,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code != 200:
                self.log_test("PUT /api/site-settings (product types)", False, 
                             f"Status code: {response.status_code}, Response: {response.text}")
                return False
            
            data = response.json()
            
            # Verify the update
            if "Spices" not in data.get("bulkOrderProductTypes", []):
                self.log_test("PUT /api/site-settings (product types)", False, 
                             "New product type 'Spices' not found in response")
                return False
            
            self.log_test("PUT /api/site-settings (product types)", True, 
                         f"Successfully added 'Spices' to product types. Total: {len(data['bulkOrderProductTypes'])}")
            return True
            
        except Exception as e:
            self.log_test("PUT /api/site-settings (product types)", False, f"Error: {str(e)}")
            return False
    
    def test_update_site_settings_benefits(self, current_settings: Dict[Any, Any]) -> bool:
        """Test updating bulkOrderBenefits"""
        try:
            # Add a new benefit
            new_benefits = current_settings.get("bulkOrderBenefits", []).copy()
            new_benefits.append("Free delivery above 50kg")
            
            update_data = {
                "bulkOrderBenefits": new_benefits
            }
            
            response = self.session.put(
                f"{self.backend_url}/site-settings",
                json=update_data,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code != 200:
                self.log_test("PUT /api/site-settings (benefits)", False, 
                             f"Status code: {response.status_code}, Response: {response.text}")
                return False
            
            data = response.json()
            
            # Verify the update
            if "Free delivery above 50kg" not in data.get("bulkOrderBenefits", []):
                self.log_test("PUT /api/site-settings (benefits)", False, 
                             "New benefit 'Free delivery above 50kg' not found in response")
                return False
            
            self.log_test("PUT /api/site-settings (benefits)", True, 
                         f"Successfully added 'Free delivery above 50kg' to benefits. Total: {len(data['bulkOrderBenefits'])}")
            return True
            
        except Exception as e:
            self.log_test("PUT /api/site-settings (benefits)", False, f"Error: {str(e)}")
            return False
    
    def test_theme_export_api(self) -> Dict[Any, Any]:
        """Test GET /api/export-theme endpoint"""
        try:
            response = self.session.get(f"{self.backend_url}/export-theme")
            
            if response.status_code != 200:
                self.log_test("GET /api/export-theme", False, f"Status code: {response.status_code}, Response: {response.text}")
                return {}
            
            # Check Content-Disposition header for download
            content_disposition = response.headers.get('Content-Disposition', '')
            if 'attachment' not in content_disposition:
                self.log_test("GET /api/export-theme", False, "Missing Content-Disposition header for download")
                return {}
            
            # Parse JSON response
            try:
                data = response.json()
            except json.JSONDecodeError:
                self.log_test("GET /api/export-theme", False, "Response is not valid JSON")
                return {}
            
            # Check required fields in export
            required_fields = ["exportVersion", "exportDate", "themeName", "siteSettings", "categories", "products", "heroSlides", "testimonials", "giftBoxes"]
            missing_fields = []
            
            for field in required_fields:
                if field not in data:
                    missing_fields.append(field)
            
            if missing_fields:
                self.log_test("GET /api/export-theme", False, f"Missing required fields: {missing_fields}")
                return {}
            
            # Verify data types
            if not isinstance(data["siteSettings"], dict):
                self.log_test("GET /api/export-theme", False, "siteSettings is not a dict")
                return {}
            
            if not isinstance(data["categories"], list):
                self.log_test("GET /api/export-theme", False, "categories is not a list")
                return {}
            
            if not isinstance(data["products"], list):
                self.log_test("GET /api/export-theme", False, "products is not a list")
                return {}
            
            self.log_test("GET /api/export-theme", True, 
                         f"Export contains {len(data['categories'])} categories, {len(data['products'])} products, theme: {data['themeName']}")
            
            return data
            
        except requests.exceptions.RequestException as e:
            self.log_test("GET /api/export-theme", False, f"Request error: {str(e)}")
            return {}
        except Exception as e:
            self.log_test("GET /api/export-theme", False, f"Unexpected error: {str(e)}")
            return {}
    
    def test_theme_import_api(self, export_data: Dict[Any, Any]) -> bool:
        """Test POST /api/import-theme endpoint"""
        try:
            if not export_data:
                self.log_test("POST /api/import-theme", False, "No export data available for import test")
                return False
            
            # Modify the theme data slightly to test import
            modified_data = export_data.copy()
            if "siteSettings" in modified_data and "theme" in modified_data["siteSettings"]:
                # Change accent color to test theme import
                modified_data["siteSettings"]["theme"]["colors"]["accent"] = "#e11d48"
                modified_data["themeName"] = "Test Import Theme"
            
            response = self.session.post(
                f"{self.backend_url}/import-theme",
                json=modified_data,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code != 200:
                self.log_test("POST /api/import-theme", False, 
                             f"Status code: {response.status_code}, Response: {response.text}")
                return False
            
            data = response.json()
            
            if not data.get("success"):
                self.log_test("POST /api/import-theme", False, f"Import failed: {data}")
                return False
            
            self.log_test("POST /api/import-theme", True, "Theme import successful")
            return True
            
        except Exception as e:
            self.log_test("POST /api/import-theme", False, f"Error: {str(e)}")
            return False
    
    def test_site_settings_with_theme(self) -> bool:
        """Test PUT /api/site-settings with theme configuration"""
        try:
            # Test theme configuration update
            theme_config = {
                "theme": {
                    "colors": {
                        "primary": "#1e40af",
                        "accent": "#f59e0b",
                        "background": "#f8fafc"
                    },
                    "typography": {
                        "fontFamily": "Roboto, sans-serif",
                        "baseFontSize": "18px"
                    },
                    "header": {
                        "background": "#1e40af",
                        "text": "#ffffff"
                    },
                    "footer": {
                        "background": "#374151",
                        "text": "#f3f4f6"
                    },
                    "buttons": {
                        "primaryBg": "#f59e0b",
                        "primaryText": "#ffffff",
                        "borderRadius": "0.75rem"
                    },
                    "cards": {
                        "background": "#ffffff",
                        "borderRadius": "1rem",
                        "shadow": "0 4px 6px rgba(0,0,0,0.1)"
                    }
                }
            }
            
            response = self.session.put(
                f"{self.backend_url}/site-settings",
                json=theme_config,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code != 200:
                self.log_test("PUT /api/site-settings (theme)", False, 
                             f"Status code: {response.status_code}, Response: {response.text}")
                return False
            
            data = response.json()
            
            # Verify theme was saved
            if "theme" not in data:
                self.log_test("PUT /api/site-settings (theme)", False, "Theme field not found in response")
                return False
            
            saved_theme = data["theme"]
            
            # Check if our test values were saved
            if saved_theme.get("colors", {}).get("primary") != "#1e40af":
                self.log_test("PUT /api/site-settings (theme)", False, "Primary color not saved correctly")
                return False
            
            if saved_theme.get("typography", {}).get("fontFamily") != "Roboto, sans-serif":
                self.log_test("PUT /api/site-settings (theme)", False, "Font family not saved correctly")
                return False
            
            self.log_test("PUT /api/site-settings (theme)", True, "Theme configuration saved successfully")
            return True
            
        except Exception as e:
            self.log_test("PUT /api/site-settings (theme)", False, f"Error: {str(e)}")
            return False
    
    def test_theme_persistence_verification(self) -> bool:
        """Test that theme changes persist by making a fresh GET request"""
        try:
            response = self.session.get(f"{self.backend_url}/site-settings")
            
            if response.status_code != 200:
                self.log_test("Theme persistence verification", False, f"Status code: {response.status_code}")
                return False
            
            data = response.json()
            
            # Check if our theme changes are still there
            theme = data.get("theme", {})
            
            primary_color = theme.get("colors", {}).get("primary")
            font_family = theme.get("typography", {}).get("fontFamily")
            
            if primary_color != "#1e40af":
                self.log_test("Theme persistence verification", False, f"Primary color not persisted. Found: {primary_color}")
                return False
            
            if font_family != "Roboto, sans-serif":
                self.log_test("Theme persistence verification", False, f"Font family not persisted. Found: {font_family}")
                return False
            
            self.log_test("Theme persistence verification", True, "Theme changes persisted successfully")
            return True
            
        except Exception as e:
            self.log_test("Theme persistence verification", False, f"Error: {str(e)}")
            return False
        """Test that changes persist by making a fresh GET request"""
        try:
            response = self.session.get(f"{self.backend_url}/site-settings")
            
            if response.status_code != 200:
                self.log_test("Persistence verification", False, f"Status code: {response.status_code}")
                return False
            
            data = response.json()
            
            # Check if our test additions are still there
            product_types = data.get("bulkOrderProductTypes", [])
            benefits = data.get("bulkOrderBenefits", [])
            
            spices_found = "Spices" in product_types
            delivery_found = "Free delivery above 50kg" in benefits
            
            if not spices_found:
                self.log_test("Persistence verification", False, "'Spices' product type not persisted")
                return False
            
            if not delivery_found:
                self.log_test("Persistence verification", False, "'Free delivery above 50kg' benefit not persisted")
                return False
            
            self.log_test("Persistence verification", True, 
                         "Both test additions persisted successfully")
            return True
            
        except Exception as e:
            self.log_test("Persistence verification", False, f"Error: {str(e)}")
            return False
    
    def test_api_connectivity(self) -> bool:
        """Test basic API connectivity"""
        try:
            response = self.session.get(f"{self.backend_url}/")
            
            if response.status_code != 200:
                self.log_test("API Connectivity", False, f"Status code: {response.status_code}")
                return False
            
            data = response.json()
            if data.get("message") != "DryFruto API":
                self.log_test("API Connectivity", False, f"Unexpected response: {data}")
                return False
            
            self.log_test("API Connectivity", True, "Backend API is accessible")
            return True
            
        except Exception as e:
            self.log_test("API Connectivity", False, f"Error: {str(e)}")
            return False
    
    def run_all_tests(self):
        """Run all backend tests"""
        print(f"🚀 Starting Backend API Tests for DryFruto")
        print(f"Backend URL: {self.backend_url}")
        print("=" * 60)
        
        # Test 1: API Connectivity
        if not self.test_api_connectivity():
            print("\n❌ API connectivity failed. Stopping tests.")
            return False
        
        # Test 2: Get site settings
        current_settings = self.test_get_site_settings()
        if not current_settings:
            print("\n❌ Failed to get site settings. Stopping tests.")
            return False
        
        # Test 3: Update product types
        if not self.test_update_site_settings_product_types(current_settings):
            print("\n❌ Failed to update product types.")
        
        # Test 4: Update benefits
        if not self.test_update_site_settings_benefits(current_settings):
            print("\n❌ Failed to update benefits.")
        
        # Test 5: Verify persistence
        self.test_persistence_verification()
        
        # Summary
        print("\n" + "=" * 60)
        print("📊 TEST SUMMARY")
        print("=" * 60)
        
        passed = sum(1 for result in self.test_results if result["success"])
        total = len(self.test_results)
        
        for result in self.test_results:
            print(f"{result['status']}: {result['test']}")
        
        print(f"\n🎯 Results: {passed}/{total} tests passed")
        
        if passed == total:
            print("🎉 All tests passed!")
            return True
        else:
            print("⚠️  Some tests failed. Check details above.")
            return False

def main():
    """Main test execution"""
    tester = BackendTester()
    success = tester.run_all_tests()
    
    if not success:
        sys.exit(1)

if __name__ == "__main__":
    main()