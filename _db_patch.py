# -*- coding: utf-8 -*-
"""
CongoSchool - Application de Gestion Scolaire
Flask + SQLite | Tout en un seul fichier
"""

import sqlite3
import os
from datetime import datetime, date
from flask import Flask, request, redirect, url_for, render_template_string, flash, jsonify, send_file, session
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
import zipfile
import shutil
from io import BytesIO
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'congoschool-v2-secure-a7f3e9b1d4c6')

# ──────────────────────────────────────────────
# DATABASE
# ──────────────────────────────────────────────
if getattr(sys, 'frozen', False):
    # Running as PyInstaller bundle
    BASE_DIR = os.path.dirname(sys.executable)
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DB_PATH = os.environ.get('DATABASE_PATH', os.path.join(BASE_DIR, 'congoschool.db'))
