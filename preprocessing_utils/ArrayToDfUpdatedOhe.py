import pandas as pd
from sklearn.base import BaseEstimator,TransformerMixin

from preprocessing_utils.create_log import Create_preprocessing_logs
class ArrayToDfUpdatedOhe(BaseEstimator, TransformerMixin):

    def __init__(self,X):

        self.X = X
        self.create_preprocessing_logs = Create_preprocessing_logs()

    def fit(self, X, y=None):
        return self

    def transform(self, X, y=None):
        try:
            X = pd.DataFrame(X, \
                             index=[i for i in range(X.shape[0])], \
                             columns=['Current Loan Amount', 'Credit Score', 'Annual Income', \
                                      'Years in current job', 'Monthly Debt', 'Years of Credit History', \
                                      'Months since last delinquent', 'Number of Open Accounts', \
                                      'Number of Credit Problems', 'Current Credit Balance', \
                                      'Maximum Open Credit', 'Home Ownership', 'Purpose', 'Term']

                             )
            self.create_preprocessing_logs.insert_log("Preprocessing_log/preprocessing_log.txt",
                                                      "Successfully Array converted into Data frame")
            return X



        except Exception as e:
            self.create_preprocessing_logs.insert_log("Preprocessing_log/preprocessing_error_log.txt",
                                                      "Something went wrong in ArrayToDfUpdatedOhe to Dataframe")

