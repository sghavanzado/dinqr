"""
Windows Service for DINQR Backend
==================================

This module provides Windows Service functionality for the DINQR Flask application.
It allows the application to run as a Windows Service, providing automatic startup,
graceful shutdown, and service management capabilities.

Usage:
    python windows_service.py install    # Install the service
    python windows_service.py start      # Start the service
    python windows_service.py stop       # Stop the service
    python windows_service.py remove     # Remove the service
    python windows_service.py debug      # Run in debug mode (console)

Requirements:
    - pywin32 package
    - Windows operating system
    - Administrator privileges for install/remove operations
"""

import os
import sys
import time
import logging
from pathlib import Path

# Add current directory to path for imports
current_dir = Path(__file__).parent.absolute()
sys.path.insert(0, str(current_dir))

try:
    import win32serviceutil
    import win32service
    import win32event
    import win32api
    import win32con
    import servicemanager
except ImportError:
    print("ERROR: pywin32 is required for Windows Service functionality")
    print("Install with: pip install pywin32")
    sys.exit(1)

from config import ProductionConfig
from waitress_server import WaitressServer

class DINQRWindowsService(win32serviceutil.ServiceFramework):
    """Windows Service class for DINQR Backend"""
    
    # Service configuration
    _svc_name_ = ProductionConfig.WINDOWS_SERVICE_NAME
    _svc_display_name_ = ProductionConfig.WINDOWS_SERVICE_DISPLAY_NAME
    _svc_description_ = ProductionConfig.WINDOWS_SERVICE_DESCRIPTION
    _svc_deps_ = None  # No service dependencies
    _svc_reg_class_ = "DINQRWindowsService"  # Required for PyWin32 service registration
    
    def __init__(self, args):
        """Initialize the Windows Service"""
        win32serviceutil.ServiceFramework.__init__(self, args)
        
        # Create an event to listen for stop requests
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
        
        # Initialize logging
        self.setup_service_logging()
        
        # Initialize server
        self.server = None
        self.logger = logging.getLogger(__name__)
        
        self.logger.info(f"Service {self._svc_name_} initialized")
    
    def setup_service_logging(self):
        """Setup logging specifically for Windows Service"""
        try:
            # Ensure logs directory exists
            logs_dir = Path(current_dir) / 'logs'
            logs_dir.mkdir(exist_ok=True)
            
            # Service-specific log file
            service_log_file = logs_dir / 'windows_service.log'
            
            # Configure logging
            logging.basicConfig(
                level=logging.INFO,
                format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
                handlers=[
                    logging.FileHandler(str(service_log_file), encoding='utf-8'),
                    logging.StreamHandler()
                ]
            )
            
            # Also log to Windows Event Log
            servicemanager.LogMsg(
                servicemanager.EVENTLOG_INFORMATION_TYPE,
                servicemanager.PYS_SERVICE_STARTED,
                (self._svc_name_, '')
            )
            
        except Exception as e:
            print(f"Failed to setup service logging: {e}")
            # Continue without logging setup
    
    def SvcStop(self):
        """Handle service stop request"""
        try:
            self.logger.info("Service stop requested")
            
            # Report that we're stopping
            self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
            
            # Log to Windows Event Log
            servicemanager.LogMsg(
                servicemanager.EVENTLOG_INFORMATION_TYPE,
                servicemanager.PYS_SERVICE_STOPPING,
                (self._svc_name_, '')
            )
            
            # Stop the Waitress server
            if self.server:
                self.logger.info("Stopping Waitress server...")
                self.server.shutdown()
            
            # Signal the main thread to stop
            win32event.SetEvent(self.hWaitStop)
            
            self.logger.info("Service stop completed")
            
        except Exception as e:
            self.logger.error(f"Error during service stop: {str(e)}")
            servicemanager.LogErrorMsg(f"Error stopping service: {str(e)}")
    
    def SvcDoRun(self):
        """Main service execution method"""
        try:
            self.logger.info("Starting DINQR Windows Service")
            
            # Log to Windows Event Log
            servicemanager.LogMsg(
                servicemanager.EVENTLOG_INFORMATION_TYPE,
                servicemanager.PYS_SERVICE_STARTED,
                (self._svc_name_, '')
            )
            
            # Change to the correct working directory
            os.chdir(str(current_dir))
            
            # Create and configure the Waitress server
            self.server = WaitressServer(ProductionConfig)
            
            # Start the server in a separate thread
            import threading
            server_thread = threading.Thread(target=self._run_server, daemon=False)
            server_thread.start()
            
            # Wait for stop signal
            win32event.WaitForSingleObject(self.hWaitStop, win32event.INFINITE)
            
            self.logger.info("Service main thread exiting")
            
        except Exception as e:
            self.logger.error(f"Service execution error: {str(e)}")
            servicemanager.LogErrorMsg(f"Service execution error: {str(e)}")
            raise
    
    def _run_server(self):
        """Run the Waitress server in service mode"""
        try:
            self.logger.info("Starting Waitress server in service mode")
            
            # Set environment for production
            os.environ['FLASK_ENV'] = 'production'
            
            # Run the server
            self.server.run()
            
        except Exception as e:
            self.logger.error(f"Server execution error: {str(e)}")
            servicemanager.LogErrorMsg(f"Server execution error: {str(e)}")
            
            # Stop the service if server fails
            self.SvcStop()

