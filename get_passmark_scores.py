import requests
from bs4 import BeautifulSoup
import pandas as pd


save_csv = 'CPU_passmark_scores.csv'


def get_passmark_scores(output_csv):
    ### original passmark data page url
    html = 'https://www.cpubenchmark.net/high_end_cpus.html'

    ### retrieve html text information
    req = requests.get(html)
    req.encoding = req.apparent_encoding

    # print(req.text)

    ### convert to bueatiful soup object
    bsObj = BeautifulSoup(req.text, "html.parser")

    ### obtain list elements
    lists = bsObj.find_all('li')

    ### filter the elements above for product entry
    element = [l for l in lists if 'prdname' in str(l)]

    ### get product and score lists
    products = [e.find("span", {"class": "prdname"}).get_text() for e in element if 'mark-neww' in str(e)]
    scores = [int(e.find("span", {"class": "mark-neww"}).get_text().replace(',','')) for e in element if 'mark-neww' in str(e)]

    ### creating pandas dataframe for saving
    df = pd.DataFrame({'CPU name':products, 'Passmark score': scores})

    df['Chip'] = df['CPU name'].str.replace('-', ' ')
    df['Chip'] = [n.split('@')[0].strip() for n in df['Chip']]

    df.to_csv(output_csv)


if __name__ == '__main__':
    get_passmark_scores(save_csv)

