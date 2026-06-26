import urllib.request, http.cookiejar, json

# Use Flask test client directly
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath('.')))
os.chdir(r'C:\Users\GUSTAVE KUTSHE\.openclaw-autoclaw\workspace\congoschool')

# We need to import the running app - use test client via subprocess
import subprocess
result = subprocess.run(['python', '-c', '''
import sys
sys.path.insert(0, r"C:\\Users\\GUSTAVE KUTSHE\\.openclaw-autoclaw\\workspace\\congoschool")
from app import app

with app.test_client() as c:
    # Test primaire
    print("=== PRIMAIRE ===")
    r = c.get("/")
    print("Dashboard:", r.status_code, "len:", len(r.data))
    r = c.get("/students")
    print("Students:", r.status_code, "len:", len(r.data))
    r = c.get("/classes")
    print("Classes:", r.status_code, "len:", len(r.data))
    r = c.get("/grades")
    print("Grades:", r.status_code, "len:", len(r.data))
    r = c.get("/attendance")
    print("Attendance:", r.status_code, "len:", len(r.data))
    r = c.get("/fees")
    print("Fees:", r.status_code, "len:", len(r.data))
    r = c.get("/timetable")
    print("Timetable:", r.status_code, "len:", len(r.data))
    
    # Switch to secondaire
    print("\n=== SWITCH TO SECONDAIRE ===")
    r = c.post("/set_cycle", data={"cycle": "secondaire"}, follow_redirects=False)
    print("set_cycle:", r.status_code, r.headers.get("Location", "none"))
    
    # Test secondaire pages
    print("\n=== SECONDAIRE ===")
    r = c.get("/")
    print("Dashboard:", r.status_code, "len:", len(r.data))
    data = r.data.decode()
    if "secondaire" in data:
        print("  -> Cycle secondaire actif: YES")
    else:
        print("  -> Cycle secondaire actif: NO")
    
    r = c.get("/students")
    print("Students:", r.status_code, "len:", len(r.data))
    data = r.data.decode()
    errors = [l.strip()[:120] for l in data.split("\\n") if ("500" in l or "Traceback" in l or "Internal Server Error" in l)]
    if errors:
        print("  ERRORS:", errors[:3])
    else:
        print("  -> OK")
    
    r = c.get("/classes")
    print("Classes:", r.status_code, "len:", len(r.data))
    
    r = c.get("/grades")
    print("Grades:", r.status_code, "len:", len(r.data))
    data = r.data.decode()
    errors = [l.strip()[:120] for l in data.split("\\n") if ("500" in l or "Traceback" in l or "Internal Server Error" in l)]
    if errors:
        print("  ERRORS:", errors[:3])
    else:
        print("  -> OK")
    
    r = c.get("/attendance")
    print("Attendance:", r.status_code, "len:", len(r.data))
    
    r = c.get("/fees")
    print("Fees:", r.status_code, "len:", len(r.data))
    
    r = c.get("/timetable")
    print("Timetable:", r.status_code, "len:", len(r.data))
    
    # Test export
    r = c.get("/export/students")
    print("\nExport students:", r.status_code, "content-type:", r.content_type)
    
    # Test add student in secondaire
    print("\n=== ADD STUDENT SECONDAIRE ===")
    r = c.post("/students/add", data={
        "matricule": "SEC-001",
        "first_name": "Jean",
        "last_name": "Test",
        "gender": "M",
        "date_of_birth": "2010-01-01"
    }, follow_redirects=False)
    print("Add student:", r.status_code, r.headers.get("Location", "none"))
    
    # Verify student appears
    r = c.get("/students")
    print("Students after add:", r.status_code)
    data = r.data.decode()
    if "SEC-001" in data or "Jean" in data:
        print("  -> Student visible in secondaire: YES")
    else:
        print("  -> Student NOT visible")
    
    print("\n=== ALL TESTS COMPLETE ===")
'''], capture_output=True, text=True, timeout=20)

print(result.stdout)
if result.stderr:
    print("STDERR:", result.stderr[:2000])
