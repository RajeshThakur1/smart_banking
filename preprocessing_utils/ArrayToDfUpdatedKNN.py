####Creating a updated ArraytoDataframe class with updated columns

import pandas as pd
from sklearn.base import BaseEstimator,TransformerMixin

from preprocessing_utils.create_log import Create_preprocessing_logs



class ArrayToDfUpdatedKNN(BaseEstimator, TransformerMixin):

    def __init__(self,X):
        self.X = X
        self.create_preprocessing_logs = Create_preprocessing_logs()

    def fit(self, X, y=None):
        return self

    def transform(self, X, y=None):
        try:
            X = pd.DataFrame(X, \
                             index=[i for i in range(X.shape[0])], \
                             columns=['Years in current job', 'Credit Score', 'Current Loan Amount',
                                      'Months since last delinquent', 'Home Ownership', 'Purpose', 'Term',
                                      'Annual Income',
                                      'Monthly Debt', 'Years of Credit History',
                                      'Number of Open Accounts',
                                      'Number of Credit Problems', 'Current Credit Balance',
                                      'Maximum Open Credit']

                             )

            self.create_preprocessing_logs.insert_log("Preprocessing_log/preprocessing_log.txt",
                                                      "Successfully Array converted into Data frame")

            return X

        except Exception as e:
            self.create_preprocessing_logs.insert_log("Preprocessing_log/preprocessing_error_log.txt",
                                                      "Something went wrong in ArrayToDfUpdatedKNN")

