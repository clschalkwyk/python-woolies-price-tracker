import json
from datetime import datetime
from os.path import exists
import requests
from bs4 import BeautifulSoup

meat_html = 'woolies_meat.html'
url ='https://www.woolworths.co.za'

if not exists(meat_html):
    res = requests.get(url)
    # print(res.text)

    soup = BeautifulSoup(res.text, 'html.parser')
    found_a = soup.find_all('a', class_="main-nav__link")
    for a in found_a:
        # print(a.text.find('Food'))
        # if a.text.find('dept/Food') > -1:
        if str(a.attrs.get('href')).find('dept/Food') > -1:
            # print(a.attrs.get('href'))
            food_url = '{}{}'.format(url, a.attrs.get('href'))
            food_dept = requests.get(food_url)
            food_dept_soup = BeautifulSoup(food_dept.text, 'html.parser')
            food_dept_urls = food_dept_soup.find_all('a')

            meat_url = ''
            for urldept in food_dept_urls:
                if urldept.attrs.get('href').find('cat/Food/Meat-Poultry-Fish/_/') > -1:
                    meat_url = '{}{}'.format(url,  urldept.attrs.get('href'))


    meat_page = requests.get(meat_url)
    with open(meat_html,'w') as fp:
        fp.write(meat_page.text)
        fp.close()

with open(meat_html,'r') as fp:
    txt = fp.read()
    sp = BeautifulSoup(txt, 'html.parser')
    scripts = sp.find_all('script')
    script = [x for x in scripts if x.text.find('window.__INITIAL_STATE__') > -1].pop()
    js = json.loads(script.text.split('window.__INITIAL_STATE__ =')[1])
    products = js['clp']['SLPData'][0]['mainContent'][0]['contents'][0]['records']
    prices = []
    for prod in products:
        prices.append({
            "onPromotion":prod['attributes'].get('OnPromotion'),
            "name": prod['attributes'].get('p_displayName'),
            "unitPrice": prod['startingPrice'].get('p_pl00_kilogramPrice'),
            "price":prod['startingPrice'].get('p_pl00')
        })
    # print(js['clp']['SLPData']['mainContent'])
    # print(script.split('window.__INITIAL_STATE__ ='))

    out_file = open('prices_{}.json'.format(datetime.now().strftime("%Y%m%d_%H%M%S")),'w')
    json.dump(prices, out_file)
    print(json.dumps(prices))