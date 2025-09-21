from flask import Flask, jsonify
from flask_cors import CORS

def create_simple_app():
    """Simple app just for testing dashboard"""
    app = Flask(__name__)
    
    # Configure CORS
    CORS(app, origins=['http://localhost:3000', 'http://localhost:5173'], supports_credentials=True)
    
    # Register Dashboard blueprint only
    from routes.dashboard_routes import dashboard_bp
    app.register_blueprint(dashboard_bp, url_prefix='/api/dashboard')
    
    @app.route('/health', methods=['GET'])
    def health():
        return jsonify({'status': 'OK', 'service': 'Dashboard API'})
    
    return app

if __name__ == '__main__':
    app = create_simple_app()
    print("=== DASHBOARD ROUTES ===")
    for rule in app.url_map.iter_rules():
        print(f"[ROUTE] {rule}")
    print("========================")
    
    app.run(host='127.0.0.1', port=5001, debug=True)
