# -*- coding: utf-8 -*-
"""Patch CongoSchool app.py: add auth + ngrok tunnel + logout button"""

with open('app.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

out = []
i = 0

while i < len(lines):
    line = lines[i]

    # 1. After "from io import BytesIO", add functools import
    if line.strip() == 'from io import BytesIO':
        out.append(line)
        out.append('from functools import wraps\n')
        i += 1
        continue

    # 2. After app.secret_key line, add USERS dict and login_required
    if line.strip() == "app.secret_key = 'congoschool-secret-key-2025'":
        out.append(line)
        out.append('\n')
        out.append("# ── AUTHENTIFICATION ──\n")
        out.append("USERS = {\n")
        out.append("    'admin': 'congoschool2025',\n")
        out.append("    'gustavo': 'espadon2025'\n")
        out.append("}\n")
        out.append("\n")
        out.append("def login_required(f):\n")
        out.append("    @wraps(f)\n")
        out.append("    def decorated(*args, **kwargs):\n")
        out.append("        if 'logged_in' not in session:\n")
        out.append("            return redirect(url_for('login'))\n")
        out.append("        return f(*args, **kwargs)\n")
        out.append("    return decorated\n")
        out.append("\n")
        i += 1
        continue

    # 3. Add @login_required before protected routes
    # Match @app.route followed by def (not login/logout)
    if line.startswith('@app.route(') and i + 1 < len(lines):
        next_line = lines[i + 1]
        # Skip if already has @login_required
        if i > 0 and lines[i-1].strip() == '@login_required':
            out.append(line)
            i += 1
            continue
        # Don't protect login/logout
        route_arg = line[line.find('(')+1:line.find(')')]
        if "'/login'" in route_arg or '"/login"' in route_arg or "'/logout'" in route_arg or '"/logout"' in route_arg:
            out.append(line)
            i += 1
            continue
        # Add @login_required
        out.append(line)
        out.append('@login_required\n')
        i += 1
        continue

    # 4. Replace __main__ block with ngrok version
    if "if __name__ == '__main__':" in line:
        out.append("if __name__ == '__main__':\n")
        out.append("    import socket, subprocess, time, re as _re\n")
        out.append("    import urllib.request as _ur\n")
        out.append("\n")
        out.append("    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)\n")
        out.append("    try:\n")
        out.append("        s.connect(('8.8.8.8', 80))\n")
        out.append("        local_ip = s.getsockname()[0]\n")
        out.append("    except Exception:\n")
        out.append("        local_ip = '127.0.0.1'\n")
        out.append("    finally:\n")
        out.append("        s.close()\n")
        out.append("\n")
        out.append("    # Start ngrok tunnel\n")
        out.append("    public_url = None\n")
        out.append("    ngrok_paths = [\n")
        out.append("        os.path.join(os.path.expanduser('~'), 'ngrok.exe'),\n")
        out.append("        os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ngrok.exe'),\n")
        out.append("    ]\n")
        out.append("    ngrok_exe = None\n")
        out.append("    for p in ngrok_paths:\n")
        out.append("        if os.path.exists(p):\n")
        out.append("            ngrok_exe = p\n")
        out.append("            break\n")
        out.append("    if ngrok_exe:\n")
        out.append("        try:\n")
        out.append("            subprocess.Popen([ngrok_exe, 'http', '5000', '--log', 'stdout'],\n")
        out.append("                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)\n")
        out.append("            time.sleep(3)\n")
        out.append("            try:\n")
        out.append("                info = _ur.urlopen('http://127.0.0.1:4040/api/tunnels').read().decode()\n")
        out.append("                m = _re.search(r'\"public_url\":\"(https://[^\"]+)\"', info)\n")
        out.append("                if m:\n")
        out.append("                    public_url = m.group(1)\n")
        out.append("            except Exception:\n")
        out.append("                pass\n")
        out.append("        except Exception as e:\n")
        out.append("            print(f'  Tunnel ngrok erreur: {e}')\n")
        out.append("\n")
        out.append("    print()\n")
        out.append("    print('  ========================================')\n")
        out.append("    print('  CongoSchool - Serveur actif')\n")
        out.append("    print('  ========================================')\n")
        out.append("    print(f'  Ordinateur : http://localhost:5000')\n")
        out.append("    print(f'  Reseau local : http://{local_ip}:5000')\n")
        out.append("    if public_url:\n")
        out.append("        print(f'  TELEPHONE (de partout) : {public_url}')\n")
        out.append("    else:\n")
        out.append("        print('  Tunnel public : indisponible (seul WiFi local)')\n")
        out.append("    print('  ========================================')\n")
        out.append("    print('  Comptes :')\n")
        out.append("    print('    admin  / congoschool2025')\n")
        out.append("    print('    gustavo / espadon2025')\n")
        out.append("    print('  ========================================')\n")
        out.append("    print()\n")
        out.append("\n")
        out.append("    app.run(host='0.0.0.0', port=5000, debug=False)\n")
        # Skip all remaining lines (the old __main__ block)
        break

    # 5. Add logout button in sidebar (after fees link)
    if '<a href="/fees" class="{{\'active\' if page==\'fees\'}}"' in line:
        out.append(line)
        i += 1
        # Check next line for </nav>
        if i < len(lines) and '</nav>' in lines[i]:
            # Insert logout link before </nav>
            out.append('    <a href="/logout" style="margin-top:20px;border-top:1px solid #16213e;padding-top:12px;"><span class="icon">🚪</span> Déconnexion</a>\n')
        continue

    out.append(line)
    i += 1

# 6. Append login/logout routes before the end (before __main__ was)
# We need to add them. Let's find a good spot - right before the __main__ section marker
# Since we already handled __main__ and stopped, we need to insert the login routes
# They should go after all other routes but before __main__

# Find the line with "# ── CLOSE SCHOOL YEAR" or similar late section, or the last route
login_routes = '''
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

'''

# Insert login routes before the START comment
final = []
for j, l in enumerate(out):
    if '# ──────────────────────────────────────────────\n# START' in l or ('# ──' in l and 'START' in l):
        final.append(login_routes)
    final.append(l)

with open('app.py', 'w', encoding='utf-8') as f:
    f.writelines(final)

print('Patch applied successfully!')
print('Verifying syntax...')
