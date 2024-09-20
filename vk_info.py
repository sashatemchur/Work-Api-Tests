import requests, json
import csv, time

info_user = [['Full name', 'Date of birth', 'Family status', 'Phone number', 'Interests', 'Friends', 'Last online'], []]
input_id = str(input("Вкажіть поселання на vk:"))
if 'id' in input_id:
    index = input_id.index('id')
    user = input_id[index+2:]
else:
    index = input_id.index('m/')
    user = input_id[index+2:]

token = "d5c4489dd5c4489dd5c4489d96d6d31a7cdd5c4d5c4489db0178c4b6ebdedc3fa35dc21"
response = requests.post(f"https://api.vk.com/method/users.get?user_ids={user}&fields=bdate,counters,interests,contacts,last_seen,relation&access_token={token}&v=5.131 HTTP/1.1")

try:
    all_info = json.loads(response.text)['response'][0]
except:
    all_info = json.loads(response.text)['response']

try:
    if all_info['relation'] == 0:
        relation = 'Не вказано'
    elif all_info['relation'] == 1:
        relation = 'Не одружений/незаміжня'
    elif all_info['relation'] == 2:
        relation = 'Є друг/є подруга'
    elif all_info['relation'] == 3:
        relation = 'Заручений/заручена'
    elif all_info['relation'] == 4:
        relation = 'Одружений/одружена'
    elif all_info['relation'] == 5:
        relation = 'Все важко'
    elif all_info['relation'] == 6:
        relation = 'В активному пошуку'
    elif all_info['relation'] == 7:
        relation = 'Закоханий/закохана'
    elif all_info['relation'] == 8:
        relation = 'У цивільному шлюбі'
except:
    relation = 'Не вказано'     

try:
    number_phone = all_info['mobile_phone']  
except:
    number_phone = ''

try:
    interest = all_info['interests']
except:
    interest = ''

try:
    bdate = all_info['bdate']
except:
    bdate = ''

try:
    friends = all_info['counters']['clips_followers']-all_info['counters']['followers']
except:
    friends = 'Неможливо визначити, закритий акаунт'

time = str(list(reversed(time.gmtime(all_info['last_seen']['time'])[:5]))).replace(',', '.').replace('[', '').replace(']', '').replace(' ', '')
info_user[1].append(all_info['first_name'] + ' ' + all_info['last_name'])
info_user[1].append(bdate)
info_user[1].append(relation)
info_user[1].append(number_phone)
info_user[1].append(interest)
info_user[1].append(friends)
info_user[1].append(time)

with open('vk.csv', 'w') as data:
    writer = csv.writer(data)
    for row in info_user:
        writer.writerow(row)

