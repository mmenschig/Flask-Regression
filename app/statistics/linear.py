# For macOS (and heroku), we call a different rendering backend
# for matplotlib. This call needs to precede all
# import of all other rendering libraries.
import matplotlib as mpl
mpl.use('Agg')

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# TODO: accept additional parameters passed from form input
def main(timestamp, filename):
    path = 'app/uploads/{}'.format(filename)
    df = pd.read_csv(path, header=None, sep=",", names=['x', 'y'])

    y = df['y'].values
    x = df['x'].values

    fig, ax = plt.subplots(figsize=(8, 4))
    yplt = y
    ax.scatter(x, yplt, alpha=0.5, color='orchid')
    fig.suptitle('Function with XY Confidence Interval')
    fig.tight_layout(pad=2)
    ax.grid(True)

    save_path = 'app/charts/{}.png'.format(timestamp)
    fig.savefig(save_path, dpi=125)
