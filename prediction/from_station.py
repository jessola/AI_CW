from sklearn.linear_model import BayesianRidge
from sklearn.neighbors import KNeighborsRegressor
from sklearn.model_selection import train_test_split

from .format_results import format_results

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
    knn = KNeighborsRegressor(n_neighbors=2)

    X_train, X_test, Y_train, Y_test = train_test_split(
        X,
        Y,
        test_size=0.2,
    )

    reg.fit(X_train, Y_train)
    knn.fit(X_train, Y_train)
    Y_pred = [int(round(num)) for num in reg.predict(X_test)]
    Y_pred2 = [int(round(num)) for num in knn.predict(X_test)]

    # df = pd.DataFrame({'Actual': Y_test, 'Predicted': Y_pred, 'KNN': Y_pred2})
    # df1 = df.head(25)
    # print(df1)
    # print('Mean Absolute', metrics.mean_absolute_error(Y_test, Y_pred),
    #       metrics.mean_absolute_error(Y_test, Y_pred2))
    # print('Mean Squared', metrics.mean_squared_error(Y_test, Y_pred),
    #       metrics.mean_squared_error(Y_test, Y_pred2))
    # print('Root Mean Squared',
    #       np.sqrt((metrics.mean_squared_error(Y_test, Y_pred))),
    #       np.sqrt((metrics.mean_squared_error(Y_test, Y_pred2))))

    # print(reg.predict([[1, 15]]))
    # print(Y_pred)
    # format_results(Y_test, Y_pred, Y_pred2)
    return reg


# from_station('STWMRKT', True)