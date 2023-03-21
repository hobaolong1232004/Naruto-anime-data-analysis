import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import requests

def crawl_rating():
    # naruto,shippuden,boruto (params URL)
    urls_api=[18821,27282,63568]
    url='https://www.ratingraph.com/show-episodes-graph/{}/total_votes/'

    rating={'Total Votes':[],'Rating':[]}
    for param in urls_api:
        response=requests.get(url.format(param))
        if response.status_code==200:
            data=response.json()['data'][1]['data']
            for v in data:
                rating['Total Votes'].append(v['total_votes'])
                rating['Rating'].append(v['average_rating'])

    ratingdf=pd.DataFrame(rating)
    ratingdf.to_csv('rating.csv')


