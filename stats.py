from urlextract import URLExtract
import pandas as pd
from collections import Counter
from wordcloud import WordCloud
import re

import emoji

extract = URLExtract()

def fetchstats(selected_user,df):
    if selected_user != 'Overall':
        df=df[df['User'] == selected_user]
    
    num_messages=df.shape[0]
    words=[]
    for message in df['Message']:
        words.extend(message.split())
    
    mediaommitted= df[df['Message'] == '<Media omitted>']
    
    links = []
    for message in df['Message']:
        links.extend(extract.find_urls(message))

    return num_messages, len(words), mediaommitted.shape[0], len(links) 

def fetchbusyuser(df):
    df=df[df['User']!='Group Notification']
    count=df['User'].value_counts().head()
    
    newdf=pd.DataFrame((df['User'].value_counts()/df.shape[0])*100)
    return count, newdf

def createwordcloud(selected_user,df):
    
    if selected_user!='Overall':
        df=df[df['User'] == selected_user]
     
    wc=WordCloud(width=400, height=350, min_font_size=3, background_color='white', max_font_size=200, colormap='viridis')    
    
    df_wc=wc.generate(df['Message'].str.cat(sep=" "))
    
    return df_wc

def getcommonwords(selected_user,df):
    file= open('stop_hinglish.txt','r')
    stopwords=file.read()
    stopwords=stopwords.split('\n')
    
    if selected_user != 'Overall':
        df=df[df['User']==selected_user]
    
    temp=df[(df['User']!='Group Notification') | 
            (df['User']!='<Media omitted')]
    
    words=[]
    
    for message in temp['Message']:
        for word in message.lower().split():
            if word not in stopwords:
                words.append(word)
    
    mostcommon=pd.DataFrame(Counter(words).most_common(20))
    return mostcommon

def getemojistats(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['User'] == selected_user]
    
    emojis = []
    emoji_pattern = re.compile("["
                               u"\U0001F600-\U0001F64F"  # emoticons
                               u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                               u"\U0001F680-\U0001F6FF"  # transport & map symbols
                               u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                               u"\U00002702-\U000027B0"
                               u"\U000024C2-\U0001F251"
                               "]+", flags=re.UNICODE)
    
    for message in df['Message']:
        emojis.extend(emoji_pattern.findall(message))
    
    emojidf = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))
    return emojidf
  
def monthtimeline(selected_user,df):
    if selected_user != 'Overall':
        df=df[df['User']==selected_user]
    
    temp=df.groupby(['Year', 'Month_num', 'Month']).count()['Message'].reset_index()
    
    time=[]
    for i in range(temp.shape[0]):
        time.append(temp['Month'][i]+"-"+str(temp['Year'][i]))
    
    temp['Time'] = time
    return temp

def monthactivitymap(selected_user, df):

    if selected_user != 'Overall':
        df = df[df['User'] == selected_user]

    return df['Month'].value_counts()


def weekactivitymap(selected_user, df):

    if selected_user != 'Overall':
        df = df[df['User'] == selected_user]

    return df['Day_name'].value_counts()
       
                