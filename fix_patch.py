with open('app.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Remove all @login_required lines that were added to non-main GET routes
# We only want @login_required on the main GET routes (list pages + dashboard + set_cycle)
# NOT on add/edit/delete POST routes
import re

# Remove @login_required from routes that shouldn't have it
# These routes should NOT have @login_required:
# - /students/add, /students/edit, /students/delete
# - /teachers/add, /teachers/edit, /teachers/delete
# - /classes/add, /classes/edit, /classes/delete
# - /subjects/add, /subjects/edit, /subjects/delete
# - /grades/add, /grades/edit, /grades/delete
# - /attendance/add, /attendance/edit, /attendance/delete
# - /timetable/add, /timetable/edit, /timetable/delete
# - /fees/add, /fees/edit, /fees/delete
# - /close_year, /export/*
# - /set_cycle (POST)
# - /fees/receipt

# Actually the simplest fix: remove ALL @login_required, then add them only to the right routes
lines = content.split('\n')
cleaned = []
for i, line in enumerate(lines):
    if line.strip() == '@login_required':
        # Check if the next non-empty line is a route we want to protect
        j = i + 1
        while j < len(lines) and lines[j].strip() == '':
            j += 1
        if j < len(lines) and lines[j].startswith('@app.route('):
            route = lines[j]
            # Only keep @login_required for main list/dashboard routes
            protected_routes = [
                "@app.route('/')",
                "@app.route('/students', methods=['GET'])",
                "@app.route('/students')",
                "@app.route('/teachers', methods=['GET'])",
                "@app.route('/teachers')",
                "@app.route('/classes', methods=['GET'])",
                "@app.route('/classes')",
                "@app.route('/subjects', methods=['GET'])",
                "@app.route('/subjects')",
                "@app.route('/grades', methods=['GET'])",
                "@app.route('/grades')",
                "@app.route('/attendance', methods=['GET'])",
                "@app.route('/attendance')",
                "@app.route('/timetable', methods=['GET'])",
                "@app.route('/timetable')",
                "@app.route('/fees', methods=['GET'])",
                "@app.route('/fees')",
            ]
            is_protected = any(p in route for p in protected_routes)
            if not is_protected:
                # Skip this @login_required
                continue
    cleaned.append(line)

content = '\n'.join(cleaned)

# Now add the missing logout route if not present
if 'def logout' not in content:
    logout_code = """
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

"""
    content = content.replace(
        "@app.route('/login', methods=['GET', 'POST'])",
        logout_code + "@app.route('/login', methods=['GET', 'POST'])"
    )

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(content)

# Count again
count = content.count('@login_required')
print(f'@login_required count: {count}')
print(f'def logout: {content.count("def logout")}')
print('Done!')
