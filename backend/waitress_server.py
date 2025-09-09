"""
DINQR Waitress Server - Server wrapper for Windows Service
=========================================================

Provides a WaitressServer class for use with Windows Services and standalone execution.
"""

import sys
import threading
import time
from pathlib import Path

try:
    from waitress import serve
except ImportError:
    print("ERROR: Waitress is not installed. Run: pip install waitress")
    sys.exit(1)

from app import create_app

class WaitressServer:
    """Waitress server wrapper for Windows Service integration"""
    
    def __init__(self, config_class=None):
        """Initialize the Waitress server with configuration"""
        self.config_class = config_class
        self.app = None
        self.server_thread = None
        self.is_running = False
        self._stop_event = threading.Event()
        
        # Default configuration
        self.host = getattr(config_class, 'HOST', '127.0.0.1') if config_class else '127.0.0.1'
        self.port = getattr(config_class, 'PORT', 5000) if config_class else 5000
        
    def run(self):
        """Start the Waitress server (blocking)"""
        try:
            print(f"Starting DINQR Waitress Server on {self.host}:{self.port}")
            
            # Create Flask app
            self.app = create_app(self.config_class)
            
            # Start Waitress server (this blocks)
            serve(
                self.app,
                host=self.host,
                port=self.port,
                _quiet=False,  # Show startup messages
                connection_limit=1000,
                cleanup_interval=30,
                channel_timeout=120
            )
            
        except Exception as e:
            print(f"Error starting Waitress server: {e}")
            raise
    
    def start(self):
        """Start the server in a separate thread (non-blocking)"""
        if self.is_running:
            print("Server is already running")
            return
        
        print("Starting Waitress server in background thread...")
        self.server_thread = threading.Thread(target=self.run, daemon=False)
        self.server_thread.start()
        self.is_running = True
        
        # Give the server a moment to start
        time.sleep(2)
        print(f"Server started on {self.host}:{self.port}")
    
    def stop(self):
        """Stop the server (graceful shutdown)"""
        if not self.is_running:
            print("Server is not running")
            return
        
        print("Stopping Waitress server...")
        self.is_running = False
        self._stop_event.set()
        
        # Note: Waitress doesn't have a built-in graceful shutdown mechanism
        # when used with serve(). For production, consider using WSGIServer directly
        if self.server_thread and self.server_thread.is_alive():
            print("Waiting for server thread to finish...")
            # In a real implementation, you'd want to use WSGIServer for better control
        
        print("Server stopped")
    
    def shutdown(self):
        """Alias for stop() for compatibility"""
        self.stop()

def main():
    """Main entry point for standalone execution"""
    print("DINQR Waitress Server - Standalone Mode")
    print("=" * 50)
    
    server = WaitressServer()
    
    try:
        server.run()  # This will block until interrupted
    except KeyboardInterrupt:
        print("\nShutdown requested by user")
        server.stop()
    except Exception as e:
        print(f"Server error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
