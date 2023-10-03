# python3 -m venv name_venv
# source name_venv/bin/activate
# pip install --upgrade pip

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

try:
    data_rr = pd.read_csv('songs_lyrics.csv')
except:
    print('Creating new file..')
    pd.DataFrame(columns=['song_index','topic','name','artist','lyrics','res_API','status_API']).to_csv('songs_lyrics.csv')
    data_rr = pd.read_csv('songs_lyrics.csv')

def get_remaining_indexes():
    complete_index = list(range(0,data.shape[0]))
    index_done = data_rr['song_index'].values.tolist()
    index_torun = list(set(complete_index) - set(index_done))
    return index_torun

def run_request_at():
    index_torun = get_remaining_indexes()
    for i in index_torun:
        print(i)
        row = data.iloc[i]
        song = row['name'].strip()
        artist = row['artist'].strip()
        topic = row['topic']
        if song=='' or artist=='':
            print('artist or song is null')
            continue
        try:
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
            if res=='notfound' or res=='song_notfound':
                print('not found')
                text='notfound in API'
            else: 
                music_df = json_normalize(df['mus']).iloc[0]
                text = music_df['text']
            final_df = pd.DataFrame({'index':[i],'song_index':[i],
                                     'topic':[topic],
                                     'name':[song],
                                     'artist':[artist],
                                     'lyrics': text,
                                     'res_API': res,
                                     'status_API': r_stat
                                     })
            final_df.to_csv('songs_lyrics.csv', mode='a', index=False, header=False)
        except Exception as e: 
            print(e)