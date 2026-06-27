# -*- coding: utf-8 -*-
"""Dump CongoSchool pages to HTML files for review"""
import urllib.request, urllib.parse, http.cookiejar, os, sys

BASE = "http://127.0.0.1:5000"
OUT = r"C:\Users\GUSTAVE KUTSHE\.openclaw-autoclaw\workspace\congoschool\_pages"

os.makedirs(OUT, exist_ok=True)

cj = http.cookiejar.CookieJar()
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))

# Login first
print("Logging in...")
data = urllib.parse.urlencode({
    'username': 'admin',
    'password': 'congoschool2025!',
    'access_code': 'congo2025'
}).encode('utf-8')
req = urllib.request.Request(BASE + "/login", data=data)
resp = opener.open(req, timeout=5)
print(f"Login result: {resp.url}")

# Now fetch each page
pages = [
    ("/", "dashboard.html"),
    ("/students", "students.html"),
    ("/teachers", "teachers.html"),
    ("/classes", "classes.html"),
    ("/subjects", "subjects.html"),
    ("/grades", "grades.html"),
    ("/attendance", "attendance.html"),
    ("/timetable", "timetable.html"),
    ("/fees", "fees.html"),
    ("/admin/users", "admin_users.html"),
    ("/admin/access-code", "admin_access_code.html"),
]

for path, filename in pages:
    try:
        req = urllib.request.Request(BASE + path)
        resp = opener.open(req, timeout=5)
        body = resp.read().decode('utf-8', errors='replace')
        filepath = os.path.join(OUT, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(body)
        print(f"  OK: {path} -> {filename} ({len(body)} bytes)")
    except Exception as e:
        print(f"  ERR: {path}: {e}")

print("\nDone! Pages saved to: " + OUT)
