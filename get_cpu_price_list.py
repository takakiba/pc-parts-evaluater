import requests
from bs4 import BeautifulSoup
import time
import pandas as pd
import datetime

target_cpu_socket = ['LGA1700', 'LGA1200', 'Socket AM5', 'Socket AM4', 'Socket sTR5', 'Socket sWRX8']
csv_database = './CPU_prices.csv'


if __name__ == '__main__':

    ### getting the number of items in the target category in kakaku.com
    url = 'https://kakaku.com/pc/cpu/itemlist.aspx'
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'lxml')
    n_item = int(soup.find(class_="result").span.text)
    # print(n_item)

    ### define the page settings
    n_per_page = 40
    pages = n_item // n_per_page + 1
    # print(pages)

    print('Found {0} products, {1} pages to read'.format(n_item, pages))

    ### url common in multiple pages
    page_url_base = 'https://kakaku.com/pc/cpu/itemlist.aspx?pdf_pg='

    res = []

    ### loop for page
    for i in range(1, pages+1):
        page_url = page_url_base + '{0:d}'.format(i)
        print('Page {0:3d} : {1}'.format(i, page_url))
        res.append(requests.get(page_url))
        time.sleep(5)

    list_product = []
    list_chip    = []
    list_price   = []
    list_vender  = []
    list_socket  = []

    ### get the data for price and others
    for i, r in enumerate(res):
        soup = BeautifulSoup(r.text, 'lxml')
        elems = soup.find_all(class_='tr-border')
        # print(len(elems))

        # for k, td in enumerate(chip):
        #     print('{0:3d} : {1}'.format(k, td.text))
        '''
        index for td meta data
        0 : blank
        1 : price
        2 : rank1
        3 : rank2
        4 : review score
        5 : num of review
        6 : registration date
        7 : sale date
        8 : chip
        9 : clock freq
        10: socket
        11: num of cores
        12: num of threads
        13: blank
        '''
        itd_chip   = 8
        itd_socket = 10

        n_left_item = n_item - n_per_page * i
        n_item_in_page = min(n_per_page, n_left_item)

        for n in range(n_item_in_page):
            vender = elems[n*3+2].find('span').text
            # print(vender)

            product = elems[n*3+2].find('a').text.split('\u3000')[1]
            # print(product)

            chip = elems[n*3+3].find_all('td')[itd_chip].text
            # print(chip)

            socket = elems[n*3+3].find_all('td')[itd_socket].text
            # print(socket)

            price = int(elems[n*3+3].find(class_='pryen').text.replace(',', '')[1:])
            # print(price)

            # print('{0:24} {1:48} {2:8d}'.format(product, chip, price))

            if socket in target_cpu_socket:
                list_vender.append(vender)
                list_product.append(product)
                list_chip.append(chip)
                list_socket.append(socket)
                list_price.append(price)

    df = pd.DataFrame({
        'Product': list_product,
        'Chip'   : list_chip,
        'Vender' : list_vender,
        'Socket' : list_socket,
        'Price'  : list_price
    })
    df['Vender'] = df['Vender'].str.strip()
    df['Vender'] = df['Vender'].str.replace('インテル', 'Intel')
    df['Product'] = df['Product'].str.replace('バルク', 'BULK')
    df.sort_values(['Vender', 'Socket', 'Price'], ascending=False, inplace=True, ignore_index=True)
    print(df)
    df.to_csv(csv_database)

