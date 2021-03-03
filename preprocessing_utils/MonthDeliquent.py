from sklearn.base import BaseEstimator,TransformerMixin
from preprocessing_utils.create_log import Create_preprocessing_logs
import numpy as  np
class MonthDeliquent(BaseEstimator, TransformerMixin):
    def __init__(self,X):
        self.X = X
        self.create_preprocessing_logs = Create_preprocessing_logs()

    def fit(self, X, y=None):
        return self

    def transform(self, X, y=None):
        try:
            X['Months since last delinquent'] = X['Months since last delinquent'].replace(np.nan, 0)
            self.create_preprocessing_logs.insert_log("Preprocessing_log/preprocessing_log.txt",
                                                      "Months since last delinquent nan value converted to 0 Successfully")
            return X
        except Exception as e:
            self.create_preprocessing_logs.insert_log("Preprocessing_log/preprocessing_error_log.txt",
                                                      "Something went wrong in MonthDeliquent")



