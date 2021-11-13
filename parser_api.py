from fake_headers import Headers
import requests
import csv
import json


header = Headers( browser="chrome", os="win",  headers=True  )


# Получение дааных и сохранение JSON
def main():
    for i in range(30, 600 , 30):
        with open(f'data/data_{i}.json', 'wb') as f:
            data = get_data_from_url(i)
            f.write(data)

    edit_to_scv()

def edit_to_scv():
    with open('lego.csv', 'w') as file:
        field = ['ID', 'description', 'prise', 'region' ,'promo_price' , 'url']
        w = csv.DictWriter(file, fieldnames=field)
        w.writeheader()

        for n in range(30, 600 , 30):
            with open(f'data/data_{n}.json') as f:
                templates = json.load(f)
                
                for i in range(len(templates['items'])):
                    # Проверка есть ли продукт в МСК и СПБ
                    tem =templates['items'][i]['available']['offline']['region_iso_codes']
                    if any(x in tem for x in ['RU-MOW','RU-SPE']):
                        w.writerow({
                            'ID': templates['items'][i]['id'],
                            'description': templates['items'][i]['title'],
                            'prise':templates['items'][i]['price']['price'], 
                            'region':[ i for i in ['RU-MOW','RU-SPE'] if i in tem] ,
                            'promo_price':templates['items'][i]['old_price']['price'] if templates['items'][i]['old_price'] else "-" ,
                            'url':templates['items'][i]['link']['web_url']
                            })


proxie_ht = [
        {'https':'195.201.52.68:5566'},
        {'https':'51.81.35.113:8080'},
        {'https':'201.95.211.76:8081'},
        {'https':'168.196.124.116:999'},
        {'https':'34.125.195.142:8080'},
        {'https':'181.143.224.45:999'},
        {'https':'34.92.163.25:3128'},
        {'https':'85.195.104.71:80'},
        {'https':'46.4.91.36:3128'},
        {'https':'108.160.130.33:3128'},
        {'https':'165.16.66.217:8080'},
        {'https':'188.165.59.127:3128'},
        {'https':'189.203.147.84:999'},
        {'https':'200.122.226.43:999'},
        {'https':'148.255.243.123:999'},
        {'https':'51.195.76.214:3128'},
        {'https':'212.237.16.60:3128'},
        {'https':'136.243.34.226:3128'},
        {'https':'152.0.226.164:999'},
        {'https':'211.110.60.22:3128'},
        {'https':'198.144.149.82:3128'},
        {'https':'38.101.122.211:8080'},
        {'https':'14.225.192.18:8080'},
    ]    

# Генератор получения Proxie 
def proxie_range(proxie_ht):
    for val  in proxie_ht:
        yield val
proxie_init = proxie_range(proxie_ht)


# Получение JSON
def get_data_from_url(i):
    try:
        url =f'https://api.detmir.ru/v2/products?filter=categories[].alias:lego;promo:false;withregion:RU-MOW&expand=meta.facet.ages.adults,meta.facet.gender.adults&meta=*&limit=30&offset={i}&sort=popularity:desc'
        params = {'meta': 'long', 'limit': '1'}   
        req = requests.get(url, params = params , headers=header.generate(), proxies=next(proxie_init) )           
        return req.content
    except:
        get_data_from_url(i)

if __name__ == '__main__':
	main()
    