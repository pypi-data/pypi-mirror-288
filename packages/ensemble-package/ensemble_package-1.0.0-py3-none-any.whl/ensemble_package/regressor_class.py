import numpy as np
import pandas as pd

from sklearn.linear_model import LinearRegression, Ridge
from sklearn.neighbors import KNeighborsRegressor


# Regressor-Klasse

class Regressor:
    '''Die Regressor-Klasse bildet die Grundlage für das Ensemble.
    In ihr werden die einzelnen Regressoren abgebildet.
    Die folgenden Funktionen stehen dabei zu Verfügung:
    fit()
    predict()
    fit_predict()
    score()'''

    def __init__(self, regressor_type: str):
        
        if regressor_type == "linear_regressor":
            self.model = LinearRegression()
        
        elif regressor_type == "nearest_neighbor_regressor":
            self.model = KNeighborsRegressor()
        
        elif regressor_type == "ridge_regressor":
            self.model = Ridge()

        elif not regressor_type:
            self.model = None

        else:
            raise ValueError(f'Regressortyp {regressor_type} steht nicht zur Verfügung.')



    #defining the hidden check_input function
    def __check_input(self, x):
        self.x = x


        # check wether all instances are a int or float if input is a list
        if isinstance(x, list):
            if not np.isnan(x).any():
                return True
            else:
                raise ValueError(f'There are non-numerical inputs within the given list')
    
        
        
        # check wether all instances are a int or float if input is a pandas-dataframe
        elif isinstance(x, pd.DataFrame):
            if np.all(x.map(lambda i: isinstance(i, (int, float)))):
                    return True
            else:
                    raise ValueError(f'There are non-numerical inputs within the given pd.Dataframe')
        

        # check wether all instances are a int or float if input is a pandas-series
        elif isinstance(x, pd.Series):
            if np.all(x.map(lambda i: isinstance(i, (int, float)))):
                    return True
            else:
                raise ValueError(f'There are non-numerical inputs within the given series')


        # check wether all instances are a int or float if input is a numpy-aray
        if isinstance(x, np.ndarray):
            if not np.isnan(x).any():
                return True
            else:
                raise ValueError(f'There are non-numerical inputs within the given np.array')
        

        # raise error due to unsupported input
        else:
            raise ValueError(f'unsupported input-type, please use list, np.array, pd.Series or pd.Dataframe')



    # defining the fit-function
    def fit(self, X, y):
        
        if self.__check_input(X) and self.__check_input(y):
            self.model.fit(X, y)


    # defining the predict-function
    def predict(self, X):
        
        if self.__check_input(X):
            return self.model.predict(X)


    # defining the fit_predict-function
    def fit_predict(self, X, y, Z):
        
        if self.__check_input(X) and self.__check_input(y):
            self.model.fit(X, y)
            return self.model.predict(Z)


    # defining the score-function
    def score(self, X, y):
        
        if self.__check_input(X) and self.__check_input(y):
            return self.model.score(X, y)
