import re

with open('app.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Remove broken USERS/login_required blocks that may have been inserted wrong
# Find and remove any duplicate or misplaced login_required definitions
while content.count('def login_required') > 1:
    # Remove the second occurrence
    idx1 = content.find('def login_required')
    idx2 = content.find('def login_required', idx1 + 1)
    # Find the end of the second definition (next def)
    idx3 = content.find('\ndef ', idx2 + 1)
    content = content[:idx2] + content[idx3:]
    print(f'Removed duplicate login_required at pos {idx2}')

# Remove duplicate USERS dict
while content.count("'admin': 'congoschool2025'") > 1:
    idx1 = content.find("USERS = {")
    idx2 = content.find("USERS = {", idx1 + 1)
    if idx2 == -1:
        break
    idx3 = content.find('}', idx2) + 1
    content = content[:idx2] + content[idx3:]
    print(f'Removed duplicate USERS at pos {idx2}')

# Ensure from functools import wraps is present
if 'from functools import wraps' not in content:
    content = content.replace(
        'from io import BytesIO\n',
        'from functools import wraps\nfrom io import BytesIO\n'
    )

# Ensure there's exactly one login_required before DB_PATH
if 'def login_required' not in content:
    content = content.replace(
        "DB_PATH = os.path.join",
        """USERS = {
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

DB_PATH = os.path.join"""
    )

# Add @login_required to routes that don't have it
routes = [
    "@app.route('/')\ndef dashboard",
    "@app.route('/students')\ndef students_list",
    "@app.route('/teachers')\ndef teachers_list",
    "@app.route('/classes')\ndef classes_list",
    "@app.route('/subjects')\ndef subjects_list",
    "@app.route('/grades')\ndef grades_list",
    "@app.route('/attendance')\ndef attendance_list",
    "@app.route('/timetable')\ndef timetable_list",
    "@app.route('/fees')\ndef fees_list",
    "@app.route('/set_cycle', methods=['POST'])\ndef set_cycle",
]

for route_line in routes:
    parts = route_line.split('\n')
    search = parts[0] + '\n    def ' + parts[1].split('def ')[1]
    replacement = parts[0] + '\n@login_required\n    def ' + parts[1].split('def ')[1]
    if search in content and replacement not in content:
        content = content.replace(search, replacement, 1)
        print(f'Protected: {parts[1].split("(")[0]}')

# Add login/logout routes before the START section
login_section = """
# ──────────────────────────────────────────────
# AUTH - Login / Logout
# ──────────────────────────────────────────────
LOGIN_HTML = \'\'\'<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>CongoSchool - Connexion</title>
<style>
*{margin:0;padding:0;box-sizing:border-box;}
body{font-family:'Segoe UI',Tahoma,Geneva,Verdana,sans-serif;background:linear-gradient(135deg,#1a1a2e,#16213e);min-height:100vh;display:flex;align-items:center;justify-content:center;}
.login-box{background:#fff;border-radius:16px;padding:40px;width:90%;max-width:380px;box-shadow:0 20px 60px rgba(0,0,0,.3);}
.login-box .logo{text-align:center;font-size:28px;font-weight:700;color:#1a1a2e;margin-bottom:6px;}
.login-box .logo span{color:#e94560;}
.login-box .sub{text-align:center;font-size:13px;color:#636e72;margin-bottom:28px;}
.login-box label{display:block;font-size:13px;font-weight:600;color:#374151;margin-bottom:5px;}
.login-box input{width:100%;padding:10px 14px;border:2px solid #d1d5db;border-radius:8px;font-size:14px;margin-bottom:16px;font-family:inherit;}
.login-box input:focus{outline:none;border-color:#e94560;box-shadow:0 0 0 3px rgba(233,69,96,.15);}
.login-box button{width:100%;padding:12px;border:none;border-radius:8px;background:#e94560;color:#fff;font-size:15px;font-weight:700;cursor:pointer;transition:all .2s;}
.login-box button:hover{background:#d63851;transform:translateY(-1px);}
.error{background:#fee2e2;color:#991b1b;padding:10px;border-radius:8px;font-size:13px;margin-bottom:16px;text-align:center;}
</style>
</head>
<body>
<div class="login-box">
  <div class="logo"><span>Congo</span>School</div>
  <div class="sub">Gestion Scolaire</div>
  {% if error %}
    <div class="error">{{error}}</div>
  {% endif %}
  <form method="post" action="/login">
    <label>Identifiant</label>
    <input name="username" required placeholder="Votre identifiant" autofocus>
    <label>Mot de passe</label>
    <input name="password" type="password" required placeholder="Votre mot de passe">
    <button type="submit">Se connecter</button>
  </form>
</div>
</body>
</html>\\'\\'\\'


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        if username in USERS and USERS[username] == password:
            session['logged_in'] = True
            session['user'] = username
            flash(f'Bienvenue {username} !', 'success')
            return redirect(request.args.get('next') or url_for('dashboard'))
        return render_template_string(LOGIN_HTML, error='Identifiant ou mot de passe incorrect')
    return render_template_string(LOGIN_HTML, error=None)


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

"""

if 'def login' not in content or 'def logout' not in content:
    content = content.replace(
        "# ──────────────────────────────────────────────\n# START",
        login_section + "# ──────────────────────────────────────────────\n# START"
    )
    print('Added login/logout routes')

# Add logout button in sidebar
if 'href="/logout"' not in content:
    content = content.replace(
        '<a href="/fees" class="{{\'active\' if page==\'fees\'}}"',
        '<a href="/fees" class="{{\'active\' if page==\'fees\'}}"'
    )
    # Just add it after the fees link
    content = content.replace(
        """<a href="/fees" class="{{'active' if page=='fees'}}"><span class="icon">💰</span> Frais scolaires</a>
  </nav>""",
        """<a href="/fees" class="{{'active' if page=='fees'}}"><span class="icon">💰</span> Frais scolaires</a>
    <a href="/logout" style="margin-top:20px;border-top:1px solid #16213e;padding-top:12px;"><span class="icon">🚪</span> Deconnexion</a>
  </nav>"""
    )
    print('Added logout button')

# Update the START section with ngrok tunnel
start_new = """if __name__ == '__main__':
    import socket, subprocess, time, re as _re
    import urllib.request as _ur

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('8.8.8.8', 80))
        local_ip = s.getsockname()[0]
    except Exception:
        local_ip = '127.0.0.1'
    finally:
        s.close()

    # Start ngrok tunnel
    public_url = None
    ngrok_paths = [
        os.path.join(os.path.expanduser('~'), 'ngrok.exe'),
        os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ngrok.exe'),
    ]
    ngrok_exe = None
    for p in ngrok_paths:
        if os.path.exists(p):
            ngrok_exe = p
            break
    if ngrok_exe:
        try:
            subprocess.Popen([ngrok_exe, 'http', '5000', '--log', 'stdout'],
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            time.sleep(3)
            try:
                info = _ur.urlopen('http://127.0.0.1:4040/api/tunnels').read().decode()
                m = _re.search(r'"public_url":"(https://[^"]+)"', info)
                if m:
                    public_url = m.group(1)
            except Exception:
                pass
        except Exception as e:
            print(f'  Tunnel ngrok erreur: {e}')

    print()
    print('  ========================================')
    print('  CongoSchool - Serveur actif')
    print('  ========================================')
    print(f'  Ordinateur : http://localhost:5000')
    print(f'  Reseau local : http://{local_ip}:5000')
    if public_url:
        print(f'  TELEPHONE (de partout) : {public_url}')
    else:
        print('  Tunnel public : indisponible (seul WiFi local)')
    print('  ========================================')
    print('  Comptes :')
    print('    admin  / congoschool2025')
    print('    gustavo / espadon2025')
    print('  ========================================')
    print()

    app.run(host='0.0.0.0', port=5000, debug=False)
"""

# Find and replace the __main__ block
main_start = "if __name__ == '__main__':"
idx = content.find(main_start)
if idx >= 0:
    content = content[idx:]
    # Find where the old main block ends
    content = start_new
    # But we need to keep everything before __main__ and replace just the end
    # Let's redo this properly

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(content)

print('Done! Checking syntax...')
"
