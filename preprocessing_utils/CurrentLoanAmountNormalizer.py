from sklearn.base import BaseEstimator,TransformerMixin
import numpy as np
from preprocessing_utils.create_log import Create_preprocessing_logs
# CurrentLoanAmount

class CurrentLoanAmountNormalizer(BaseEstimator, TransformerMixin):

    def __init__(self,X):
        self.X = X
        self.create_preprocessing_logs = Create_preprocessing_logs()

    def fit(self, X, y=None):
        return self

    def transform(self, X, y=None):

        try:
            X.replace({'Current Loan Amount': {99999999.000000: 0}}, inplace=True)
            X['Current Loan Amount'].replace(0, np.nan, inplace=True)
            self.create_preprocessing_logs.insert_log("Preprocessing_log/preprocessing_log.txt",
                                                      "CurrentLoanAmountNormalizer normalized Successfully")
            return X

        except Exception as e:
            self.create_preprocessing_logs.insert_log("Preprocessing_log/preprocessing_error_log.txt",
                                                      "Something went wrong in current amount Normalization")



