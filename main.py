import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from crawl_info import  crawl_info
from crawl_rating import crawl_rating


# crawl_info()
# crawl_rating()

df=pd.read_csv('Naruto.csv')
df_rate=pd.read_csv('rating.csv')

# start analysis
#Which are the most popular episodes of Naruto-Boruto series ( highest rating)
df_merge=df_rate.merge(df,left_index=True,right_index=True)
df_highestrating=df_merge[['Title','Total Votes','Rating','Categorized']]
df_highestrating=df_highestrating.sort_values(by='Rating',ascending=False).head(10)
df_highestrating.to_csv('highest.csv')
title=df_highestrating['Title'].tolist() # change df to list of title
categorized=df_highestrating['Categorized'].tolist()

rank=[1,2,3,4,5,6,7,8,9,10]
#horizon bar plot
bars = plt.barh(rank,df_highestrating['Rating'],tick_label=rank) # force tick label to show full number on y axis
for  i,bar in enumerate(bars):
    width = bar.get_width()
    label_y = bar.get_y() + bar.get_height() / 2
    plt.text(0.1, label_y, s=title[i]+f' ({categorized[i]})') # add  text in the bar for title
    plt.text(width, label_y, s=f'{width}') # display score

plt.xlabel('Rating')
plt.ylabel('Rank and Episode Title')
plt.title('Top 10 Most Popular Episodes of Naruto')
plt.show()

#Total longest arc from each series from longest to shortest(naruto to boruto)
df_longestarc=df_merge[['Arc','Categorized','Episode']]
df_longestarc=df_longestarc.groupby(as_index=False,by=['Arc','Categorized']).count() # groupby with as_index=False not delete columns
df_longestarc.columns=df_longestarc.columns.str.replace('Episode','Total episodes')# change column name from aggerate func
# take longest arc from each series
naruto=df_longestarc[df_longestarc.Categorized=='naruto'].sort_values(by='Total episodes',ascending=False).head(1)
shippuden=df_longestarc[df_longestarc.Categorized=='shippuden'].sort_values(by='Total episodes',ascending=False).head(1)
boruto=df_longestarc[df_longestarc.Categorized=='Boruto'].sort_values(by='Total episodes',ascending=False).head(1)
df_longestarc=pd.concat([naruto,shippuden,boruto]).sort_values(by='Total episodes',ascending=False)
x=df_longestarc['Arc']
y=df_longestarc['Total episodes']
bar_colors = ['tab:red', 'tab:blue', 'tab:orange']
categorized=['Naruto','Shippuden','Boruto']
fig, ax = plt.subplots()
ax.bar(x, y, label=categorized, color=bar_colors)
ax.set_ylabel('Total episodes')
ax.set_title('Arc name')
ax.legend(title='Series type')
plt.xticks(rotation=30)
plt.tight_layout() # to capture all the text
plt.show()

#Which characters appear most frequently in Naruto?
# Create a new DataFrame with one row per character
characters = []
df_character=df['Character appearance'].apply(eval) # convert str back to list

for i in range(len(df)):
    for character in df_character[i]:
        characters.append({'Title': df.loc[i, 'Title'], 'Character': character})
df_characters = pd.DataFrame(characters)
df_characters.to_csv('Character_appearance.csv')
df_characters=df_characters['Character'].value_counts().head(10)
# plot pie chart
def absolute_value(val): # funct to display number on pie chart
    a  = int(np.round(val/100.*df_characters.values.sum(), 0))
    return a

plt.pie(df_characters.values,labels=df_characters.index,startangle=90,autopct=absolute_value)
plt.title('Top 10 Characters with the Most Appearances in Naruto')
plt.show()