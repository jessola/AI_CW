from sklearn.linear_model import BayesianRidge
from sklearn.model_selection import train_test_split
# import numpy as np

from journeys import at_station


def from_station(station, departing=False):
    journeys = at_station(station)
    livst = station == 'LIVST'

    X = [row[2:4] for row in journeys if None not in [row[3], row[4], row[5]]]
    Y = [
        row[-1 if departing else -2] for row in journeys
        if None not in [row[3], row[4], row[5]]
    ]

    if livst:
        X = [row[2:4] for row in journeys if None not in [row[3], row[4]]]
        Y = [row[-2] for row in journeys if None not in [row[3], row[4]]]

    reg = BayesianRidge()
    X_train, X_test, Y_train, Y_test = train_test_split(
        X,
        Y,
        test_size=0.2,
    )

    reg.fit(X_train, Y_train)

    print(reg.predict([[1, 15]]))


from_station('LIVST', True)