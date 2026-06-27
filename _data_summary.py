# -*- coding: utf-8 -*-
"""Create simple text summaries of all CongoSchool data for Gustavo"""
import sqlite3, json

DB = r"C:\Users\GUSTAVE KUTSHE\.openclaw-autoclaw\workspace\congoschool\congoschool.db"
conn = sqlite3.connect(DB)
conn.row_factory = sqlite3.Row
c = conn.cursor()

lines = []
lines.append("=" * 55)
lines.append("   CONGOSCHOOL - DONNEES COMPLETES")
lines.append("=" * 55)

# Students
lines.append("\n--- ELEVES ---")
students = c.execute("SELECT matricule, first_name, last_name, gender, class_id, parent_name, parent_phone, status FROM students ORDER BY class_id, matricule").fetchall()
classes_map = {}
for cl in c.execute("SELECT id, name FROM classes").fetchall():
    classes_map[cl['id']] = cl['name']
for s in students:
    lines.append(f"  {s['matricule']} | {s['first_name']} {s['last_name']} | {s['gender']} | {classes_map.get(s['class_id'],'?')} | {s['parent_name']} | {s['parent_phone']} | {s['status']}")

# Teachers
lines.append("\n--- ENSEIGNANTS ---")
teachers = c.execute("SELECT id, first_name, last_name, subject, phone, salary, status FROM teachers").fetchall()
for t in teachers:
    lines.append(f"  {t['id']} | {t['first_name']} {t['last_name']} | {t['subject']} | {t['phone']} | {t['salary']} FC | {t['status']}")

# Classes
lines.append("\n--- CLASSES ---")
classes = c.execute("SELECT id, name, level, capacity, cycle FROM classes").fetchall()
for cl in classes:
    count = c.execute("SELECT COUNT(*) FROM students WHERE class_id=?", (cl['id'],)).fetchone()[0]
    lines.append(f"  {cl['name']} | Niveau: {cl['level']} | Capacite: {cl['capacity']} | Eleves: {count} | Cycle: {cl['cycle']}")

# Subjects
lines.append("\n--- MATIERES ---")
subjects = c.execute("SELECT id, name, code, coefficient FROM subjects").fetchall()
for s in subjects:
    teacher = c.execute("SELECT first_name || ' ' || last_name FROM teachers WHERE id=?", (s['id'],)).fetchone()
    tname = teacher[0] if teacher else "-"
    lines.append(f"  {s['code']} | {s['name']} | Coef: {s['coefficient']} | Prof: {tname}")

# Grades
lines.append("\n--- NOTES ---")
grades = c.execute("""
SELECT g.student_id, s.first_name || ' ' || s.last_name as student,
       sub.name as subject, g.term, g.exam_type, g.score, g.max_score,
       ROUND(CAST(g.score AS FLOAT)/g.max_score*100, 1) as pct
FROM grades g
JOIN students s ON g.student_id = s.id
JOIN subjects sub ON g.subject_id = sub.id
ORDER BY s.last_name, sub.name
""").fetchall()
for g in grades:
    lines.append(f"  {g['student']} | {g['subject']} | {g['term']} | {g['exam_type']} | {g['score']}/{g['max_score']} ({g['pct']}%)")

# Attendance
lines.append("\n--- PRESENCES ---")
att = c.execute("""
SELECT s.first_name || ' ' || s.last_name, a.date, a.status
FROM attendance a JOIN students s ON a.student_id = s.id
ORDER BY a.date DESC, s.last_name
""").fetchall()
for a in att:
    lines.append(f"  {a[0]} | {a[1]} | {a[2]}")

# Fees
lines.append("\n--- FRAIS SCOLAIRES ---")
fees = c.execute("""
SELECT s.first_name || ' ' || s.last_name, f.fee_type, f.amount, f.amount_paid,
       CASE WHEN f.amount_paid >= f.amount THEN 'Paye' ELSE 'Impaye' END as status,
       f.receipt_number, f.due_date
FROM fees f JOIN students s ON f.student_id = s.id
ORDER BY s.last_name
""").fetchall()
for f in fees:
    rest = f['amount'] - f['amount_paid']
    lines.append(f"  {f[0]} | {f[1]} | Total: {f[2]} FC | Paye: {f[3]} FC | Reste: {rest} FC | {f[5]} | {f[6]}")

# Timetable
lines.append("\n--- EMPLOI DU TEMPS ---")
tt = c.execute("""
SELECT c.name as classe, sub.name as subject, t.day, t.time_start, t.time_end, t.room
FROM timetable t
JOIN classes c ON t.class_id = c.id
JOIN subjects sub ON t.subject_id = sub.id
ORDER BY c.name, t.day, t.time_start
""").fetchall()
for t in tt:
    lines.append(f"  {t['classe']} | {t['subject']} | {t['day']} | {t['time_start']}-{t['time_end']} | {t['room']}")

# Users
lines.append("\n--- UTILISATEURS ---")
users = c.execute("SELECT id, username, full_name, role, is_active, created_at FROM users").fetchall()
for u in users:
    lines.append(f"  {u['id']} | {u['username']} | {u['full_name']} | Role: {u['role']} | Actif: {u['is_active']}")

# Access code
lines.append("\n--- CODE D'ACCES ---")
code = c.execute("SELECT value, updated_at FROM system_settings WHERE key='access_code'").fetchone()
if code:
    lines.append(f"  Code: {code[0]}")
    lines.append(f"  Modifie: {code[1]}")

conn.close()

output = "\n".join(lines)
print(output)

# Save
with open(r"C:\Users\GUSTAVE KUTSHE\.openclaw-autoclaw\workspace\congoschool\_data_summary.txt", "w", encoding="utf-8") as f:
    f.write(output)
print("\n(Saved to _data_summary.txt)")
