import pandas as pd
import json
import numpy as np
import berserk
from requests_oauthlib import OAuth2Session
import random

client_id = 'UD1t5xkI2SUzcChd'
secret_client_id = 'DbWXT4aEJcbnx71KLptfRE7CSq7xGMbh'

session = OAuth2Session(client_id)
client = berserk.Client(session)

class Rating():
    def __init__(self, rating):
        self.rating = rating

def time_control(game_perf, data):
    perfs = {'UltraBullet':30, 'Bullet':60, 'Blitz':300, 'Rapid':600, 'Classical':1800}
    for perf in perfs:
        if perf == game_perf:
            data = data.append(pd.Series([1], index=['Perf_' + perf]))
        else:
            data = data.append(pd.Series([0], index=['Perf_' + perf]))
    data = data.append(pd.Series([perfs[game_perf]], index=['Clock_Initial']))
    data = data.append(pd.Series([0], index=['Clock_Increment']))

    return data

def rh_ratings(player, color, data, game_perf):
    perfs = ['UltraBullet', 'Bullet', 'Blitz', 'Rapid', 'Classical', 'Correspondence']
    #rh = client.users.get_rating_history(player)
    rh = []

    for perf in ['UltraBullet', 'Bullet', 'Blitz', 'Rapid', 'Classical', 'Correspondence']:
        rh.append({'name':perf, 'points':[Rating(random.randint(1400,1600)) for i in range(random.randint(1,10))]})

    for index, rh_perf in enumerate([perf['name'] for perf in rh]):
        if rh_perf in perfs and len(rh[index]['points']) > 0:
            final_rating = rh[index]['points'][-1]
            data = data.append(pd.Series([final_rating.rating], index=[color + '_' + rh_perf + '_Rating']))
            if rh_perf == game_perf:
                data = data.append(pd.Series([final_rating.rating], index=[color + '_Rating']))
        elif rh_perf in perfs and len(rh[index]['points']) == 0:
            data = data.append(pd.Series([0], index=[color + '_' + rh_perf + '_Rating']))

    return data

def rating_difference(perf, data):
    white_rating_columns = [column for column in data.index if ('Rating' in column) and ('White' in column)]
    black_rating_columns = [column for column in data.index if ('Rating' in column) and ('Black' in column)]
    data['Rating_Difference'] = data['White_' + perf + '_Rating'] - data['Black_' + perf + '_Rating']
    for white_column in white_rating_columns:
        black_column = white_column.replace('White', 'Black')
        data[white_column[6:] + '_Difference'] = data[white_column]-data[black_column]
    data.drop(labels=white_rating_columns+black_rating_columns, inplace=True)

def transform(data, white, black, evaluation, eval_mate, white_clock, black_clock, perf):
    data = rh_ratings(white, 'White', data, perf)
    data = rh_ratings(black, 'Black', data, perf)
    data = time_control(perf, data)

    data = data.append(pd.Series([int(white_clock)], index=['White_Clock']))
    data = data.append(pd.Series([int(black_clock)], index=['Black_Clock']))

    data = data.append(pd.Series([float(evaluation)], index=['Eval']))
    data = data.append(pd.Series([eval(eval_mate)], index=['Is_Mate']))

    column_order = ['Perf_Blitz', 'Perf_Bullet', 'Perf_Classical', 'Perf_Rapid',
        'Perf_UltraBullet', 'White_Rating', 'White_UltraBullet_Rating',
        'White_Bullet_Rating', 'White_Blitz_Rating', 'White_Rapid_Rating',
       'White_Classical_Rating', 'White_Correspondence_Rating', 'Black_Rating',
        'Black_UltraBullet_Rating', 'Black_Bullet_Rating', 'Black_Blitz_Rating',
       'Black_Rapid_Rating', 'Black_Classical_Rating', 'Black_Correspondence_Rating',
       'Clock_Initial', 'Clock_Increment', 'White_Clock', 'Black_Clock', 'Eval', 'Is_Mate']

    import ctypes
    print (ctypes.sizeof(ctypes.c_voidp))
    data = data[column_order]

    return data
