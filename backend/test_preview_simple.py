#!/usr/bin/env python3
"""
Test script for the preview endpoint using urllib
"""

import urllib.request
import urllib.error
import sys

def test_preview_endpoint():
    """Test the preview endpoint with funcionario ID 5"""
    try:
        print("Testing preview endpoint...")
        
        # Test with funcionario ID 5 (as mentioned in the error)
        url = "http://localhost:5000/api/iamc/passes/preview/5"
        
        print(f"Making request to: {url}")
        
        req = urllib.request.Request(url)
        
        with urllib.request.urlopen(req, timeout=30) as response:
            status_code = response.getcode()
            headers = dict(response.headers)
            content = response.read().decode('utf-8')
            
            print(f"Response status: {status_code}")
            print(f"Response headers: {headers}")
            
            if status_code == 200:
                print("✅ Preview endpoint working correctly!")
                print(f"Content type: {headers.get('content-type')}")
                print(f"Content length: {len(content)} characters")
                
                # Save HTML content to file for inspection
                with open('preview_output.html', 'w', encoding='utf-8') as f:
                    f.write(content)
                print("HTML content saved to preview_output.html")
                
            else:
                print(f"❌ Error {status_code}: {content[:500]}")
            
    except urllib.error.HTTPError as e:
        print(f"❌ HTTP Error {e.code}: {e.read().decode('utf-8')}")
    except urllib.error.URLError as e:
        print(f"❌ URL Error: {e.reason}")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_preview_endpoint()
