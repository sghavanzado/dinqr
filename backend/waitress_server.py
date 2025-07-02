"""
DINQR Waitress Server for Windows Server Deployment
====================================================

This module provides a production-ready Waitress WSGI server for deploying
the DINQR Flask application on Windows Server with IIS.

Features:
- Waitress WSGI server (Windows-optimized)
- Windows Service support
- Graceful shutdown handling
- Comprehensive logging
- Configuration via environment variables
- Health check endpoints
- Performance monitoring
"""

import os
import sys
import signal
import logging
import threading
import time
from logging.handlers import RotatingFileHandler
from pathlib import Path

# Add the current directory to sys.path to ensure imports work
current_dir = Path(__file__).parent.absolute()
sys.path.insert(0, str(current_dir))

try:
    from waitress import serve
    from waitress.server import create_server
except ImportError:
    print("ERROR: Waitress is not installed. Run: pip install waitress")
    sys.exit(1)

from app import create_app
from config import Config, ProductionConfig, DevelopmentConfig

class WaitressServer:
    """Waitress server wrapper with Windows Service support"""
    
    def __init__(self, config_class=None):
        self.config_class = config_class or self._get_config_class()
        self.app = None
        self.server = None
        self.running = False
        self.shutdown_event = threading.Event()
        
        # Setup logging
        self.setup_logging()
        self.logger = logging.getLogger(__name__)
        
    def _get_config_class(self):
        """Determine configuration class based on environment"""
        env = os.environ.get('FLASK_ENV', 'production').lower()
        if env == 'development':
            return DevelopmentConfig
        elif env == 'testing':
            from config import TestingConfig
            return TestingConfig
        else:
            return ProductionConfig
    
    def setup_logging(self):
        """Setup comprehensive logging for the server"""
        # Ensure logs directory exists
        logs_dir = Path('logs')
        logs_dir.mkdir(exist_ok=True)
        
        # Root logger configuration
        root_logger = logging.getLogger()
        root_logger.setLevel(getattr(logging, self.config_class.LOG_LEVEL.upper(), logging.INFO))
        
        # Remove existing handlers to avoid duplicates
        for handler in root_logger.handlers[:]:
            root_logger.removeHandler(handler)
        
        # File handler with rotation
        file_handler = RotatingFileHandler(
            self.config_class.LOG_FILE,
            maxBytes=self.config_class.LOG_MAX_BYTES,
            backupCount=self.config_class.LOG_BACKUP_COUNT,
            encoding='utf-8'
        )
        file_formatter = logging.Formatter(
            '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
        )
        file_handler.setFormatter(file_formatter)
        root_logger.addHandler(file_handler)
        
        # Console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_formatter = logging.Formatter(
            '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
        )
        console_handler.setFormatter(console_formatter)
        root_logger.addHandler(console_handler)
        
        # Waitress access log
        access_log_file = logs_dir / 'waitress_access.log'
        self.access_logger = logging.getLogger('waitress.access')
        access_handler = RotatingFileHandler(
            str(access_log_file),
            maxBytes=self.config_class.LOG_MAX_BYTES,
            backupCount=self.config_class.LOG_BACKUP_COUNT
        )
        access_formatter = logging.Formatter('%(message)s')
        access_handler.setFormatter(access_formatter)
        self.access_logger.addHandler(access_handler)
        self.access_logger.setLevel(logging.INFO)
    
    def create_application(self):
        """Create and configure the Flask application"""
        try:
            self.app = create_app()
            self.app.config.from_object(self.config_class)
            
            # Additional Windows-specific configuration
            if os.name == 'nt':  # Windows
                self.app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 31536000  # 1 year
            
            self.logger.info(f"Flask application created with {self.config_class.__name__}")
            return self.app
            
        except Exception as e:
            self.logger.error(f"Failed to create Flask application: {str(e)}")
            raise
    
    def create_waitress_server(self):
        """Create and configure the Waitress server"""
        if not self.app:
            self.create_application()
        
        try:
            # Waitress server configuration
            server_config = {
                'host': self.config_class.WAITRESS_HOST,
                'port': self.config_class.WAITRESS_PORT,
                'threads': self.config_class.WAITRESS_THREADS,
                'connection_limit': self.config_class.WAITRESS_CONNECTION_LIMIT,
                'cleanup_interval': self.config_class.WAITRESS_CLEANUP_INTERVAL,
                'channel_timeout': self.config_class.WAITRESS_CHANNEL_TIMEOUT,
                'send_bytes': 18000,  # Optimized for Windows
                'max_request_header_size': 262144,  # 256KB
                'max_request_body_size': 1073741824,  # 1GB
                'expose_tracebacks': self.config_class.DEBUG,
                'ident': 'DINQR-Waitress/1.0',
            }
            
            self.logger.info(f"Creating Waitress server with config: {server_config}")
            
            self.server = create_server(self.app, **server_config)
            
            self.logger.info(
                f"Waitress server created - "
                f"Host: {server_config['host']}, "
                f"Port: {server_config['port']}, "
                f"Threads: {server_config['threads']}"
            )
            
            return self.server
            
        except Exception as e:
            self.logger.error(f"Failed to create Waitress server: {str(e)}")
            raise
    
    def setup_signal_handlers(self):
        """Setup signal handlers for graceful shutdown"""
        def signal_handler(signum, frame):
            signal_name = {
                signal.SIGINT: 'SIGINT',
                signal.SIGTERM: 'SIGTERM'
            }.get(signum, f'Signal {signum}')
            
            self.logger.info(f"Received {signal_name}, initiating graceful shutdown...")
            self.shutdown()
        
        # Only setup signal handlers if not running as Windows Service
        if not getattr(sys, 'frozen', False) and hasattr(signal, 'SIGINT'):
            signal.signal(signal.SIGINT, signal_handler)
        
        if hasattr(signal, 'SIGTERM'):
            signal.signal(signal.SIGTERM, signal_handler)
        
        self.logger.debug("Signal handlers configured")
    
    def run(self):
        """Run the Waitress server"""
        try:
            if not self.server:
                self.create_waitress_server()
            
            self.setup_signal_handlers()
            
            self.running = True
            self.logger.info("=" * 60)
            self.logger.info("DINQR Backend Server Starting")
            self.logger.info("=" * 60)
            self.logger.info(f"Environment: {self.config_class.__name__}")
            self.logger.info(f"Host: {self.config_class.WAITRESS_HOST}")
            self.logger.info(f"Port: {self.config_class.WAITRESS_PORT}")
            self.logger.info(f"Threads: {self.config_class.WAITRESS_THREADS}")
            self.logger.info(f"Debug: {self.config_class.DEBUG}")
            self.logger.info(f"Process ID: {os.getpid()}")
            self.logger.info("=" * 60)
            
            # Start monitoring thread
            monitor_thread = threading.Thread(target=self._monitor_health, daemon=True)
            monitor_thread.start()
            
            # Run the server
            self.server.run()
            
        except KeyboardInterrupt:
            self.logger.info("Received keyboard interrupt, shutting down...")
            self.shutdown()
        except Exception as e:
            self.logger.error(f"Server error: {str(e)}")
            raise
        finally:
            self.running = False
            self.logger.info("Server stopped")
    
    def _monitor_health(self):
        """Monitor server health and log statistics"""
        while self.running and not self.shutdown_event.is_set():
            try:
                if self.server and hasattr(self.server, 'task_dispatcher'):
                    # Log basic server statistics
                    active_channels = len(getattr(self.server.task_dispatcher, 'threads', []))
                    self.logger.debug(f"Active channels: {active_channels}")
                
                # Wait before next check
                self.shutdown_event.wait(300)  # Check every 5 minutes
                
            except Exception as e:
                self.logger.error(f"Health monitor error: {str(e)}")
                self.shutdown_event.wait(60)  # Wait 1 minute on error
    
    def shutdown(self):
        """Gracefully shutdown the server"""
        if not self.running:
            return
        
        self.logger.info("Initiating server shutdown...")
        self.running = False
        self.shutdown_event.set()
        
        if self.server:
            try:
                # Give active requests time to complete
                self.logger.info("Waiting for active requests to complete...")
                time.sleep(2)
                
                # Close the server
                self.server.close()
                self.logger.info("Server closed successfully")
                
            except Exception as e:
                self.logger.error(f"Error during shutdown: {str(e)}")
        
        self.logger.info("Shutdown complete")

# Convenience functions for deployment scripts
def create_server_instance(config_class=None):
    """Create a server instance for external use"""
    return WaitressServer(config_class)

def run_server(config_class=None):
    """Run the server with specified configuration"""
    server = WaitressServer(config_class)
    server.run()

def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description='DINQR Waitress Server')
    parser.add_argument(
        '--config', 
        choices=['development', 'production', 'testing'],
        default='production',
        help='Configuration environment'
    )
    parser.add_argument(
        '--host',
        default=None,
        help='Host to bind to'
    )
    parser.add_argument(
        '--port',
        type=int,
        default=None,
        help='Port to bind to'
    )
    
    args = parser.parse_args()
    
    # Select configuration
    config_map = {
        'development': DevelopmentConfig,
        'production': ProductionConfig,
        'testing': getattr(sys.modules[__name__], 'TestingConfig', ProductionConfig)
    }
    
    config_class = config_map[args.config]
    
    # Override host/port if provided
    if args.host:
        config_class.WAITRESS_HOST = args.host
    if args.port:
        config_class.WAITRESS_PORT = args.port
    
    # Run the server
    run_server(config_class)

if __name__ == '__main__':
    main()
