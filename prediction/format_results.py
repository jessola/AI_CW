import numpy as np
import pandas as pd
from sklearn import metrics


def format_results(actual, bayes, knn, head=25):
    # Error Measures
    # errors = {'MAE': None, 'MSE': None, 'RMS': None}
    mae = lambda x: round(metrics.mean_absolute_error(actual, x), 3)
    mse = lambda x: round(metrics.mean_squared_error(actual, x), 3)
    rms = lambda x: round(np.sqrt(metrics.mean_squared_error(actual, x)), 3)

    # Table showing some results
    df = pd.DataFrame({'Actual': actual, 'Bayes Pred': bayes, 'kNN Pred': knn})
    df1 = df.head(25)

    print(df1)
    print('MAE', mae(bayes), mae(knn))
    print('MSE', mse(bayes), mse(knn))
    print('RMS', rms(bayes), rms(knn))
