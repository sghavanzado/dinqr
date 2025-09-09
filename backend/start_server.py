"""
Script simples para iniciar o servidor Flask
"""

from app import app

if __name__ == '__main__':
    print("🚀 Iniciando servidor Flask para teste IAMC...")
    app.run(debug=True, host='127.0.0.1', port=5000)
