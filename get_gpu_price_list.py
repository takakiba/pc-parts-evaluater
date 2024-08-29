import requests
from bs4 import BeautifulSoup
import time
import pandas as pd
import datetime

csv_database = './GPU_prices.csv'


if __name__ == '__main__':

    ### getting the number of items in the target category in kakaku.com
    url = 'https://kakaku.com/pc/videocard/itemlist.aspx?pdf_Spec101=1,11,12'
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
    page_url_base = 'https://kakaku.com/pc/videocard/itemlist.aspx?pdf_Spec101=1,11,12&pdf_pg='

    res = []

    ### loop for page
    for i in range(1, pages+1):
        page_url = page_url_base + '{0:d}'.format(i)
        print('Page {0:3d} : {1}'.format(i, page_url))
        res.append(requests.get(page_url))
        time.sleep(5)

    list_product      = []
    list_chip         = []
    list_chip_vender  = []
    list_price        = []
    list_manufacturer = []

    ### get the data for price and others
    for i, r in enumerate(res):
        soup = BeautifulSoup(r.text, 'lxml')
        elems = soup.find_all(class_='tr-border')
        # print(len(elems))

        # for k, td in enumerate(elems):
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
        8 : interface
        9 : chip
        10: memory
        11: output plugs
        14: blank
        '''
        itd_chip   = 9
        # itd_socket = 10

        n_left_item = n_item - n_per_page * i
        n_item_in_page = min(n_per_page, n_left_item)

        for n in range(n_item_in_page):
            manufacturer = elems[n*3+2].find('span').get_text().strip()
            # print(vender)

            product = elems[n*3+2].find('a').get_text().split('\u3000')[1]
            # print(product)

            ### separate chip vender info from chip name
            chip = elems[n*3+3].find_all('td')[itd_chip].get_text()
            chip = chip.replace('NVIDIA', 'NVIDIA ')
            chip = chip.replace('AMD', 'AMD ')
            chip = chip.replace('Intel', 'Intel ')
            # print(chip)

            chip_vender = chip.split()[0]

            price = int(elems[n*3+3].find(class_='pryen').get_text().replace(',', '')[1:])
            # print(price)

            # print('{0:24} {1:48} {2:8d}'.format(product, chip, price))

            list_manufacturer.append(manufacturer)
            list_product.append(product)
            list_chip.append(chip)
            list_chip_vender.append(chip_vender)
            list_price.append(price)


    ### dataframe to save gpu price data
    df = pd.DataFrame({
        'Product'      : list_product,
        'Chip'         : list_chip,
        'Chip vender'  : list_chip_vender,
        'Manufacturer' : list_manufacturer,
        'Price'        : list_price
    })
    df.sort_values(['Chip vender', 'Chip', 'Price'], ascending=False, inplace=True, ignore_index=True)
    print(df)
    df.to_csv(csv_database)


