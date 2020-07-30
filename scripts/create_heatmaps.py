import sys
parent_dir = "\\".join(sys.path[0].split("\\")[:-1])
sys.path.append(parent_dir)
from decimal import Decimal, ROUND_HALF_UP

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from absl import app, flags

from utils.baseline_utils import con_interval, columns_group, columns_group_tail, round_to, create_pivot, create_heatmap

FLAGS = flags.FLAGS

flags.DEFINE_integer('granularity', 100, 'Width of range in heatmap.')

flags.DEFINE_list('boundaries', [-1000, 1000], 'Range of values in heatmap')

flags.DEFINE_bool('draws', False, 'Whether or not to include draws in win prob.')

def main(argv):
    baseline = pd.read_csv(parent_dir + "\\data\\baseline-june.csv")

    if not FLAGS.draws:
        baseline['Total Points'] -= .5*baseline['Total Draws']
        baseline['Total Games'] -= baseline['Total Draws']

    df = pd.DataFrame(columns=baseline.columns)

    for gs in baseline['Game Speed'].unique():
        df.loc[len(df)] = columns_group_tail(baseline, gs, FLAGS.boundaries[0], upper_or_lower='lower')
        for num in range(FLAGS.boundaries[0], FLAGS.boundaries[1]+1, FLAGS.granularity):
            df.loc[len(df)] = columns_group(baseline, gs, FLAGS.granularity, num)
        df.loc[len(df)] = columns_group_tail(baseline, gs, FLAGS.boundaries[1], upper_or_lower='upper')

    df['Game Speed'] = pd.Categorical(df['Game Speed'], ["Bullet", "Blitz", "Rapid", "Classical"])
    df.sort_values(by=['Game Speed', 'Rating Difference'], inplace=True)

    interval = con_interval(df['Total Points'], df['Total Games'])
    df['White Win Probability'] = interval[0]
    df['Lower White Win Probability'] = interval[1]
    df['Upper White Win Probability'] = interval[2]

    interval = con_interval(df['Total Draws'], df['Total Games'])
    df['Draw Probability'] = interval[0]
    df['Lower Draw Probability'] = interval[1]
    df['Upper Draw Probability'] = interval[2]

    float_columns = [column for column in df.columns if column not in ['Game Speed', 'Rating Difference', 'Total Games', 'Total Draws']]
    int_columns = ['Total Games', 'Total Draws']
    df[float_columns] = df[float_columns].astype(float)
    df[int_columns] = df[int_columns].astype(int)

    clip_columns = ['Lower White Win Probability', 'Upper White Win Probability', 'Lower Draw Probability', 'Upper Draw Probability']
    df[clip_columns] = df[clip_columns].clip(0, 1)

    for attribute in df.columns[5:]:
        file_name = "".join([word[0].lower() for word in attribute.split(" ")]) + "_" + str(FLAGS.boundaries[1]) + "_" + str(FLAGS.granularity)
        create_heatmap(create_pivot(df, 'Rating Difference', 'Game Speed', attribute, FLAGS.boundaries), 'Rating Difference', 'Game Speed', attribute, FLAGS.granularity)
        plt.savefig(parent_dir + "\\results\\" + file_name, facecolor='w', bbox_inches="tight")

if __name__ == '__main__':
  app.run(main)
