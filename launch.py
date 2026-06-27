# -*- coding: utf-8 -*-
"""CongoSchool launcher - bundled version"""
import sys
import os

if getattr(sys, 'frozen', False):
    BASE_DIR = os.path.dirname(sys.executable)
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Ensure we're in the right directory
os.chdir(BASE_DIR)

# Set the DB path before importing app
os.environ['DATABASE_PATH'] = os.path.join(BASE_DIR, 'congoschool.db')

from app import app, init_db

if __name__ == '__main__':
    init_db()

    # Auto-open browser
    import webbrowser
    import threading
    def open_browser():
        import time
        time.sleep(2)
        webbrowser.open('http://localhost:5000')
    threading.Thread(target=open_browser, daemon=True).start()

    print("=" * 50)
    print("  Ouverture de CongoSchool...")
    print("  Ordinateur : http://localhost:5000")
    print("  Telephone  : http://192.168.0.55:5000")
    print("  (Assurez-vous d'etre sur le meme WiFi)")
    print("=" * 50)

    app.run(host='0.0.0.0', port=5000, debug=False)
