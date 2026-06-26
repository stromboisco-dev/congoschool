"""Test CongoSchool - Add sample data via HTTP requests"""
import urllib.request
import urllib.parse

BASE = "http://localhost:5000"

def post(path, data):
    d = urllib.parse.urlencode(data).encode()
    req = urllib.request.Request(f"{BASE}{path}", data=d)
    try:
        resp = urllib.request.urlopen(req, timeout=5)
        print(f"  POST {path} -> {resp.status}")
        return resp.status
    except Exception as e:
        print(f"  POST {path} -> ERROR: {e}")
        return None

def get(path):
    try:
        resp = urllib.request.urlopen(f"{BASE}{path}", timeout=5)
        print(f"  GET {path} -> {resp.status}")
        return resp.status
    except Exception as e:
        print(f"  GET {path} -> ERROR: {e}")
        return None

print("=== CongoSchool Test ===")
print()

# 1. Classes
print("[1] Classes:")
post("/classes/add", {"name": "6eme A", "level": "6eme annee", "capacity": "40", "description": "Classe de 6eme A"})
post("/classes/add", {"name": "5eme B", "level": "5eme annee", "capacity": "35", "description": "Classe de 5eme B"})
post("/classes/add", {"name": "4eme C", "level": "4eme annee", "capacity": "38", "description": "Classe de 4eme C"})
get("/classes")
print()

# 2. Teachers
print("[2] Teachers:")
post("/teachers/add", {"first_name": "Jean", "last_name": "Mukendi", "phone": "0810001111", "email": "jm@upn.cd", "subject": "Mathematiques", "salary": "350000"})
post("/teachers/add", {"first_name": "Marie", "last_name": "Nsimba", "phone": "0820002222", "email": "mn@upn.cd", "subject": "Francais", "salary": "320000"})
post("/teachers/add", {"first_name": "Pierre", "last_name": "Kabongo", "phone": "0830003333", "subject": "Sciences", "salary": "330000"})
get("/teachers")
print()

# 3. Students
print("[3] Students:")
students = [
    {"matricule": "2025-001", "first_name": "Emmanuel", "last_name": "Kasongo", "dob": "2010-03-15", "gender": "M", "class_id": "1", "parent_name": "Papa Kasongo", "parent_phone": "0811111111"},
    {"matricule": "2025-002", "first_name": "Grace", "last_name": "Mbemba", "dob": "2010-07-22", "gender": "F", "class_id": "1", "parent_name": "Maman Mbemba", "parent_phone": "0822222222"},
    {"matricule": "2025-003", "first_name": "Joel", "last_name": "Tshimanga", "dob": "2009-01-10", "gender": "M", "class_id": "2", "parent_name": "Papa Tshimanga", "parent_phone": "0833333333"},
    {"matricule": "2025-004", "first_name": "Divine", "last_name": "Lukaku", "dob": "2009-05-30", "gender": "F", "class_id": "2", "parent_name": "Maman Lukaku", "parent_phone": "0844444444"},
    {"matricule": "2025-005", "first_name": "Patrick", "last_name": "Mokobe", "dob": "2008-11-05", "gender": "M", "class_id": "3", "parent_name": "Papa Mokobe", "parent_phone": "0855555555"},
]
for s in students:
    post("/students/add", s)
get("/students")
print()

# 4. Subjects
print("[4] Subjects:")
post("/subjects/add", {"name": "Mathematiques", "code": "MATH01", "coefficient": "4", "teacher_id": "1"})
post("/subjects/add", {"name": "Francais", "code": "FR01", "coefficient": "4", "teacher_id": "2"})
post("/subjects/add", {"name": "Sciences Naturelles", "code": "SCI01", "coefficient": "3", "teacher_id": "3"})
post("/subjects/add", {"name": "Anglais", "code": "ANG01", "coefficient": "2"})
post("/subjects/add", {"name": "Geographie", "code": "GEO01", "coefficient": "2"})
get("/subjects")
print()

# 5. Grades
print("[5] Grades:")
grades_data = [
    {"student_id": "1", "subject_id": "1", "term": "1er Trim", "exam_type": "Devoir", "score": "78", "max_score": "100"},
    {"student_id": "1", "subject_id": "1", "term": "1er Trim", "exam_type": "Examen", "score": "82", "max_score": "100"},
    {"student_id": "2", "subject_id": "1", "term": "1er Trim", "exam_type": "Devoir", "score": "91", "max_score": "100"},
    {"student_id": "1", "subject_id": "2", "term": "1er Trim", "exam_type": "Composition", "score": "65", "max_score": "100"},
    {"student_id": "2", "subject_id": "2", "term": "1er Trim", "exam_type": "Composition", "score": "88", "max_score": "100"},
    {"student_id": "3", "subject_id": "3", "term": "1er Trim", "exam_type": "Devoir", "score": "55", "max_score": "100"},
]
for g in grades_data:
    post("/grades/add", g)
get("/grades")
print()

# 6. Attendance
print("[6] Attendance:")
from datetime import date
today = date.today().isoformat()
post("/attendance/mark", {"student_id": "1", "date": today, "status": "present"})
post("/attendance/mark", {"student_id": "2", "date": today, "status": "present"})
post("/attendance/mark", {"student_id": "3", "date": today, "status": "absent"})
post("/attendance/mark", {"student_id": "4", "date": today, "status": "retard"})
post("/attendance/mark", {"student_id": "5", "date": today, "status": "present"})
get(f"/attendance?date={today}")
print()

# 7. Timetable
print("[7] Timetable:")
post("/timetable/add", {"class_id": "1", "subject_id": "1", "day": "Lundi", "time_start": "07:30", "time_end": "09:00", "room": "Salle A1"})
post("/timetable/add", {"class_id": "1", "subject_id": "2", "day": "Lundi", "time_start": "09:15", "time_end": "10:45", "room": "Salle A1"})
post("/timetable/add", {"class_id": "1", "subject_id": "4", "day": "Mardi", "time_start": "07:30", "time_end": "09:00", "room": "Salle A2"})
post("/timetable/add", {"class_id": "2", "subject_id": "3", "day": "Lundi", "time_start": "07:30", "time_end": "09:00", "room": "Salle B1"})
get("/timetable?class=1")
print()

# 8. Fees
print("[8] Fees:")
post("/fees/add", {"student_id": "1", "fee_type": "Inscription", "amount": "50000", "amount_paid": "50000", "due_date": "2025-09-15", "payment_date": "2025-09-10", "receipt_number": "REC-001"})
post("/fees/add", {"student_id": "2", "fee_type": "Inscription", "amount": "50000", "amount_paid": "30000", "due_date": "2025-09-15", "receipt_number": "REC-002"})
post("/fees/add", {"student_id": "1", "fee_type": "Scolarite", "amount": "150000", "amount_paid": "75000", "due_date": "2025-10-30", "receipt_number": "REC-003"})
post("/fees/add", {"student_id": "3", "fee_type": "Inscription", "amount": "50000", "amount_paid": "0", "due_date": "2025-09-15", "receipt_number": "REC-004"})
get("/fees")
print()

print("=" * 50)
print("  TEST TERMINE - Toutes les donnees sont chargees !")
print("  Ouvrez : http://localhost:5000")
print("=" * 50)