class ServiceManager:
    """Helper class for service management operations"""
    
    @staticmethod
    def install_service():
        """Install the Windows Service"""
        try:
            print("Attempting to install Windows Service...")
            
            # Use the standard win32serviceutil approach
            # This mimics running: python windows_service.py install
            sys.argv = [sys.argv[0], 'install']
            win32serviceutil.HandleCommandLine(DINQRWindowsService)
            
            print(f"✅ Service '{DINQRWindowsService._svc_display_name_}' installed successfully")
            print("Service will start automatically on system boot")
            return True
            
        except Exception as e:
            error_msg = str(e).lower()
            
            # Check for specific permission errors
            if "access" in error_msg or "denied" in error_msg or "privilege" in error_msg:
                print("❌ ERROR: Administrator privileges required to install service")
                print("\n🔧 SOLUCIONES:")
                print("1. Ejecute CMD como Administrador:")
                print("   - Click derecho en 'Símbolo del sistema'")
                print("   - Seleccione 'Ejecutar como administrador'")
                print("2. O use PowerShell como Administrador:")
                print("   - Click derecho en 'Windows PowerShell'")
                print("   - Seleccione 'Ejecutar como administrador'")
                print("3. Verifique que UAC no esté bloqueando la operación")
                print("\n💡 ALTERNATIVA: Use NSSM")
                print("   instalar_servicio_nssm.bat")
            else:
                print(f"❌ Failed to install service: {str(e)}")
            
            return False
    
    @staticmethod
    def remove_service():
        """Remove the Windows Service"""
        try:
            print("Attempting to remove Windows Service...")
            
            # Stop the service first if it's running
            try:
                win32serviceutil.StopService(DINQRWindowsService._svc_name_)
                print("Service stopped")
                time.sleep(2)  # Wait for service to stop
            except:
                pass  # Service might not be running
            
            # Use the standard win32serviceutil approach
            sys.argv = [sys.argv[0], 'remove']
            win32serviceutil.HandleCommandLine(DINQRWindowsService)
            
            print(f"✅ Service '{DINQRWindowsService._svc_display_name_}' removed successfully")
            return True
            
        except Exception as e:
            error_msg = str(e).lower()
            
            if "access" in error_msg or "denied" in error_msg or "privilege" in error_msg:
                print("❌ ERROR: Administrator privileges required to remove service")
                print("\n🔧 SOLUCIÓN: Ejecute como Administrador")
            else:
                print(f"❌ Failed to remove service: {str(e)}")
            
            return False
    
    @staticmethod
    def start_service():
        """Start the Windows Service"""
        try:
            sys.argv = [sys.argv[0], 'start']
            win32serviceutil.HandleCommandLine(DINQRWindowsService)
            print(f"Service '{DINQRWindowsService._svc_display_name_}' started successfully")
            return True
        except Exception as e:
            print(f"Failed to start service: {str(e)}")
            return False
    
    @staticmethod
    def stop_service():
        """Stop the Windows Service"""
        try:
            sys.argv = [sys.argv[0], 'stop']
            win32serviceutil.HandleCommandLine(DINQRWindowsService)
            print(f"Service '{DINQRWindowsService._svc_display_name_}' stopped successfully")
            return True
        except Exception as e:
            print(f"Failed to stop service: {str(e)}")
            return False
    
    @staticmethod
    def restart_service():
        """Restart the Windows Service"""
        print("Restarting service...")
        if ServiceManager.stop_service():
            time.sleep(3)  # Wait for service to fully stop
            return ServiceManager.start_service()
        return False
    
    @staticmethod
    def service_status():
        """Get the Windows Service status"""
        try:
            status = win32serviceutil.QueryServiceStatus(DINQRWindowsService._svc_name_)
            status_map = {
                win32service.SERVICE_STOPPED: "Stopped",
                win32service.SERVICE_START_PENDING: "Starting",
                win32service.SERVICE_STOP_PENDING: "Stopping",
                win32service.SERVICE_RUNNING: "Running",
                win32service.SERVICE_CONTINUE_PENDING: "Continuing",
                win32service.SERVICE_PAUSE_PENDING: "Pausing",
                win32service.SERVICE_PAUSED: "Paused"
            }
            
            current_status = status_map.get(status[1], "Unknown")
            print(f"Service Status: {current_status}")
            return status[1]
            
        except Exception as e:
            print(f"Failed to get service status: {str(e)}")
            return None
    
    @staticmethod
    def is_admin():
        """Check if running with administrator privileges"""
        try:
            import ctypes
            return ctypes.windll.shell32.IsUserAnAdmin() != 0
        except:
            # Fallback method using win32api
            try:
                import win32security
                # Get current user token
                token = win32security.OpenProcessToken(
                    win32api.GetCurrentProcess(),
                    win32security.TOKEN_QUERY
                )
                
                # Check if user is in Administrators group
                admin_sid = win32security.LookupAccountName(None, "Administrators")[0]
                token_groups = win32security.GetTokenInformation(
                    token, win32security.TokenGroups
                )
                
                for group in token_groups:
                    if win32security.EqualSid(group[0], admin_sid):
                        win32api.CloseHandle(token)
                        return True
                
                win32api.CloseHandle(token)
                return False
            except:
                # Last fallback - just try to perform an admin operation
                try:
                    # Try to read a registry key that requires admin access
                    import winreg
                    key = winreg.OpenKey(
                        winreg.HKEY_LOCAL_MACHINE,
                        "SYSTEM\\CurrentControlSet\\Services",
                        0,
                        winreg.KEY_READ
                    )
                    winreg.CloseKey(key)
                    return True
                except:
                    return False

