#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script to run migration and restart backend
"""

import subprocess
import sys
import time
import os

def run_migration():
    """Run the database migration"""
    print("🔄 Running database migration...")
    
    try:
        result = subprocess.run([
            sys.executable, "migrate_add_departamento_to_cargo.py"
        ], capture_output=True, text=True, cwd=r"c:\Users\administrator.GTS\Develop\dinqr\backend")
        
        print("📋 Migration output:")
        print(result.stdout)
        
        if result.stderr:
            print("⚠️  Migration errors:")
            print(result.stderr)
        
        return result.returncode == 0
        
    except Exception as e:
        print(f"❌ Error running migration: {e}")
        return False

def stop_backend():
    """Stop any running Python processes"""
    try:
        subprocess.run(["taskkill", "/F", "/IM", "python.exe"], capture_output=True)
        print("🛑 Stopped existing backend processes")
        time.sleep(2)
    except:
        pass

def start_backend():
    """Start the backend server"""
    try:
        os.chdir(r"c:\Users\administrator.GTS\Develop\dinqr\backend")
        
        print("🚀 Starting backend server...")
        process = subprocess.Popen([
            sys.executable, "app.py"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Wait a moment for the server to start
        time.sleep(3)
        
        # Check if process is still running
        if process.poll() is None:
            print(f"✅ Backend started successfully (PID: {process.pid})")
            return True
        else:
            stdout, stderr = process.communicate()
            print("❌ Backend failed to start")
            print("stdout:", stdout.decode())
            print("stderr:", stderr.decode())
            return False
            
    except Exception as e:
        print(f"❌ Error starting backend: {e}")
        return False

if __name__ == "__main__":
    print("🔧 Migration and Backend Restart Script")
    print("=" * 50)
    
    # Run migration
    if run_migration():
        print("✅ Migration completed!")
        
        # Stop backend
        stop_backend()
        
        # Start backend
        if start_backend():
            print("✅ Backend restarted successfully!")
            print("\n🎯 You can now test cargo creation with departamento assignment")
        else:
            print("❌ Failed to restart backend")
    else:
        print("❌ Migration failed! Backend not restarted.")
    
    print("\n" + "=" * 50)
