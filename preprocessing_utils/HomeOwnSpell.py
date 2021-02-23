###Home Ownership
from sklearn.base import BaseEstimator,TransformerMixin

from preprocessing_utils.create_log import Create_preprocessing_logs

class HomeOwnSpell(BaseEstimator,TransformerMixin):
    def __init__(self,X):
        self.X=X
        self.create_preprocessing_logs = Create_preprocessing_logs()
    def fit(self,X,y=None):
        return self
    def transform(self,X,y=None):
        try:
            X.replace({'Home Ownership': {'HaveMortgage': 'Home Mortgage'}}, inplace=True)
            return X
            self.create_preprocessing_logs.insert_log("Preprocessing_log/preprocessing_log.txt",
                                                      "Successfully HomeOwnSpell into Data frame")
        except Exception as e:
            self.create_preprocessing_logs.insert_log("Preprocessing_log/preprocessing_error_log.txt",
                                                      "Something went wrong in Array to Dataframe")



