from sklearn.linear_model import BayesianRidge
from sklearn.neighbors import KNeighborsRegressor
from sklearn.model_selection import train_test_split
from joblib import dump, load

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
if __name__ == "__main__":
    # dump(from_station('IPSWICH'), 'prediction/models/ipsw_arr.joblib')
    # dump(from_station('IPSWICH', True), 'prediction/models/ipsw_dep.joblib')
    # dump(from_station('STWMRKT'), 'prediction/models/stow_arr.joblib')
    # dump(from_station('STWMRKT', True), 'prediction/models/stow_dep.joblib')
    # dump(from_station('MANNGTR'), 'prediction/models/mann_arr.joblib')
    # dump(from_station('MANNGTR', True), 'prediction/models/mann_dep.joblib')
    # dump(from_station('CLCHSTR'), 'prediction/models/colc_arr.joblib')
    # dump(from_station('CLCHSTR', True), 'prediction/models/colc_dep.joblib')
    # dump(from_station('CHLMSFD'), 'prediction/models/chel_arr.joblib')
    # dump(from_station('CHLMSFD', True), 'prediction/models/chel_dep.joblib')
    # dump(from_station('STFD'), 'prediction/models/stfd_arr.joblib')
    # dump(from_station('STFD', True), 'prediction/models/stfd_dep.joblib')
    # dump(from_station('LIVST'), 'prediction/models/lliv_arr.joblib')
    diss_model = load('prediction/models/diss_dep.joblib')
    ipsw_model = load('prediction/models/ipsw_dep.joblib')
    stow_model = load('prediction/models/stow_dep.joblib')
    mann_model = load('prediction/models/mann_dep.joblib')
    colc_model = load('prediction/models/colc_dep.joblib')
    chel_model = load('prediction/models/chel_dep.joblib')
    stfd_model = load('prediction/models/stfd_dep.joblib')

    # print(from_station('DISS', True).predict([[1, 8]]))
    print('DISS', diss_model.predict([[1, 5]]))
    print('IPSW', ipsw_model.predict([[1, 5]]))
    print('STOW', stow_model.predict([[1, 5]]))
    print('MANN', mann_model.predict([[1, 5]]))
    print('COLC', colc_model.predict([[1, 5]]))
    print('CHEL', chel_model.predict([[1, 5]]))
    print('STFD', stfd_model.predict([[1, 5]]))
