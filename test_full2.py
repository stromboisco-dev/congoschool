
import sys
sys.path.insert(0, r"C:\Users\GUSTAVE KUTSHE\.openclaw-autoclaw\workspace\congoschool")
from app import app

with app.test_client() as c:
    # Switch to secondaire
    r = c.post("/set_cycle", data={"cycle": "secondaire"}, follow_redirects=False)
    print("set_cycle:", r.status_code, r.headers.get("Location", "none"))

    # Dashboard
    r = c.get("/")
    print("Dashboard:", r.status_code, len(r.data))
    d = r.data.decode()
    print("  cycle secondaire:", "secondaire" in d)

    # Students
    r = c.get("/students")
    print("Students:", r.status_code, len(r.data))

    # Classes
    r = c.get("/classes")
    print("Classes:", r.status_code, len(r.data))

    # Grades
    r = c.get("/grades")
    print("Grades:", r.status_code, len(r.data))

    # Attendance
    r = c.get("/attendance")
    print("Attendance:", r.status_code, len(r.data))

    # Fees
    r = c.get("/fees")
    print("Fees:", r.status_code, len(r.data))

    # Timetable
    r = c.get("/timetable")
    print("Timetable:", r.status_code, len(r.data))

    # Export students
    r = c.get("/export/students")
    print("Export:", r.status_code, r.content_type)

    # Add student
    r = c.post("/students/add", data={"matricule":"SEC-001","first_name":"Jean","last_name":"Test","gender":"M","date_of_birth":"2010-01-01"}, follow_redirects=False)
    print("Add student:", r.status_code, r.headers.get("Location","none"))

    # Verify
    r = c.get("/students")
    d = r.data.decode()
    print("Student visible:", "SEC-001" in d or "Jean Test" in d)

    # Add class
    r = c.post("/classes/add", data={"name":"1ere Secondaire","level":"1ere","capacity":"40"}, follow_redirects=False)
    print("Add class:", r.status_code, r.headers.get("Location","none"))

    r = c.get("/classes")
    d = r.data.decode()
    print("Class visible:", "1ere" in d)

    # Switch back to primaire and verify student NOT visible
    c.post("/set_cycle", data={"cycle": "primaire"}, follow_redirects=False)
    r = c.get("/students")
    d = r.data.decode()
    print("Student hidden in primaire:", "SEC-001" not in d)

    print("ALL TESTS DONE")
