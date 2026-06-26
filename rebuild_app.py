# -*- coding: utf-8 -*-
"""
CongoSchool - Application de Gestion Scolaire
Flask + SQLite | Tout en un seul fichier
"""

import sqlite3
import os
from datetime import datetime, date
from flask import Flask, request, redirect, url_for, render_template_string, flash, jsonify, send_file, session
from functools import wraps
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
import zipfile
import shutil
from io import BytesIO

app = Flask(__name__)
app.secret_key = 'congoschool-secret-key-2025'

# ── AUTHENTIFICATION ──
USERS = {
    'admin': 'congoschool2025',
    'gustavo': 'espadon2025'
}

def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'logged_in' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'congoschool.db')


# ──────────────────────────────────────────────
# DATABASE
# ──────────────────────────────────────────────
def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    conn = get_db()
    c = conn.cursor()

    c.executescript('''
        CREATE TABLE IF NOT EXISTS classes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            level TEXT,
            capacity INTEGER DEFAULT 40,
            teacher_id INTEGER,
            description TEXT,
            cycle TEXT DEFAULT 'primaire',
            FOREIGN KEY (teacher_id) REFERENCES teachers(id)
        );
        CREATE TABLE IF NOT EXISTS teachers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            phone TEXT,
            email TEXT,
            subject TEXT,
            address TEXT,
            hire_date TEXT,
            status TEXT DEFAULT 'actif',
            salary REAL DEFAULT 0
        );
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            matricule TEXT UNIQUE NOT NULL,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            date_of_birth TEXT,
            gender TEXT,
            class_id INTEGER,
            parent_name TEXT,
            parent_phone TEXT,
            address TEXT,
            email TEXT,
            enrollment_date TEXT,
            status TEXT DEFAULT 'actif',
            cycle TEXT DEFAULT 'primaire',
            FOREIGN KEY (class_id) REFERENCES classes(id)
        );
        CREATE TABLE IF NOT EXISTS subjects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            code TEXT,
            coefficient INTEGER DEFAULT 1,
            teacher_id INTEGER,
            class_id INTEGER,
            description TEXT,
            FOREIGN KEY (teacher_id) REFERENCES teachers(id),
            FOREIGN KEY (class_id) REFERENCES classes(id)
        );
        CREATE TABLE IF NOT EXISTS grades (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER NOT NULL,
            subject_id INTEGER NOT NULL,
            term TEXT,
            exam_type TEXT,
            score REAL NOT NULL,
            max_score REAL DEFAULT 20,
            date TEXT,
            comment TEXT,
            FOREIGN KEY (student_id) REFERENCES students(id),
            FOREIGN KEY (subject_id) REFERENCES subjects(id)
        );
        CREATE TABLE IF NOT EXISTS attendance (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER NOT NULL,
            date TEXT NOT NULL,
            status TEXT NOT NULL,
            comment TEXT,
            FOREIGN KEY (student_id) REFERENCES students(id)
        );
        CREATE TABLE IF NOT EXISTS fees (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER NOT NULL,
            fee_type TEXT,
            amount REAL DEFAULT 0,
            amount_paid REAL DEFAULT 0,
            due_date TEXT,
            payment_date TEXT,
            status TEXT DEFAULT 'impaye',
            receipt_number TEXT,
            comment TEXT,
            FOREIGN KEY (student_id) REFERENCES students(id)
        );
        CREATE TABLE IF NOT EXISTS timetable (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            class_id INTEGER NOT NULL,
            subject_id INTEGER NOT NULL,
            day TEXT,
            time_start TEXT,
            time_end TEXT,
            room TEXT,
            FOREIGN KEY (class_id) REFERENCES classes(id),
            FOREIGN KEY (subject_id) REFERENCES subjects(id)
        );
    ''')

    try:
        c.execute("ALTER TABLE classes ADD COLUMN cycle TEXT DEFAULT 'primaire'")
    except:
        pass
    try:
        c.execute("ALTER TABLE students ADD COLUMN cycle TEXT DEFAULT 'primaire'")
    except:
        pass

    count = c.execute("SELECT COUNT(*) FROM students").fetchone()[0]
    if count == 0:
        c.execute("INSERT INTO teachers (first_name,last_name,phone,email,subject,hire_date,status,salary) VALUES (?,?,?,?,?,?,?,?)",
                  ("Jean", "Mukendi", "+243810000001", "jmukendi@school.cd", "Mathematiques", "2020-09-01", "actif", 450000))
        c.execute("INSERT INTO teachers (first_name,last_name,phone,email,subject,hire_date,status,salary) VALUES (?,?,?,?,?,?,?,?)",
                  ("Marie", "Nsimba", "+243810000002", "mnsimba@school.cd", "Francais", "2019-09-01", "actif", 430000))
        c.execute("INSERT INTO teachers (first_name,last_name,phone,email,subject,hire_date,status,salary) VALUES (?,?,?,?,?,?,?,?)",
                  ("Pierre", "Kabongo", "+243810000003", "pkabongo@school.cd", "Sciences", "2021-09-01", "actif", 440000))

        c.execute("INSERT INTO classes (name,level,capacity,teacher_id,description) VALUES (?,?,?,?,?)",
                  ("6eme A", "6eme", 45, 1, "Classe de 6eme annee option A"))
        c.execute("INSERT INTO classes (name,level,capacity,teacher_id,description) VALUES (?,?,?,?,?)",
                  ("5eme B", "5eme", 40, 2, "Classe de 5eme annee option B"))
        c.execute("INSERT INTO classes (name,level,capacity,teacher_id,description) VALUES (?,?,?,?,?)",
                  ("4eme C", "4eme", 40, 3, "Classe de 4eme annee option C"))

        today = date.today().isoformat()
        students_data = [
            ("2025-001", "Emmanuel", "Kasongo", "2012-03-15", "M", 1, "Papa Kasongo", "+243820000001", "Matonge, Kinshasa"),
            ("2025-002", "Grace", "Mbemba", "2012-07-22", "F", 1, "Maman Mbemba", "+243820000002", "Lemba, Kinshasa"),
            ("2025-003", "Joel", "Tshimanga", "2013-01-10", "M", 2, "Papa Tshimanga", "+243820000003", "Kalamu, Kinshasa"),
            ("2025-004", "Divine", "Lukaku", "2013-05-30", "F", 2, "Maman Lukaku", "+243820000004", "Ngiri-Ngiri, Kinshasa"),
            ("2025-005", "Patrick", "Mokobe", "2012-11-05", "M", 3, "Papa Mokobe", "+243820000005", "Bandunduville, Kinshasa"),
        ]
        for sd in students_data:
            c.execute("INSERT INTO students (matricule,first_name,last_name,date_of_birth,gender,class_id,parent_name,parent_phone,address,enrollment_date,status) VALUES (?,?,?,?,?,?,?,?,?,?,?)",
                      (*sd, today, "actif"))

        subjects_data = [
            ("Mathematiques", "MATH", 4, 1, None, "Cours de mathematiques"),
            ("Francais", "FRA", 4, 2, None, "Cours de langue francaise"),
            ("Sciences Naturelles", "SCN", 3, 3, None, "Sciences de la nature"),
            ("Anglais", "ANG", 2, 2, None, "Cours d'anglais"),
            ("Geographie", "GEO", 2, 1, None, "Geographie generale"),
        ]
        for sb in subjects_data:
            c.execute("INSERT INTO subjects (name,code,coefficient,teacher_id,class_id,description) VALUES (?,?,?,?,?,?)", sb)

        grades_data = [
            (1,1,"1er Trimestre","Devoir",15,20),(1,2,"1er Trimestre","Devoir",12,20),(1,3,"1er Trimestre","Devoir",17,20),(1,4,"1er Trimestre","Devoir",14,20),(1,5,"1er Trimestre","Devoir",13,20),
            (2,1,"1er Trimestre","Devoir",18,20),(2,2,"1er Trimestre","Devoir",16,20),(2,3,"1er Trimestre","Devoir",14,20),(2,4,"1er Trimestre","Devoir",19,20),(2,5,"1er Trimestre","Devoir",15,20),
            (3,1,"1er Trimestre","Devoir",11,20),(3,2,"1er Trimestre","Devoir",13,20),(3,3,"1er Trimestre","Devoir",10,20),(3,4,"1er Trimestre","Devoir",12,20),(3,5,"1er Trimestre","Devoir",9,20),
            (4,1,"1er Trimestre","Devoir",16,20),(4,2,"1er Trimestre","Devoir",17,20),(4,3,"1er Trimestre","Devoir",15,20),(4,4,"1er Trimestre","Devoir",18,20),(4,5,"1er Trimestre","Devoir",14,20),
            (5,1,"1er Trimestre","Devoir",13,20),(5,2,"1er Trimestre","Devoir",11,20),(5,3,"1er Trimestre","Devoir",14,20),(5,4,"1er Trimestre","Devoir",10,20),(5,5,"1er Trimestre","Devoir",12,20),
        ]
        for gd in grades_data:
            c.execute("INSERT INTO grades (student_id,subject_id,term,exam_type,score,max_score,date) VALUES (?,?,?,?,?,?,?)",
                      (*gd, today))

        att_statuses = [("present",""),("present",""),("absent","Maladie"),("present",""),("retard","Embouteillage")]
        for i,(st,cm) in enumerate(att_statuses,1):
            c.execute("INSERT INTO attendance (student_id,date,status,comment) VALUES (?,?,?,?)",(i,today,st,cm))

        tt_data = [
            (1,1,"Lundi","07:30","09:00","Salle A1"),(1,2,"Lundi","09:15","10:45","Salle A1"),
            (1,3,"Mardi","07:30","09:00","Labo Sciences"),(1,4,"Mardi","09:15","10:45","Salle A1"),
            (1,5,"Mercredi","07:30","09:00","Salle A1"),(2,1,"Lundi","07:30","09:00","Salle B1"),
            (2,2,"Lundi","09:15","10:45","Salle B1"),(2,3,"Mardi","07:30","09:00","Labo Sciences"),
            (2,5,"Mercredi","07:30","09:00","Salle B1"),(3,1,"Lundi","07:30","09:00","Salle C1"),
            (3,3,"Mardi","07:30","09:00","Labo Sciences"),(3,4,"Mercredi","07:30","09:00","Salle C1"),
        ]
        for td in tt_data:
            c.execute("INSERT INTO timetable (class_id,subject_id,day,time_start,time_end,room) VALUES (?,?,?,?,?,?)",td)

        fee_data = [
            (1,"Inscription",150000,150000,"2025-09-15","2025-09-10","paye","REC-001"),
            (2,"Inscription",150000,150000,"2025-09-15","2025-09-12","paye","REC-002"),
            (3,"Inscription",150000,80000,"2025-09-15","2025-09-14","partiel","REC-003"),
            (4,"Inscription",150000,0,"2025-09-15",None,"impaye",None),
            (5,"Inscription",150000,75000,"2025-09-15","2025-09-13","partiel","REC-004"),
        ]
        for fd in fee_data:
            c.execute("INSERT INTO fees (student_id,fee_type,amount,amount_paid,due_date,payment_date,status,receipt_number) VALUES (?,?,?,?,?,?,?,?)",fd)

    conn.commit()
    conn.close()


