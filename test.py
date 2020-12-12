import os
import csv
import requests
from bs4 import BeautifulSoup
from unicodedata import normalize

os.system("clear")
alba_url = "http://www.alba.co.kr"

res = requests.get(alba_url)
soup = BeautifulSoup(res.text, 'html.parser')
brand_list = []


def get_brand(box):
    inner_list = box.find_all('a')[1:]

    for inner in inner_list:
        name = inner.find(
            'span', {"class": "company"}).find('strong').get_text()
        url = inner['href']
        brand_list.append({'name': name, 'url': url, 'info': []})


def get_hire_info_url(brand):
    res = requests.get(brand['url'])
    soup = BeautifulSoup(res.text, 'html.parser')
    # check_page
    page_size = soup.find(
        'p', {"class": "jobCount"}).find('strong').get_text()
    return brand['url'] + f"/job/brand/?pagesize={page_size}"


def get_hire_info(hire):
    try:
        hire_info = hire.find_all('td')

        place = normalize('NFKD', hire_info[0].get_text())
        title = hire_info[1].find('a').find(
            'span', {"class": "company"}).get_text()
        time = hire_info[2].get_text()
        pay = hire_info[3].find('span', {"class": "payIcon"}).get_text(
        ) + hire_info[3].find("span", {"class": "number"}).get_text()
        date = hire_info[4].get_text()

        return [place, title,  time,  pay,  date]
    except:
        return []


def save_to_file(brand):
    file = open(f"test/{brand['name']}.csv", "w")
    writer = csv.writer(file)
    writer.writerow(["place", "title", "time", "pay", "date"])
    for info in brand['info']:
        writer.writerow(info)
    return


box_list = soup.find('div', {"id": "MainSuperBrand"}).find(
    'ul', {"class": "goodsBox"}).find_all('li')


for box in box_list:
    get_brand(box)

for brand in brand_list:

    try:
        url = get_hire_info_url(brand)
        res = requests.get(url)
        soup = BeautifulSoup(res.text, 'html.parser')

        try:
            hire_list = soup.find('div', {"id": "NormalInfo"}).find(
                'table').find('tbody').find_all('tr', {"class": ""})
        except:
            hire_list = []

        for hire in hire_list:
            brand['info'].append(get_hire_info(hire))

        save_to_file(brand)
    except:
        pass
