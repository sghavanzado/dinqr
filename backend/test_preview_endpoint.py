#!/usr/bin/env python3
"""
Test script for the preview endpoint
"""

import requests
import sys

def test_preview_endpoint():
    """Test the preview endpoint with funcionario ID 5"""
    try:
        print("Testing preview endpoint...")
        
        # Test with funcionario ID 5 (as mentioned in the error)
        url = "http://localhost:5000/api/iamc/passes/preview/5"
        
        print(f"Making request to: {url}")
        response = requests.get(url, timeout=30)
        
        print(f"Response status: {response.status_code}")
        print(f"Response headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            print("✅ Preview endpoint working correctly!")
            print(f"Content type: {response.headers.get('content-type')}")
            print(f"Content length: {len(response.text)} characters")
            
            # Save HTML content to file for inspection
            with open('preview_output.html', 'w', encoding='utf-8') as f:
                f.write(response.text)
            print("HTML content saved to preview_output.html")
            
        else:
            print(f"❌ Error {response.status_code}: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Connection error - is the backend server running?")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_preview_endpoint()
