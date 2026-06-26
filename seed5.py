import urllib.request, urllib.parse, traceback
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
    p("/subjects/add", {"name": "Mathematiques", "code": "MATH01", "coefficient": "4", "teacher_id": "1"})
    p("/subjects/add", {"name": "Francais", "code": "FR01", "coefficient": "4", "teacher_id": "2"})
    p("/subjects/add", {"name": "Sciences Naturelles", "code": "SCI01", "coefficient": "3", "teacher_id": "3"})
    p("/subjects/add", {"name": "Anglais", "code": "ANG01", "coefficient": "2"})
    p("/subjects/add", {"name": "Geographie", "code": "GEO01", "coefficient": "2"})
    with open(LOG, "a") as f:
        f.write("SUBJECTS done\n")
except Exception as e:
    with open(LOG, "a") as f:
        f.write(f"FATAL_SUBJ: {e}\n{traceback.format_exc()}")

try:
    p("/grades/add", {"student_id": "1", "subject_id": "1", "term": "1er Trim", "exam_type": "Examen", "score": "78", "max_score": "100"})
    p("/grades/add", {"student_id": "2", "subject_id": "1", "term": "1er Trim", "exam_type": "Devoir", "score": "91", "max_score": "100"})
    p("/grades/add", {"student_id": "1", "subject_id": "2", "term": "1er Trim", "exam_type": "Composition", "score": "65", "max_score": "100"})
    p("/grades/add", {"student_id": "2", "subject_id": "2", "term": "1er Trim", "exam_type": "Composition", "score": "88", "max_score": "100"})
    p("/grades/add", {"student_id": "3", "subject_id": "3", "term": "1er Trim", "exam_type": "Devoir", "score": "55", "max_score": "100"})
    with open(LOG, "a") as f:
        f.write("GRADES done\n")
except Exception as e:
    with open(LOG, "a") as f:
        f.write(f"FATAL_GRADES: {e}\n{traceback.format_exc()}")

try:
    p("/attendance/mark", {"student_id": "1", "date": "2025-06-25", "status": "present"})
    p("/attendance/mark", {"student_id": "2", "date": "2025-06-25", "status": "present"})
    p("/attendance/mark", {"student_id": "3", "date": "2025-06-25", "status": "absent"})
    p("/attendance/mark", {"student_id": "4", "date": "2025-06-25", "status": "retard"})
    p("/attendance/mark", {"student_id": "5", "date": "2025-06-25", "status": "present"})
    with open(LOG, "a") as f:
        f.write("ATTENDANCE done\n")
except Exception as e:
    with open(LOG, "a") as f:
        f.write(f"FATAL_ATT: {e}\n{traceback.format_exc()}")

try:
    p("/timetable/add", {"class_id": "1", "subject_id": "1", "day": "Lundi", "time_start": "07:30", "time_end": "09:00", "room": "Salle A1"})
    p("/timetable/add", {"class_id": "1", "subject_id": "2", "day": "Lundi", "time_start": "09:15", "time_end": "10:45", "room": "Salle A1"})
    p("/timetable/add", {"class_id": "1", "subject_id": "4", "day": "Mardi", "time_start": "07:30", "time_end": "09:00", "room": "Salle A2"})
    p("/timetable/add", {"class_id": "2", "subject_id": "3", "day": "Lundi", "time_start": "07:30", "time_end": "09:00", "room": "Salle B1"})
    with open(LOG, "a") as f:
        f.write("TIMETABLE done\n")
except Exception as e:
    with open(LOG, "a") as f:
        f.write(f"FATAL_TT: {e}\n{traceback.format_exc()}")

try:
    p("/fees/add", {"student_id": "1", "fee_type": "Inscription", "amount": "50000", "amount_paid": "50000", "due_date": "2025-09-15", "receipt_number": "REC-001"})
    p("/fees/add", {"student_id": "2", "fee_type": "Inscription", "amount": "50000", "amount_paid": "30000", "due_date": "2025-09-15", "receipt_number": "REC-002"})
    p("/fees/add", {"student_id": "1", "fee_type": "Scolarite", "amount": "150000", "amount_paid": "75000", "due_date": "2025-10-30", "receipt_number": "REC-003"})
    p("/fees/add", {"student_id": "3", "fee_type": "Inscription", "amount": "50000", "amount_paid": "0", "due_date": "2025-09-15", "receipt_number": "REC-004"})
    with open(LOG, "a") as f:
        f.write("ALL DONE\n")
except Exception as e:
    with open(LOG, "a") as f:
        f.write(f"FATAL_FEES: {e}\n{traceback.format_exc()}")
