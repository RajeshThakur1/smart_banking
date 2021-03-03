from sklearn.base import BaseEstimator,TransformerMixin
from sklearn.impute import IterativeImputer, KNNImputer
from preprocessing_utils.create_log import Create_preprocessing_logs
import pandas as pd
class KNN_Imputer(BaseEstimator, TransformerMixin):
    def __init__(self,X):
        self.X = X
        #self.num_col = num_col
        self.create_preprocessing_logs = Create_preprocessing_logs()

    def fit(self, X, y=None):
        return self

    def get_numerical_col(self,data):
        num_cols = data.select_dtypes(include=np.number)
        return num_cols

    def transform(self,X, y=None):
        # Creating instance of KNNImputer.
        num_cols = self.get_numerical_col(X)
        print(num_cols.columns)
        print(num_cols.isnull().sum())
        impute_knn = KNNImputer()
        trans = impute_knn.fit_transform(num_cols)

        try:
            trans_dataframe = pd.DataFrame(trans, columns=['Years in current job',
                                                           'Credit Score',
                                                           'Annual Income',

                                                           'Monthly Debt',
                                                           'Years of Credit History',
                                                           'Months since last delinquent',
                                                           'Number of Open Accounts',
                                                           'Number of Credit Problems',
                                                           'Current Credit Balance',
                                                           'Maximum Open Credit',
                                                           'Bankruptcies',
                                                           'Tax Liens'])

            return trans_dataframe
        except ValueError as error:
            self.create_preprocessing_logs.insert_log("Preprocessing_log/preprocessing_log.txt",
                                                      "Fail to create the Data frame")
