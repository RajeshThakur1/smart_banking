import pandas as pd
from application_logging import logger
from preprocessing_utils.create_log import Create_preprocessing_logs
class Get_independet_dependent_data():

    def __init__(self):
        ##This is to display the numerical values as decimals instead of scientific notations like 5.951188e+08
        pd.set_option('float_format', '{:f}'.format)

        self.create_preprocessing_logs = Create_preprocessing_logs()



    def get_independent_dependent_data(self,data):
        #error_logs = open("Preprocessing_log/preprocessing_error_log.txt", 'a+')
        #preprocessing_logs = open("Preprocessing_log/preprocessing_log.txt", 'a+')
        try:
            X = data[['Loan ID', 'Customer ID', 'Current Loan Amount', 'Term',
                      'Credit Score', 'Annual Income', 'Years in current job',
                      'Home Ownership', 'Purpose', 'Monthly Debt', 'Years of Credit History',
                      'Months since last delinquent', 'Number of Open Accounts',
                      'Number of Credit Problems', 'Current Credit Balance',
                      'Maximum Open Credit', 'Bankruptcies', 'Tax Liens']]

            y = data['Loan Status']
            # self.logger.log(preprocessing_logs, "Data has segregated successfully in Ip and Op")
            # preprocessing_logs.close()
            self.create_preprocessing_logs.insert_log("Preprocessing_log/preprocessing_log.txt","Data has segregated successfully in Ip and Op")

            return X, y
        except Exception as e:
            # self.logger.log(error_logs, "Something went wrong in segration of Input and OP columns")
            # error_logs.close()
            self.create_preprocessing_logs.insert_log("Preprocessing_log/preprocessing_error_log.txt","Something went wrong in segration of Input and OP columns")


