import requests
from bs4 import BeautifulSoup
import pandas as pd

save_csv = 'GPU_3Dmark_scores.csv'


def get_passmark_scores(output_csv):
    ### original passmark data page url
    html = 'https://benchmarks.ul.com/compare/best-gpus?amount=0&sortBy=SCORE&reverseOrder=true&types=DESKTOP&minRating=0'

    ### retrieve html text information
    req = requests.get(html)
    req.encoding = req.apparent_encoding

    # print(req.text)

    ### convert to bueatiful soup object
    bsObj = BeautifulSoup(req.text, "html.parser")

    ### obtain products
    products_cand = bsObj.find_all('a', {'class': 'OneLinkNoTx'})
    products = [p.get_text() for p in products_cand]

    ### obtain score list
    score_cand = bsObj.find_all('div', {'class': 'bar-holder performance'})
    scores = [int(s.get_text()) for s in score_cand]

    # print(len(products), len(scores))
    # for p, s in zip(products, scores):
    #     print(p, s)

    ### creating pandas dataframe for saving
    df = pd.DataFrame({'GPU name':products, '3DMark score': scores})
    df.to_csv(output_csv)


if __name__ == '__main__':
    get_passmark_scores(save_csv)

