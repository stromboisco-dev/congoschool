with open('app.py', 'r', encoding='utf-8') as f:
    content = f.read()
checks = [
    ('@login_required', content.count('@login_required')),
    ('def login', content.count('def login')),
    ('def logout', content.count('def logout')),
    ('USERS', 'USERS = {' in content),
    ('logout button', 'href="/logout"' in content),
    ('ngrok', 'ngrok' in content),
    ('0.0.0.0', '0.0.0.0' in content),
    ('login_required decorator', 'def login_required' in content),
]
for name, val in checks:
    status = 'OK' if val else 'MISSING!'
    print(f'  [{status}] {name}: {val}')
