#idC
import requests, base64, re, urllib.parse
import pyaes

def pkcs7_unpad(data):
    return data[:-data[-1]]

def aes_decrypt(encrypted_data, key, iv):
    cipher = pyaes.Decrypter(pyaes.AESModeOfOperationCBC(key.encode(), iv.encode()))
    decrypted_data = cipher.feed(base64.b64decode(encrypted_data)) + cipher.feed()
    return pkcs7_unpad(decrypted_data).decode('utf-8')

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
    filename = "鹰眼加速器.txt"
    with open(filename, 'w') as file:
        file.writelines(f"{link}\n" for link in ss_links)
    return filename

if __name__ == "__main__":
    ss_links = process_servers(fetch_and_decrypt())
    filename = save_to_file(ss_links)
    print("\n".join(ss_links))
    print(f"节点总数: {len(ss_links)}")
    print(f"已保存到{filename}")
