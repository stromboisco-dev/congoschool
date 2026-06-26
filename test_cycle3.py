import urllib.request, urllib.parse, http.cookiejar

cj = http.cookiejar.CookieJar()
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))

# 1. Visit dashboard first to get session cookie
req = urllib.request.Request('http://127.0.0.1:5000/')
resp = opener.open(req)
print("Step 1 - Dashboard:", resp.status)
print("Cookies:", [c.name for c in cj])

# 2. Set cycle to secondaire WITH proper referer
data = urllib.parse.urlencode({'cycle': 'secondaire'}).encode()
req2 = urllib.request.Request('http://127.0.0.1:5000/set_cycle', data=data, method='POST')
req2.add_header('Referer', 'http://127.0.0.1:5000/')
try:
    resp2 = opener.open(req2)
    print("Step 2 - set_cycle:", resp2.status, resp2.url)
    print("Location:", resp2.headers.get('Location', 'none'))
except urllib.error.HTTPError as e:
    print("Step 2 - HTTP ERROR:", e.code)
    body = e.read().decode()
    print("Body:", body[:500])
except Exception as e:
    print("Step 2 - ERROR:", e)

# 3. Follow redirect manually to dashboard
try:
    resp3 = opener.open('http://127.0.0.1:5000/')
    body3 = resp3.read().decode('utf-8')
    print("\nStep 3 - Dashboard after set_cycle:", resp3.status)
    if 'secondaire' in body3:
        print("CYCLE SECONDAIRE ACTIVE - OK!")
    else:
        print("Still on primaire or error")
except Exception as e:
    print("Step 3 ERROR:", str(e)[:300])
