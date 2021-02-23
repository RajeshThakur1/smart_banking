## Credit Score
import numpy as np
from sklearn.base import BaseEstimator,TransformerMixin

class CreditScoreNormalizer(BaseEstimator, TransformerMixin):

    def __init__(self,data):
        self.data = data

    def fit(self, X, y=None):
        return self

    def transform(self, X, y=None):

        New_Credit_Score = []
        for i in X['Credit Score']:

            if np.isnan(i):
                New_Credit_Score.append(i)
            else:
                if float(str(i)[:3]) > 900:
                    New_Credit_Score.append(900.0)
                else:
                    New_Credit_Score.append(float(str(i)[:3]))
        X['Credit Score'] = New_Credit_Score
        return X
