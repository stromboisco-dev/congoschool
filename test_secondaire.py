import urllib.request, urllib.parse, sys
sys.stdout.reconfigure(encoding='utf-8')

cj = urllib.request.HTTPCookieProcessor()
opener = urllib.request.build_opener(cj)

data = urllib.parse.urlencode({'cycle': 'secondaire'}).encode()
req = urllib.request.Request('http://127.0.0.1:5000/set_cycle', data=data, method='POST')
req.add_header('Referer', 'http://127.0.0.1:5000/')
opener.open(req)

for page in ['/', '/students', '/classes', '/grades', '/fees', '/attendance', '/timetable', '/subjects']:
    try:
        r = opener.open('http://127.0.0.1:5000' + page)
        body = r.read().decode()
        status = r.status
    except Exception as e:
        print(f'{page}: EXCEPTION - {e}')
        continue

    # Check for flash messages with actual content
    if 'flash-' in body and 'Erreur' in body:
        # Extract the error message
        start = body.find('flash-error')
        if start >= 0:
            msg_start = body.find('>', start) + 1
            msg_end = body.find('</div>', msg_start)
            if msg_end > msg_start:
                err = body[msg_start:msg_end].strip()
                print(f'{page}: ERROR FLASH = {err}')
            else:
                print(f'{page}: malformed flash-error at pos {start}')
        else:
            # check flash-danger
            start = body.find('flash-danger')
            if start >= 0:
                msg_start = body.find('>', start) + 1
                msg_end = body.find('</div>', msg_start)
                if msg_end > msg_start:
                    print(f'{page}: DANGER FLASH = {body[msg_start:msg_end].strip()}')
            else:
                print(f'{page}: has Erreur text but no flash-error/danger class')
    elif status != 200:
        print(f'{page}: HTTP {status}')
    else:
        print(f'{page}: OK ({len(body)} bytes)')
