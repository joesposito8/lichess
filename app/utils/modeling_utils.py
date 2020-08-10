import pandas as pd
import json
import numpy as np
import random

class Rating():
    def __init__(self, rating):
        self.rating = rating

def time_control(game_perf, data):
    perfs = {'ultrabullet':30, 'bullet':60, 'blitz':300, 'rapid':600, 'classical':1800}
    for perf in perfs:
        if perf == game_perf:
            data = data.append(pd.Series([1], index=['perf_' + perf]))
        else:
            data = data.append(pd.Series([0], index=['perf_' + perf]))
    data = data.append(pd.Series([perfs[game_perf]], index=['clock_initial']))
    data = data.append(pd.Series([0], index=['clock_increment']))

    return data

def player_ratings(player_info, color, data, game_perf):
    perfs = ['ultrabullet', 'bullet', 'blitz', 'rapid', 'classical', 'correspondence']

    ratings = player_info['perfs']

    for perf in perfs:
        if perf == game_perf:
            if perf in ratings and 'prov' not in ratings[perf]:
                data = data.append(pd.Series([ratings[perf]['rating']], index=[color + '_' + perf + '_rating']))
                data = data.append(pd.Series([ratings[perf]['rating']], index=[color + '_rating']))
            else:
                data = data.append(pd.Series([0], index=[color + '_' + perf + '_rating']))
                data = data.append(pd.Series([0], index=[color + '_rating']))
        else:
            if perf in ratings and 'prov' not in ratings[perf]:
                data = data.append(pd.Series([ratings[perf]['rating']], index=[color + '_' + perf + '_rating']))
            else:
                data = data.append(pd.Series([0], index=[color + '_' + perf + '_rating']))

    return data

def rating_difference(perf, data):
    white_rating_columns = [column for column in data.index if ('rating' in column) and ('white' in column)]
    black_rating_columns = [column for column in data.index if ('rating' in column) and ('black' in column)]
    data['rating_difference'] = data['white_' + perf + '_rating'] - data['black_' + perf + '_rating']
    for white_column in white_rating_columns:
        black_column = white_column.replace('white', 'black')
        data[white_column[6:] + '_difference'] = data[white_column]-data[black_column]
    data.drop(labels=white_rating_columns+black_rating_columns, inplace=True)

def transform(data, white_info, black_info, evaluation, white_clock, black_clock, perf):
    data = player_ratings(white_info, 'white', data, perf.lower())
    data = player_ratings(black_info, 'black', data, perf.lower())
    data = time_control(perf.lower(), data)

    data = data.append(pd.Series([int(white_clock)], index=['white_clock']))
    data = data.append(pd.Series([int(black_clock)], index=['black_clock']))

    if evaluation[0] == '#':
        data = data.append(pd.Series([float(evaluation[1:])], index=['eval']))
        data = data.append(pd.Series([True], index=['is_mate']))
    else:
        data = data.append(pd.Series([float(evaluation)], index=['eval']))
        data = data.append(pd.Series([False], index=['is_mate']))

    column_order = ['perf_blitz', 'perf_bullet', 'perf_classical', 'perf_rapid',
        'perf_ultrabullet', 'white_rating', 'white_ultrabullet_rating',
        'white_bullet_rating', 'white_blitz_rating', 'white_rapid_rating',
        'white_classical_rating', 'white_correspondence_rating', 'black_rating',
        'black_ultrabullet_rating', 'black_bullet_rating', 'black_blitz_rating',
        'black_rapid_rating', 'black_classical_rating', 'black_correspondence_rating',
        'clock_initial', 'clock_increment', 'white_clock', 'black_clock', 'eval', 'is_mate']

    data = data[column_order]

    print(data)

    return data
