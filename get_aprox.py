import requests
import json
from pandas import json_normalize
import pandas as pd
import numpy as np
import time

vagalume_key = 'e25867120a9e8faa8f139b5f716b6c4a'
url = 'https://api.vagalume.com.br/search.php'

data = pd.read_csv('./songfacts/songs.csv')
data = data[~data['name'].isna()]

data_rr = pd.read_csv('songs_lyrics.csv')

#### Getting name for aprox results
data_rr_aprox = data_rr[data_rr['res_API']=='aprox']
data_rr_aprox['name_API'] = np.nan

try:
    data_aprox_new = pd.read_csv('songs_lyrics_aprox.csv')
except:
    print('Creating new file..')
    pd.DataFrame(columns=['song_index','topic','name','artist','lyrics','res_API','status_API','name_API']).to_csv('songs_lyrics_aprox.csv')
    data_aprox_new = pd.read_csv('songs_lyrics_aprox.csv')

def get_remaining_indexes_aprox():
    complete_index = data_rr_aprox['song_index'].values.tolist()
    index_done = data_aprox_new['song_index'].values.tolist()
    index_torun = list(set(complete_index) - set(index_done))
    return index_torun

def run_request_at_aprox():
    index_aprox = get_remaining_indexes_aprox()
    for i in index_aprox:
        print(i)
        row = data_rr_aprox[data_rr_aprox['song_index']==i]
        artist = row['artist']
        song = row['name']

        r_stat=0
        while r_stat!=200:
            r = requests.get(url, params={'art': artist,'mus': song,'apikey':vagalume_key})
            r_stat = r.status_code
            if r.status_code==200:
                print ('OK!')
            else:
                print ('Ops.. delaying time')
                time.sleep(5)

        df = r.json()
        res = df['type']
        music_df = json_normalize(df['mus']).iloc[0]
        song_API = music_df['name']

        index_row = row.index.values[0]

        data_rr_aprox.at[index_row, 'name_API'] = song_API
        data_rr_aprox[data_rr_aprox['song_index']==i].to_csv('songs_lyrics_aprox.csv', mode='a', index=False, header=False)

data_rr_aprox['name_API'].count()