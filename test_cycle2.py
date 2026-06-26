import urllib.request, urllib.parse, http.cookiejar

cj = http.cookiejar.CookieJar()
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))

# Check route exists
req = urllib.request.Request('http://127.0.0.1:5000/')
resp = opener.open(req)
print("Dashboard OK:", resp.status)

# Try set_cycle
data = urllib.parse.urlencode({'cycle': 'secondaire'}).encode()
req2 = urllib.request.Request('http://127.0.0.1:5000/set_cycle', data=data, method='POST')
try:
    resp2 = opener.open(req2)
    print("set_cycle:", resp2.status)
except urllib.error.HTTPError as e:
    print("set_cycle HTTP ERROR:", e.code, e.reason)
    print("Body:", e.read().decode()[:500])
except Exception as e:
    print("set_cycle ERROR:", e)
