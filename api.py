from pprint import pprint
import requests
import time

# Глобальные переменные
SECRET_KEY = 'L3PWXGvpxveaZUMzbseyh5d4MKQBPjUEo9WvryzXOwLkSSplhq5T66zKNssl4c8Q'
INTEGRATION_ID = '2f7cf93c-55a0-4e97-bc24-c0ed8740e9ad'
ACCESS_TOKEN = ''
REFRESH_TOKEN = ''
URL = 'https://vlavashov.amocrm.ru/'


# Получаем токены из файлы в переменные
def take_tokens():
    global ACCESS_TOKEN, REFRESH_TOKEN
    with open('data.txt', 'r') as file:
        lines = file.readlines()
        ACCESS_TOKEN = lines[0][:-1]
        REFRESH_TOKEN = lines[1][:-1]


# Проверяем жизненый цикл access токена и обновляем его если нужно
def check_time():
    with open('data.txt', 'r') as file:
        lines = file.readlines()
        token_time = int(time.time() - float(lines[2][:-1]))
        print(token_time)
    if token_time > 86400:
        lines[0] = update_token() + '\n'
        lines[2] = str(time.time())
        print(lines)
        with open('data.txt', 'w') as file:
            file.writelines(lines)
    take_tokens()


# Получаем access/refresh tokens
def get_tokens():
    response = requests.post(url=f'{URL}oauth2/access_token', data={
        "client_id": INTEGRATION_ID,
        "client_secret": SECRET_KEY,
        "grant_type": "authorization_code",
        "code": 'def502002cad3b8fac0aac575d044ea7908083ae2d8beb9b1f375574226cd52a0215ad6733b7069dc72b99163cc957577f6ac8c519eb370a3827b5f63dd578c6f0c04b8df2f7058150aac6b90a1aabc59d3a173a9a81b7f1e05306f5386cd54f071af6255d3467d487e9ed646899cfcd205b2e1665f87180fff439ce9584ba39c5ef153309daa12b0f034d31e8616cdc4d3a91d98919e966aa36c9d082f71a0112ad895a16c8c924ff228714c6d02d348e3590fa6560da1583a8b6d9aa736860da922f69210542f6845c7243e08e42ce7bb75ea49ca91852bd6f20fc503cac313fa54d3a6f3f851129b1958fdaf7c8b7b4a6f65481f810b1b08aee3e6bf85ec0e8926fbd9587c874199d204b5461240490113f3de01649fa9c010d2307d7265778c33644ad3a8d573d5435907b4ffc624994ca1f03cc60e4c5e48f509c1ef9428af2b473581b77a2c9b41806267bfe2d3e586c06aff4a1f626440b1b5b7e276163647a300a9e93512e4bee2d787f2bf159237f0e78e0c4c369719dd903ace9269ecdc3113eae23565e915e38c815c27291211351c917f87881e8deb48ee746f81a7b09d64d997eb09987584248ddcd5711149a905d60fc2e6fe6e2a51ca756145d83232f5772395a175099d988036e2055fa9cd9e63686b9831f3bce69d296f4eea60112ccf0ab8bf6f00cca9694584b5d5a0e9adc435de5b3',
        "redirect_uri": "http://johnflyadich.pythonanywhere.com/"
    })
    data = response.json()
    print(data)
    return data


# Обновляем access token
def update_token():
    response = requests.post(url=f'{URL}oauth2/access_token', data={
        "client_id": INTEGRATION_ID,
        "client_secret": SECRET_KEY,
        "grant_type": "refresh_token",
        "refresh_token": REFRESH_TOKEN,
        "redirect_uri": "http://johnflyadich.pythonanywhere.com/"
    })
    data = response.json()
    return data['access_token']




# Ищем контакт по номеру
def get_contacts_by_phone(phone=None):
    try:
        params = {'query': phone}
        response = requests.get(url=f'{URL}api/v4/contacts', headers={
                                'Authorization': f'Bearer {ACCESS_TOKEN}'}, params=params)
        data = response.json()['_embedded']['contacts'][0]
        return data['id']
    except:
        return
    

# Ищем контакт по email
def get_contacts_by_mail(mail=None):
    try:
        params = {'query': mail}
        response = requests.get(url=f'{URL}api/v4/contacts', headers={
                                'Authorization': f'Bearer {ACCESS_TOKEN}'}, params=params)
        data = response.json()['_embedded']['contacts'][0]
        return data['id']
    except:
        return

# Редактируем контакт


def update_contact(**kwargs):
    access_token = ACCESS_TOKEN
    params = {'name': kwargs['name'],
              'custom_fields_values':
              [{'field_code': 'PHONE', 'values': [{'value': kwargs['phone']}]},
               {'field_code': 'EMAIL', 'values': [{'value': kwargs['mail']}]}]}
    response = requests.patch(url=f'{URL}api/v4/contacts/{kwargs["contact_id"]}', headers={
                              'Authorization': f'Bearer {access_token}'}, json=params)
    return True


# Создаём контакт
def create_contact(**kwargs):
    data = [
        {
            "name": kwargs['name'],
            "custom_fields_values": [
                {
                    "field_code": 'PHONE',
                    "values": [
                        {
                            "value": kwargs['phone']
                        }
                    ]
                },
                {
                    "field_code": 'EMAIL',
                    "values": [
                        {
                            "value": kwargs['mail']
                        }
                    ]
                }
            ]
        }
    ]
    response = requests.post(url=f'{URL}api/v4/contacts', headers={
        'Authorization': f'Bearer {ACCESS_TOKEN}'}, json=data)
    data = response.json()
    print(data)
    return data['_embedded']['contacts'][0]['id']


# Создаём лид
def create_lead(contact_id=None):
    data = [{
        "_embedded": {
            "contacts": [
                {
                    "id": contact_id
                }
            ]
        }
    }]
    response = requests.post(url=f'{URL}api/v4/leads', headers={
        'Authorization': f'Bearer {ACCESS_TOKEN}'}, json=data)
    return True
