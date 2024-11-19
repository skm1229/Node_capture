#idC
import requests, base64, re, urllib.parse
from Crypto.Cipher import AES
from datetime import datetime
import console, editor

def pkcs7_unpad(data):
    return data[:-data[-1]]

def aes_decrypt(encrypted_data, key, iv):
    cipher = AES.new(key.encode(), AES.MODE_CBC, iv.encode())
    return pkcs7_unpad(cipher.decrypt(base64.b64decode(encrypted_data))).decode('utf-8')

def fetch_and_decrypt():
    url = 'http://cnc07api.cnc07.com/api/cnc07iuapis'
    headers = {'Content-Type': 'application/json;charset=UTF-8'}
    encrypted_servers = requests.get(url, headers=headers).json().get('servers')
    return aes_decrypt(encrypted_servers, '1kv10h7t*C3f8c@$', '@$6l&bxb5n35c2w9')

def process_servers(decrypted_servers):
    ss_config_lines = re.findall(r'SS\s*=\s*ss\s*,\s*([\d\.]+)\s*,\s*(\d+)\s*,\s*encrypt-method\s*=\s*([a-zA-Z0-9\-]+)\s*,\s*password\s*=\s*([a-zA-Z0-9]+)', decrypted_servers)
    city_values = re.findall(r'"city":"(.*?)"', decrypted_servers)
    return [
        f"ss://{base64.urlsafe_b64encode(f'{method}:{password}@{ip}:{port}'.encode()).decode()}#{urllib.parse.quote(city)}"
        for (ip, port, method, password), city in zip(ss_config_lines, city_values)
    ]

def save_to_file(ss_links):
    filename = f"鹰眼加速器_{datetime.utcnow().astimezone().strftime('%Y-%m-%d')}.txt"
    with open(filename, 'w') as file:
        file.writelines(f"{link}\n" for link in ss_links)
    return filename

if __name__ == "__main__":
    ss_links = process_servers(fetch_and_decrypt())
    filename = save_to_file(ss_links)
    if console.alert("", f"一共{len(ss_links)}条节点\n已保存到{filename}", "打开文件", "取消", hide_cancel_button=True) == 1:
        editor.open_file(filename)
