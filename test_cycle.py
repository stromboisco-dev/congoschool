import urllib.request, urllib.parse, http.cookiejar

cj = http.cookiejar.CookieJar()
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))

# 1. Set cycle to secondaire
data = urllib.parse.urlencode({'cycle': 'secondaire'}).encode()
req = urllib.request.Request('http://127.0.0.1:5000/set_cycle', data=data, method='POST')
try:
    resp = opener.open(req)
    print("SET CYCLE:", resp.status, resp.headers.get("Location", "none"))
except Exception as e:
    print("SET CYCLE ERROR:", e)

# 2. Dashboard secondaire
try:
    req2 = urllib.request.Request('http://127.0.0.1:5000/')
    resp2 = opener.open(req2)
    body = resp2.read().decode('utf-8')
    print("\nDASHBOARD STATUS:", resp2.status)
    print("PAGE LENGTH:", len(body))
    
    # Check for errors
    errors = []
    for line in body.split('\n'):
        low = line.lower()
        if 'error' in low and 'display:none' not in low:
            errors.append(line.strip()[:150])
    if errors:
        print("ERRORS FOUND:")
        for e in errors[:5]:
            print("  >", e)
    else:
        print("No errors visible in page")
    
    # Check cycle selector
    if 'primaire' in body and 'secondaire' in body:
        print("Cycle selector: OK")
    else:
        print("Cycle selector: MISSING")
    
    # Check if it shows 0 eleves (expected for empty secondaire)
    if '0' in body.split('card-value')[1].split('<')[0] if 'card-value' in body else '':
        print("Shows 0 students (expected - empty secondaire)")
    
except Exception as e:
    print("DASHBOARD ERROR:", e)

# 3. Test students page in secondaire
try:
    req3 = urllib.request.Request('http://127.0.0.1:5000/students')
    resp3 = opener.open(req3)
    body3 = resp3.read().decode('utf-8')
    print("\nSTUDENTS PAGE STATUS:", resp3.status)
    print("STUDENTS PAGE LENGTH:", len(body3))
    errors3 = [l.strip()[:150] for l in body3.split('\n') if 'error' in l.lower() and 'display:none' not in l.lower()]
    if errors3:
        print("ERRORS IN STUDENTS:")
        for e in errors3[:5]:
            print("  >", e)
    else:
        print("Students page: OK")
except Exception as e:
    print("STUDENTS ERROR:", str(e)[:500])

# 4. Test classes page in secondaire
try:
    req4 = urllib.request.Request('http://127.0.0.1:5000/classes')
    resp4 = opener.open(req4)
    body4 = resp4.read().decode('utf-8')
    print("\nCLASSES PAGE STATUS:", resp4.status)
    errors4 = [l.strip()[:150] for l in body4.split('\n') if 'error' in l.lower() and 'display:none' not in l.lower()]
    if errors4:
        print("ERRORS IN CLASSES:")
        for e in errors4[:5]:
            print("  >", e)
    else:
        print("Classes page: OK")
except Exception as e:
    print("CLASSES ERROR:", str(e)[:500])

# 5. Test grades in secondaire
try:
    req5 = urllib.request.Request('http://127.0.0.1:5000/grades')
    resp5 = opener.open(req5)
    print("\nGRADES PAGE STATUS:", resp5.status)
except Exception as e:
    print("GRADES ERROR:", str(e)[:500])

# 6. Test fees in secondaire
try:
    req6 = urllib.request.Request('http://127.0.0.1:5000/fees')
    resp6 = opener.open(req6)
    print("\nFEES PAGE STATUS:", resp6.status)
except Exception as e:
    print("FEES ERROR:", str(e)[:500])

# 7. Test attendance in secondaire
try:
    req7 = urllib.request.Request('http://127.0.0.1:5000/attendance')
    resp7 = opener.open(req7)
    print("\nATTENDANCE PAGE STATUS:", resp7.status)
except Exception as e:
    print("ATTENDANCE ERROR:", str(e)[:500])

# 8. Test timetable in secondaire
try:
    req8 = urllib.request.Request('http://127.0.0.1:5000/timetable')
    resp8 = opener.open(req8)
    print("\nTIMETABLE PAGE STATUS:", resp8.status)
except Exception as e:
    print("TIMETABLE ERROR:", str(e)[:500])

print("\n=== ALL TESTS DONE ===")
