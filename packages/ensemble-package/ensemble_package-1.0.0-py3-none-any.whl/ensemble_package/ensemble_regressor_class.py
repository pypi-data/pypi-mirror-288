#Auf Notation achten, sprich - oder + für private/public

import numpy as np

from flask_restful import Resource
# from sklearn import ensemble
from flask import request
from sklearn import ensemble
from .regressor_class import Regressor

# Ensemble-Klasse

class Ensemble(Resource):
    '''Diese Klasse soll ein Ensemble aus mehreren einzelnen Regressoren bilden.
    Die möglichen Regressoren sind:
    - linear_regressor
    - nearest_neighbor_regressor
    - ridge_regressor'''


    def __init__(self, input_list):
        self.ensemble = [Regressor(regressor) for regressor in input_list]
    #     self.ensemble = [{key: Regressor(regressor) for key, regressor in request.json.items()}]

    # def __init__(self):
    #     self.ensemble = None

    # def setup(self):
    #     return None



    # def get(self, id):
    #     return {'message': id}

    # def put(self, id):
    #     self.ensemble = {key: Regressor(regressor) for key, regressor in request.json.items()}

        # for key, regressor in request.json.items():
        #     ensemble[key] = Regressor(regressor)


    # def get(self, input_list):
    #     return {"message": input_list}

    # def put(self, input_list):
    #     return {"message": "the ensemble-regressor has been created"}

    def fit(self, X, y):
        for regressor in self.ensemble:
            regressor.fit(X , y)

    def predict(self, X):
        predictions = np.array([regressor.predict(X) for regressor in self.ensemble])
        return np.mean(predictions, axis=0)

    def fit_predict(self, X, y, Z):
        for regressor in self.ensemble:
            regressor.fit(X , y)
        
        predictions = np.array([regressor.predict(Z) for regressor in self.ensemble])
        return np.mean(predictions, axis=0)

    def score(self, X, y):
        single_scores = np.array([regressor.score(X, y) for regressor in self.ensemble])
        return np.mean(single_scores, axis=0)
    
