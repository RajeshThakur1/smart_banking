###Purpose
from sklearn.base import BaseEstimator,TransformerMixin

from preprocessing_utils.create_log import Create_preprocessing_logs


class PurposeSpell(BaseEstimator,TransformerMixin):
    def __init__(self,X):
        self.X=X
        self.create_preprocessing_logs = Create_preprocessing_logs()
    def fit(self,X,y=None):
        return self
    def transform(self,X,y=None):
        try:
            X.replace({'Purpose': {'other': 'Other', 'Take a Trip': 'vacation'}}, inplace=True)
            return X
            self.create_preprocessing_logs.insert_log("Preprocessing_log/preprocessing_log.txt",
                                                      "Successfully PurposeSpell into Data frame")

        except Exception as e:
            self.create_preprocessing_logs.insert_log("Preprocessing_log/preprocessing_error_log.txt",
                                                      "Something went wrong in APurposeSpell to Dataframe")

