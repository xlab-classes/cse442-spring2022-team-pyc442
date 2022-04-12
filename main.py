from src.app.app import createApp
from src.database import wireguard_db

if __name__ == "__main__":
    wireguard_db.create_database()
    app = createApp()
    app.run(host='0.0.0.0', port=8080, debug=True, ssl_context='adhoc')
