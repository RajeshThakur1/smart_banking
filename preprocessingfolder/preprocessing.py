import pandas as pd
import numpy as np
from sklearn import preprocessing
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import LabelEncoder
from sklearn.experimental import enable_iterative_imputer
from sklearn.impute import IterativeImputer, KNNImputer
from sqlalchemy import column
from problem_utills import preprocessing_utills
from collections import Counter
import time
import os
from application_logging import logger

class Preprocessing:

    def __init__(self):
        self.logger = logger.App_Logger()
        error_file = open("Preprocessing_log/preprocessing_error_log.txt",'a+')


    def drop_columns(self, data,col_list):

        """
        droping the unnecessary columns

        :param data:
        :return:
        """
        data_reduced = data.drop(col_list, axis=1)
        #file = open("Preprocessing_log/preprocessing_log.txt", 'a+')
        #message = col_list+" has been dropped"
        #self.logger.log(file, message)
        #file.close()
        return data_reduced

    def get_null_column_list(self,data):
        #file = open("Preprocessing_log/preprocessing_log.txt", 'a+')
        #self.logger.log(file, list(data.columns[data.isnull().any()])+" having the null values")
        #file.close()
        return list(data.columns[data.isnull().any()])

    def replace_nan_zero(self,data,col):
        data[col] = data[col].replace(np.nan, 0)

        return data

    def saveUpdatedDataSet_path(UpdatedDataSet_path="UPDATED_DATASET"):
        os.makedirs(UpdatedDataSet_path, exist_ok=True)
        fileName = time.strftime("credit_ver_%Y_%m_%d_%H_%M_%S_.csv")
        UpdatedDataSet_path = os.path.join(UpdatedDataSet_path, fileName)
        print(f"your UpdatedDataSet will be saved at the following location\n{UpdatedDataSet_path}")
        return UpdatedDataSet_path

    # this method will replace the NAN by maxmium value

    def remove_nan(self,df, colname):
        df.loc[df[colname].isnull(), [colname]] = int(np.max(df[colname]))

    def extract_digit(self, df, colname):
        return df.loc[df[colname].notnull(), colname].str.extract('(\d+)').astype(int)

    # Handling the invalid credit score
    def handle_cr_score(self,data,col):
        Cr_Scr = []
        for i in data[col]:
            if np.isnan(i):
                Cr_Scr.append(i)
            else:
                if float(str(i)[:3]) > 900:
                    Cr_Scr.append(900.0)
                else:
                    Cr_Scr.append(float(str(i)[:3]))
        return Cr_Scr

    def replace_col_value(self,data,col,curr_value,new_value):
        data.replace({col: {curr_value: new_value}}, inplace=True)
        return data

    def get_highly_corr_col(self,data):
        # Calculate the correlation matrix and take the absolute value
        corr_matrix = data.corr().abs()
        # Create a True/False mask and apply it
        mask = np.triu(np.ones_like(corr_matrix, dtype=bool))
        tri_df = corr_matrix.mask(mask)
        # List column names of highly correlated features (r > 0.4)
        high_cor = [c for c in tri_df.columns if any(tri_df[c] > 0.4)]
        # Drop the features in the to_drop list
        # reduced_df = ansur_df.drop(to_drop, axis=1)
        # print("The reduced_df dataframe has {} columns".format(reduced_df.shape[1]))
        return high_cor

    def detect_outlier(self,df, n, features):
        outlier_indecies = []
        for col in features:
            Q1 = np.percentile(df[col], 25)  # Finding the Quartile Range
            Q3 = np.percentile(df[col], 75)  # Finding the 3rd Quartile Range

            IQR = Q3 - Q1

            # Setting the outlier Steps
            outlier_steps = 1.5 * IQR

            # findinfg the outlier indices

            outlier_indices_col = df[(df[col] < Q1 - outlier_steps) | (df[col] > Q3 + outlier_steps)].index
            outlier_indecies.extend(outlier_indices_col)

        outlier_indecies = Counter(outlier_indecies)

        multiple_outlier = list(k for k, v in outlier_indecies.items() if v > n)
        return multiple_outlier
    def get_numerical_col(self,data):
        num_cols = data.select_dtypes(include=np.number)
        return num_cols

    def fill_missing_value_KNN_imputer(self,data):
        # Creating instance of KNNImputer.
        num_cols = self.get_numerical_col(data)
        print(num_cols.columns)
        print(num_cols.isnull().sum())
        impute_knn = KNNImputer()
        trans = impute_knn.fit_transform(num_cols)
        try:
            trans_dataframe = pd.DataFrame(trans, columns=['Years in current job',
                                                           'Credit Score',
                                                           'Current Loan Amount',
                                                           'Months since last delinquent',
                                                           'Annual Income',
                                                           'Monthly Debt',
                                                           'Years of Credit History',
                                                           'Number of Open Accounts',
                                                           'Number of Credit Problems',
                                                           'Current Credit Balance',
                                                           'Maximum Open Credit'])
                                                           #'Purpose',
                                                           #'Monthly Debt',
                                                           # 'Years of Credit History',
                                                           # 'Months since last delinquent',
                                                           # 'Number of Open Accounts',
                                                           # 'Number of Credit Problems',
                                                           # # 'Current Credit Balance',
                                                           #'Maximum Open Credit',
                                                           #'Bankruptcies',
                                                           #'Tax Liens'

            return trans_dataframe
        except ValueError as error:
            print(error)
            self.logger.log(self.error_file, "Take a Trip has been replaced Have vacation")





    def get_cat_col_list(self,data):
        cat_col = data.select_dtypes(exclude=np.number).columns.to_list()
        return cat_col

    def get_highly_corr_col_list(self,New_Data):
        # Calculate the correlation matrix and take the absolute value
        corr_matrix = New_Data.corr().abs()
        # Create a True/False mask and apply it
        mask = np.triu(np.ones_like(corr_matrix, dtype=bool))
        tri_df = corr_matrix.mask(mask)
        # List column names of highly correlated features (r > 0.4)
        high_cor = [c for c in tri_df.columns if any(tri_df[c] > 0.4)]
        # Drop the features in the to_drop list
        # reduced_df = ansur_df.drop(to_drop, axis=1)
        # print("The reduced_df dataframe has {} columns".format(reduced_df.shape[1]))
        return high_cor

    # Above bankruptcy data shows some decimal values which doesnt look possible, might be because of KNNImputation
    # missing values would have been filled with some aggreegates which resulted in decimal values.
    # We will tackle this by rounding the values to the nearest integer.

    def roundOff_Bankruptcies(self, New_Data):
        bankr = [round(i) for i in New_Data['Bankruptcies']]
        print(bankr)
        New_Data['Bankruptcies'] = bankr

        return New_Data







