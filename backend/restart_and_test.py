#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Simple backend restart and test script
"""

import subprocess
import time
import os
import sys

def stop_python_processes():
    """Stop any running Python processes"""
    try:
        subprocess.run(["taskkill", "/F", "/IM", "python.exe"], capture_output=True)
        print("🛑 Stopped existing Python processes")
    except:
        pass

def start_backend():
    """Start the backend server"""
    try:
        # Change to backend directory
        os.chdir(r"c:\Users\administrator.GTS\Develop\dinqr\backend")
        
        # Start the backend in background
        process = subprocess.Popen([
            sys.executable, "app.py"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        print("🚀 Backend started")
        return process
    except Exception as e:
        print(f"❌ Error starting backend: {e}")
        return None

def test_backend():
    """Test if backend is responding"""
    import requests
    try:
        response = requests.get("http://localhost:5000/api/iamc/departamentos")
        if response.status_code == 200:
            print("✅ Backend is responding")
            return True
    except:
        pass
    return False

if __name__ == "__main__":
    print("🔄 Restarting backend...")
    
    # Stop existing processes
    stop_python_processes()
    time.sleep(2)
    
    # Start backend
    process = start_backend()
    if not process:
        exit(1)
    
    # Wait for backend to start
    print("⏳ Waiting for backend to start...")
    for i in range(10):
        time.sleep(2)
        if test_backend():
            break
        print(f"   Attempt {i+1}/10...")
    else:
        print("❌ Backend failed to start")
        process.terminate()
        exit(1)
    
    print("✅ Backend is ready!")
    print("   Backend process ID:", process.pid)
    print("   You can now test the API endpoints")
