import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import wordcloud
import requests
from bs4 import BeautifulSoup


def crawl_info():
    # Scrape data from the Naruto Wiki website
    url = 'https://naruto.fandom.com/wiki/List_of_Animated_Media'
    html = requests.get(url).content
    soup = BeautifulSoup(html, 'html.parser')


    # Find all episode titles and descriptions
    list_episode=soup.find_all('table',{'class':'box table coloured bordered innerbordered style-basic fill-horiz'})[:3]
    categorized=['naruto','shippuden','Boruto']

    cleaned_titles=[]
    cleaned_episode=[]
    cleaned_airdate=[]
    cleaned_categorized=[]
    cleaned_arc=[]
    cleaned_characters=[]

    # parse add arc and characters appearance each episode
    def extract_character(description_website): #function
        character=[]
        try:
            arc=description_website.find('div',{'class':'pi-item pi-data pi-item-spacing pi-border-color','data-source':'arc'}).text.strip().replace("\"",'').replace('Arc\n','')
        except:
            arc=None
        character_apperance = description_website.find('table',
                                                       {'class': 'wikitable fill-horiz cell-align-center'}).find_all('tr')[2:]
        for c in character_apperance:
            character.append(c.find('a',href=True).text)
        return arc,character

    #  clean data and add data
    for i in range(len(categorized)): # loop through 3 categorized
        parse_section=list_episode[i]
        episode = parse_section.find_all('th')[4:]
        info_episode = parse_section.find_all('td')
        list_desciption = parse_section.find_all('a', href=True)

        # add info
        for v in range(0, len(info_episode), 3):
            cleaned_airdate.append(info_episode[v + 1].text.strip())
            cleaned_titles.append(info_episode[v].text.strip().replace("\"",''))

        # add episode,categorized
        for n in range(len(episode)):
            cleaned_episode.append(episode[n].text.strip())
            cleaned_categorized.append(categorized[i])
            # arc
            newurl=list_desciption[n]['href']
            description_website = BeautifulSoup(requests.get('https://naruto.fandom.com/' + newurl).content,
                                                'html.parser')
            arc, character = extract_character(description_website)
            cleaned_arc.append(arc)
            cleaned_characters.append(character)



    data={'Episode':cleaned_episode,'Title':cleaned_titles,'Airdate':cleaned_airdate,
          'Character appearance':cleaned_characters,'Arc':cleaned_arc,'Categorized':cleaned_categorized}
    df=pd.DataFrame.from_dict(data)
    df.to_csv('Naruto.csv',index=True)

    # character appearance
