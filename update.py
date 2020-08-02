import re
token="TOKENHERE"
orderre=re.compile(r"id\"\:\"([A-Za-z0-9-]+)\",\"pay")
def update():
    import requests

    headers={
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Authorization': token
    }
    data=requests.get('https://shoppy.gg/api/v1/orders/',headers=headers)
    with open('serial.txt','r+') as c:
        lines = c.read().splitlines()
        c.seek(0)
        findem=re.findall(orderre,data.text)
        for serial in findem:
            if serial not in lines and serial+"used" not in lines:
                lines.append(serial.strip())
        for serial in lines:
            c.write(serial+"\n")
        c.truncate()
        c.close()