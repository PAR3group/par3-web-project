# app.py
from par3 import create_app, socketio
from dotenv import load_dotenv
load_dotenv()

app = create_app()

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5100, allow_unsafe_werkzeug=True)