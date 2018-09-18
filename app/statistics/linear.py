# For macOS (and heroku), we call a different rendering backend
# for matplotlib. This call needs to precede all
# import of all other rendering libraries.
import matplotlib as mpl
mpl.use('Agg')

import numpy as np
import pandas as pd
from scipy import stats
import matplotlib.pyplot as plt
import statsmodels.api as sm

# TODO: accept additional parameters passed from form input
# TODO: get filename path from config
def main(timestamp, filename, request_body):
    path = 'app/uploads/{}'.format(filename)
    df = pd.read_csv(path, header=None, sep=",", names=['x', 'y'])

    y = df['y'].values
    x = df['x'].values

    fig, ax = plt.subplots(figsize=(8, 4))
    yplt = y
    ax.scatter(x, yplt, alpha=0.5, color='dodgerblue')
    fig.suptitle(request_body["chart_title"])
    fig.tight_layout(pad=2)
    ax.grid(True)

    save_path = 'app/charts/{}.png'.format(timestamp)
    # Plots only the data points
    # fig.savefig(save_path, dpi=125)

    x = sm.add_constant(x)
    model = sm.OLS(y, x)
    fitted = model.fit()

    x_pred = np.linspace(x.min(), x.max(), 50)
    x_pred2 = sm.add_constant(x_pred)
    y_pred = fitted.predict(x_pred2)
    yplt = y_pred
    ax.plot(x_pred, yplt, '-', color='deepskyblue', linewidth=2)
    # Plots data points with regression line
    # fig.savefig(save_path, dpi=250)

    print(fitted.params)     # the estimated parameters for the regression line
    print(fitted.summary())  # summary statistics for the regression

    y_hat = fitted.predict(x) # x is
    y_err = y - y_hat

    mean_x = x.T[1].mean()
    n = len(x)

    dof = n - fitted.df_model - 1
    t = stats.t.ppf(1-0.025, df=dof)
    s_err = np.sum(np.power(y_err, 2)) # Standard error

    conf = t * np.sqrt((s_err/(n-2))*(1.0/n + (np.power((x_pred-mean_x),2) /
            ((np.sum(np.power(x_pred,2))) - n*(np.power(mean_x,2))))))

    upper = y_pred + abs(conf)
    lower = y_pred - abs(conf)

    ax.fill_between(x_pred, lower, upper, color='powderblue', alpha=0.3)
    # Save chart
    fig.savefig(save_path, dpi=125)
