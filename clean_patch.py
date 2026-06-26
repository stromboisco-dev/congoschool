# Patch script - modify app.py in place using line-by-line processing

filepath = 'app.py'
with open(filepath, 'r', encoding='utf-8') as f:
    lines = f.readlines()

result = []
i = 0
skip_until_next_route = False

# Routes that should have @login_required (only GET list pages + dashboard)
PROTECTED_ROUTES = {
    "@app.route('/')",
    "@app.route('/students')",
    "@app.route('/teachers')",
    "@app.route('/classes')",
    "@app.route('/subjects')",
    "@app.route('/grades')",
    "@app.route('/attendance')",
    "@app.route('/timetable')",
    "@app.route('/fees')",
}

while i < len(lines):
    line = lines[i]

    # 1. Add "from functools import wraps" after "from io import BytesIO"
    if line.strip() == 'from io import BytesIO':
        result.append(line)
        result.append('from functools import wraps\n')
        i += 1
        continue

    # 2. Add USERS dict + login_required after app.secret_key line
    if line.strip() == "app.secret_key = 'congoschool-secret-key-2025'":
        result.append(line)
        result.append('\n')
        result.append("# ── AUTHENTIFICATION ──\n")
        result.append("USERS = {\n")
        result.append("    'admin': 'congoschool2025',\n")
        result.append("    'gustavo': 'espadon2025'\n")
        result.append("}\n")
        result.append("\n")
        result.append("def login_required(f):\n")
        result.append("    @wraps(f)\n")
        result.append("    def decorated(*args, **kwargs):\n")
        result.append("        if 'logged_in' not in session:\n")
        result.append("            return redirect(url_for('login'))\n")
        result.append("        return f(*args, **kwargs)\n")
        result.append("    return decorated\n")
        result.append("\n")
        i += 1
        continue

    # 3. For @app.route lines, add @login_required before them if needed
    if line.startswith('@app.route('):
        # Check if this route should be protected
        route_line = line.strip()
        is_protected = False
        for pr in PROTECTED_ROUTES:
            if route_line.startswith(pr):
                is_protected = True
                break

        if is_protected:
            # Check if not already preceded by @login_required
            if not (result and result[-1].strip() == '@login_required'):
                result.append('@login_required\n')
        result.append(line)
        i += 1
        continue

    # 4. Add logout link in sidebar
    if '<a href="/fees" class="{{' in line and "'fees'" in line:
        result.append(line)
        i += 1
        # The next line should be </nav>
        if i < len(lines) and '</nav>' in lines[i]:
            result.append('    <a href="/logout" style="margin-top:20px;border-top:1px solid #16213e;padding-top:12px;"><span class="icon">\U0001f6aa</span> D&eacute;connexion</a>\n')
        continue

    # 5. Replace __main__ block
    if "if __name__ == '__main__':" in line:
        result.append("if __name__ == '__main__':\n")
        result.append("    import socket, subprocess, time\n")
        result.append("    import urllib.request as _ur\n")
        result.append("    import re as _re\n")
        result.append("\n")
        result.append("    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)\n")
        result.append("    try:\n")
        result.append("        s.connect(('8.8.8.8', 80))\n")
        result.append("        local_ip = s.getsockname()[0]\n")
        result.append("    except Exception:\n")
        result.append("        local_ip = '127.0.0.1'\n")
        result.append("    finally:\n")
        result.append("        s.close()\n")
        result.append("\n")
        result.append("    public_url = None\n")
        result.append("    ngrok_paths = [\n")
        result.append("        os.path.join(os.path.expanduser('~'), 'ngrok.exe'),\n")
        result.append("    ]\n")
        result.append("    for p in ngrok_paths:\n")
        result.append("        if os.path.exists(p):\n")
        result.append("            try:\n")
        result.append("                subprocess.Popen([p, 'http', '5000'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)\n")
        result.append("                time.sleep(4)\n")
        result.append("                info = _ur.urlopen('http://127.0.0.1:4040/api/tunnels').read().decode()\n")
        result.append("                m = _re.search(r'\"public_url\":\"(https://[^\"]+)\"', info)\n")
        result.append("                if m:\n")
        result.append("                    public_url = m.group(1)\n")
        result.append("            except Exception:\n")
        result.append("                pass\n")
        result.append("            break\n")
        result.append("\n")
        result.append("    print()\n")
        result.append("    print('  ========================================')\n")
        result.append("    print('  CongoSchool - Serveur actif')\n")
        result.append("    print('  ========================================')\n")
        result.append("    print(f'  Ordinateur : http://localhost:5000')\n")
        result.append("    print(f'  Reseau local : http://{local_ip}:5000')\n")
        result.append("    if public_url:\n")
        result.append("        print(f'  TELEPHONE (de partout) : {public_url}')\n")
        result.append("    else:\n")
        result.append("        print('  Tunnel public : indisponible (seul WiFi local)')\n")
        result.append("    print('  ========================================')\n")
        result.append("    print('  Comptes :')\n")
        result.append("    print('    admin  / congoschool2025')\n")
        result.append("    print('    gustavo / espadon2025')\n")
        result.append("    print('  ========================================')\n")
        result.append("    print()\n")
        result.append("\n")
        result.append("    app.run(host='0.0.0.0', port=5000, debug=False)\n")
        # Stop - skip rest of old __main__
        break

    result.append(line)
    i += 1

# 6. Insert login/logout routes before "# ── CLOSE SCHOOL YEAR" or before START
login_code = '''
# ──────────────────────────────────────────────
# AUTH - Login / Logout
# ──────────────────────────────────────────────
LOGIN_HTML = """<!DOCTYPE html>
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
</html>"""


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        if username in USERS and USERS[username] == password:
            session['logged_in'] = True
            session['user'] = username
            flash(f"Bienvenue {username} !", "success")
            return redirect(request.args.get('next') or url_for('dashboard'))
        return render_template_string(LOGIN_HTML, error='Identifiant ou mot de passe incorrect')
    return render_template_string(LOGIN_HTML, error=None)


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


'''

# Insert login routes right before the export/close_year sections
final = []
inserted = False
for line in result:
    if not inserted and ('_export_all_to_zip' in line or '# CLOSE SCHOOL YEAR' in line or '# ──' in line and 'CLOSE' in line):
        final.append(login_code)
        inserted = True
    final.append(line)

if not inserted:
    final.append(login_code)

with open(filepath, 'w', encoding='utf-8') as f:
    f.writelines(final)

# Verify
import py_compile
py_compile.compile(filepath, doraise=True)
print('PATCH APPLIED SUCCESSFULLY!')
print(f'@login_required count: {open(filepath,"r",encoding="utf-8").read().count("@login_required")}')
print(f'def login: {open(filepath,"r",encoding="utf-8").read().count("def login")}')
print(f'def logout: {open(filepath,"r",encoding="utf-8").read().count("def logout")}')