def main():
    """Main entry point for service management"""
    import argparse
    
    parser = argparse.ArgumentParser(description='DINQR Windows Service Manager')
    parser.add_argument(
        'action',
        choices=['install', 'remove', 'start', 'stop', 'restart', 'status', 'debug'],
        help='Service management action'
    )
    
    # Handle Windows Service utility commands
    if len(sys.argv) == 1:
        # No arguments, assume service is being started by Windows
        servicemanager.Initialize()
        servicemanager.PrepareToHostSingle(DINQRWindowsService)
        servicemanager.StartServiceCtrlDispatcher()
        return
    
    # Parse command line arguments
    try:
        args = parser.parse_args()
    except:
        # If argument parsing fails, try Windows Service utility
        win32serviceutil.HandleCommandLine(DINQRWindowsService)
        return
    
    # Execute the requested action
    if args.action == 'install':
        ServiceManager.install_service()
    
    elif args.action == 'remove':
        ServiceManager.remove_service()
    
    elif args.action == 'start':
        ServiceManager.start_service()
    
    elif args.action == 'stop':
        ServiceManager.stop_service()
    
    elif args.action == 'restart':
        ServiceManager.restart_service()
    
    elif args.action == 'status':
        ServiceManager.service_status()
    
    elif args.action == 'debug':
        # Run in debug mode (console mode)
        print("Running DINQR service in debug mode...")
        print("Press Ctrl+C to stop")
        
        try:
            server = WaitressServer(ProductionConfig)
            server.run()
        except KeyboardInterrupt:
            print("\nService stopped by user")

if __name__ == '__main__':
    main()
