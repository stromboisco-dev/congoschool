import urllib.request, urllib.parse
import traceback

B = "http://localhost:5000"
LOG = r"C:\Users\GUSTAVE KUTSHE\.openclaw-autoclaw\workspace\seed_err.txt"

def p(path, data):
    try:
        d = urllib.parse.urlencode(data).encode()
        req = urllib.request.Request(B + path, data=d)
        urllib.request.urlopen(req, timeout=5)
        return True
    except Exception as e:
        with open(LOG, "a") as f:
            f.write(f"ERR {path}: {e}\n")
        return False

try:
    p("/classes/add", {"name": "6eme A", "level": "6eme annee", "capacity": "40"})
    p("/classes/add", {"name": "5eme B", "level": "5eme annee", "capacity": "35"})
    p("/classes/add", {"name": "4eme C", "level": "4eme annee", "capacity": "38"})
    with open(LOG, "a") as f:
        f.write("STEP1 done\n")
except Exception as e:
    with open(LOG, "a") as f:
        f.write(f"FATAL: {e}\n{traceback.format_exc()}")

try:
    p("/teachers/add", {"first_name": "Jean", "last_name": "Mukendi", "subject": "Mathematiques", "salary": "350000"})
    p("/teachers/add", {"first_name": "Marie", "last_name": "Nsimba", "subject": "Francais", "salary": "320000"})
    p("/teachers/add", {"first_name": "Pierre", "last_name": "Kabongo", "subject": "Sciences", "salary": "330000"})
    with open(LOG, "a") as f:
        f.write("STEP2 done\n")
except Exception as e:
    with open(LOG, "a") as f:
        f.write(f"FATAL2: {e}\n{traceback.format_exc()}")

try:
    p("/students/add", {"matricule": "2025-001", "first_name": "Emmanuel", "last_name": "Kasongo", "gender": "M", "class_id": "1", "parent_name": "Papa Kasongo", "parent_phone": "0811111111"})
    p("/students/add", {"matricule": "2025-002", "first_name": "Grace", "last_name": "Mbemba", "gender": "F", "class_id": "1", "parent_name": "Maman Mbemba", "parent_phone": "0822222222"})
    p("/students/add", {"matricule": "2025-003", "first_name": "Joel", "last_name": "Tshimanga", "gender": "M", "class_id": "2"})
    p("/students/add", {"matricule": "2025-004", "first_name": "Divine", "last_name": "Lukaku", "gender": "F", "class_id": "2"})
    p("/students/add", {"matricule": "2025-005", "first_name": "Patrick", "last_name": "Mokobe", "gender": "M", "class_id": "3"})
    with open(LOG, "a") as f:
        f.write("STEP3 done\n")
except Exception as e:
    with open(LOG, "a") as f:
        f.write(f"FATAL3: {e}\n{traceback.format_exc()}")

try:
    p("/subjects/add", {"name": "Mathematiques", "code": "MATH01", "coefficient": "4", "teacher_id": "1"})
    p("/subjects/add", {"name": "Francais", "code": "FR01", "coefficient": "4", "teacher_id": "2"})
    p("/subjects/add", {"name": "Sciences", "code": "SCI01", "coefficient": "3", "teacher_id": "3"})
    p("/subjects/add", {"name": "Anglais", "code": "ANG01", "coefficient": "2"})
    p("/subjects/add", {"name": "Geographie", "code": "GEO01", "coefficient": "2"})
    with open(LOG, "a") as f:
        f.write("STEP4 done\n")
except Exception as e:
    with open(LOG, "a") as f:
        f.write(f"FATAL4: {e}\n{traceback.format_exc()}")

try:
    p("/grades/add", {"student_id": "1", "subject_id": "1", "term": "1er Trim", "exam_type": "Examen", "score": "78", "max_score": "100"})
    p("/grades/add", {"student_id": "2", "subject_id": "1", "term": "1er Trim", "exam_type": "Devoir", "score": "91", "max_score": "100"})
    p("/grades/add", {"student_id": "1", "subject_id": "2", "term": "1er Trim", "exam_type": "Composition", "score": "65", "max_score": "100"})
    p("/grades/add", {"student_id": "2", "subject_id": "2", "term": "1er Trim", "exam_type": "Composition", "score": "88", "max_score": "100"})
    p("/grades/add", {"student_id": "3", "subject_id": "3", "term": "1er Trim", "exam_type": "Devoir", "score": "55", "max_score": "100"})
    with open(LOG, "a") as f:
        f.write("STEP5 done\n")
except Exception as e:
    with open(LOG, "a") as f:
        f.write(f"FATAL5: {e}\n{traceback.format_exc()}")

try:
    p("/attendance/mark", {"student_id": "1", "date": "2025-06-25", "status": "present"})
    p("/attendance/mark", {"student_id": "2", "date": "2025-06-25", "status": "present"})
    p("/attendance/mark", {"student_id": "3", "date": "2025-06-25", "status": "absent"})
    p("/attendance/mark", {"student_id": "4", "date": "2025-06-25", "status": "retard"})
    p("/attendance/mark", {"student_id": "5", "date": "2025-06-25", "status": "present"})
    with open(LOG, "a") as f:
        f.write("STEP6 done\n")
except Exception as e:
    with open(LOG, "a") as f:
        f.write(f"FATAL6: {e}\n{traceback.format_exc()}")

try:
    p("/timetable/add", {"class_id": "1", "subject_id": "1", "day": "Lundi", "time_start": "07:30", "time_end": "09:00", "room": "Salle A1"})
    p("/timetable/add", {"class_id": "1", "subject_id": "2", "day": "Lundi", "time_start": "09:15", "time_end": "10:45", "room": "Salle A1"})
    p("/timetable/add", {"class_id": "1", "subject_id": "4", "day": "Mardi", "time_start": "07:30", "time_end": "09:00", "room": "Salle A2"})
    p("/timetable/add", {"class_id": "2", "subject_id": "3", "day": "Lundi", "time_start": "07:30", "time_end": "09:00", "room": "Salle B1"})
    with open(LOG, "a") as f:
        f.write("STEP7 done\n")
except Exception as e:
    with open(LOG, "a") as f:
        f.write(f"FATAL7: {e}\n{traceback.format_exc()}")

try:
    p("/fees/add", {"student_id": "1", "fee_type": "Inscription", "amount": "50000", "amount_paid": "50000", "due_date": "2025-09-15", "receipt_number": "REC-001"})
    p("/fees/add", {"student_id": "2", "fee_type": "Inscription", "amount": "50000", "amount_paid": "30000", "due_date": "2025-09-15", "receipt_number": "REC-002"})
    p("/fees/add", {"student_id": "1", "fee_type": "Scolarite", "amount": "150000", "amount_paid": "75000", "due_date": "2025-10-30", "receipt_number": "REC-003"})
    p("/fees/add", {"student_id": "3", "fee_type": "Inscription", "amount": "50000", "amount_paid": "0", "due_date": "2025-09-15", "receipt_number": "REC-004"})
    with open(LOG, "a") as f:
        f.write("ALL DONE\n")
except Exception as e:
    with open(LOG, "a") as f:
        f.write(f"FATAL8: {e}\n{traceback.format_exc()}")
