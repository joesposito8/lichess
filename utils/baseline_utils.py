import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from decimal import Decimal, ROUND_HALF_UP

def con_interval(points, games):
    p = points/games
    return (p, p - 1.96*((p*(1-p)/games)**.5), p + 1.96*((p*(1-p)/games)**.5))

def columns_group(df, game_speed, round_num, number):
    ret = [game_speed, number]
    rows = df.loc[(round_to(df['Rating Difference'], round_num) == number) & (df["Game Speed"] == game_speed)]
    ret += [rows['Total Points'].sum(), rows['Total Games'].sum(), rows['Total Draws'].sum()]
    return ret

def columns_group_tail(df, game_speed, number, upper_or_lower):
    if upper_or_lower == 'upper':
        ret = [game_speed, "> " + str(number)]
        rows = df.loc[(df['Rating Difference'] > number) & (df["Game Speed"] == game_speed)]
    else:
        ret = [game_speed, "< " + str(number)]
        rows = df.loc[(df['Rating Difference'] < number) & (df["Game Speed"] == game_speed)]
    ret += [rows['Total Points'].sum(), rows['Total Games'].sum(), rows['Total Draws'].sum()]
    return ret

def round_to(x, to):
    return to * round(x/to)

def create_pivot(df, x, y, value, boundaries):
    pivot = df.pivot(index=y, columns=x, values=value)

    cols = list(pivot)
    cols.insert(0, cols.pop(cols.index('< ' +str(boundaries[0]))))
    pivot = pivot.loc[:, cols]
    return pivot

def create_heatmap(pivot, x, y, value, granularity):
    fig, ax = plt.subplots(figsize=(55,11))
    ax.tick_params(axis='both', which='major', labelsize=24)
    ax.set_title(f"{value} based on {x} and {y}, June 2020",fontsize=48)
    ax.set_xlabel(x, fontsize = 32)
    ax.set_ylabel(y, fontsize = 32)
    ax.title.set_position([.5, 1.05])
    ax.set_facecolor('xkcd:salmon')

    if granularity == 100:
        heat = sns.heatmap(pivot, annot=True, cmap='RdYlGn', fmt='.3f', annot_kws={"size":24})
    else:
        heat = sns.heatmap(pivot, annot=True, cmap='RdYlGn', fmt='.3f', annot_kws={"size":18})