init_db()

# ──────────────────────────────────────────────
# HELPERS
# ──────────────────────────────────────────────
def badge(status, cat="default"):
    colors = {
        "actif":"badge-success","inactif":"badge-danger",
        "paye":"badge-success","partiel":"badge-warning","impaye":"badge-danger",
        "present":"badge-success","absent":"badge-danger","retard":"badge-warning",
        "présent":"badge-success","absent":"badge-danger","retard":"badge-warning",
        "M":"badge-info","F":"badge-pink",
    }
    cls = colors.get(status.lower() if status else "","badge-secondary")
    return f'<span class="badge {cls}">{status or "-"}</span>'


def status_select(name, current="", options=None):
    if options is None:
        options = ["actif","inactif"]
    parts = [f'<select name="{name}" class="form-select">']
    for o in options:
        sel = ' selected' if o == current else ''
        parts.append(f'<option value="{o}"{sel}>{o}</option>')
    parts.append('</select>')
    return '\n'.join(parts)


# ──────────────────────────────────────────────
# BASE TEMPLATE
# ──────────────────────────────────────────────
# NOTE: All original HTML template code goes here exactly as in the backup
# I will load it from the backup and only modify the needed parts

# Load the original file content up to routes, then append my routes
print("BUILDING APP FROM BACKUP...")
