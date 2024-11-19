import requests


a = "http://hs.vir-link.cn:2088/api/vpn/subscription_v3"
b = {
    'e': '917952140@qq.com',
    'p': 'tBX/'
}

c = requests.get(a, params=b)

d = c.json()

for e in d.get('data', []):
    for f in e.get('list', []):
        g = f.get('name', 'N/A')
        h = f.get('link', 'N/A')
        print(f"{g}: {h}")
