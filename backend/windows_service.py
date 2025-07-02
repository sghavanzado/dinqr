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
            # Check if running as administrator
            if not ServiceManager.is_admin():
                print("ERROR: Administrator privileges required to install service")
                return False
            
            # Install the service
            win32serviceutil.InstallService(
                DINQRWindowsService._svc_reg_class_,
                DINQRWindowsService._svc_name_,
                DINQRWindowsService._svc_display_name_,
                description=DINQRWindowsService._svc_description_,
                startType=win32service.SERVICE_AUTO_START,  # Auto-start on boot
                exeName=sys.executable,
                exeArgs=f'"{__file__}"'
            )
            
            print(f"Service '{DINQRWindowsService._svc_display_name_}' installed successfully")
            print("Service will start automatically on system boot")
            return True
            
        except Exception as e:
            print(f"Failed to install service: {str(e)}")
            return False
    
    @staticmethod
    def remove_service():
        """Remove the Windows Service"""
        try:
            if not ServiceManager.is_admin():
                print("ERROR: Administrator privileges required to remove service")
                return False
            
            # Stop the service first if it's running
            try:
                win32serviceutil.StopService(DINQRWindowsService._svc_name_)
                print("Service stopped")
                time.sleep(2)  # Wait for service to stop
            except:
                pass  # Service might not be running
            
            # Remove the service
            win32serviceutil.RemoveService(DINQRWindowsService._svc_name_)
            print(f"Service '{DINQRWindowsService._svc_display_name_}' removed successfully")
            return True
            
        except Exception as e:
            print(f"Failed to remove service: {str(e)}")
            return False
    
    @staticmethod
    def start_service():
        """Start the Windows Service"""
        try:
            win32serviceutil.StartService(DINQRWindowsService._svc_name_)
            print(f"Service '{DINQRWindowsService._svc_display_name_}' started successfully")
            return True
        except Exception as e:
            print(f"Failed to start service: {str(e)}")
            return False
    
    @staticmethod
    def stop_service():
        """Stop the Windows Service"""
        try:
            win32serviceutil.StopService(DINQRWindowsService._svc_name_)
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
            return win32api.GetUserName() in ['Administrator'] or \
                   win32con.SE_SHUTDOWN_NAME in win32api.GetTokenInformation(
                       win32api.GetCurrentProcess(), win32con.TokenPrivileges
                   )
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
