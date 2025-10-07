#!/usr/bin/env python3
"""
Direct test of the configuration endpoint
"""

import sys
import os
import logging

# Add the backend directory to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Setup logging
logging.basicConfig(level=logging.DEBUG)

def test_configuracao_endpoint():
    """Test the configuration endpoint directly"""
    try:
        print("Testing configuration endpoint logic...")
        
        # Import the function directly
        from routes.passes_routes import obter_configuracao
        
        # Call the function
        print("Calling obter_configuracao()...")
        result = obter_configuracao()
        
        print(f"Result type: {type(result)}")
        print(f"Result: {result}")
        
        if hasattr(result, 'data'):
            print(f"Result data: {result.data}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_configuracao_endpoint()
