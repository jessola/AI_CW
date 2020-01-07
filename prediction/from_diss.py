from sklearn.linear_model import BayesianRidge
from sklearn.model_selection import train_test_split
import numpy as np

from journeys import at_station

if __name__ == '__main__':

    journeys = at_station('STFD')
    X = [row[2:4] for row in journeys if None not in [row[3], row[4], row[5]]]
    Y = [row[-1] for row in journeys if None not in [row[3], row[4], row[5]]]

    reg = BayesianRidge()
    X_train, X_test, Y_train, Y_test = train_test_split(
        X,
        Y,
        test_size=0.2,
    )

    # t = [j for j in journeys if j[-1]]
    # print(t)

    reg.fit(X_train, Y_train)

    print(reg.predict([[1, 10], [0, 10]]))
