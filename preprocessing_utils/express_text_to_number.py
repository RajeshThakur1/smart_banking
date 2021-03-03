from sklearn.base import BaseEstimator,TransformerMixin

from preprocessing_utils.create_log import Create_preprocessing_logs

##Work Exp
class ExpTextToNum(BaseEstimator, TransformerMixin):

    def __init__(self,data):
        self.data = data
        self.create_preprocessing_logs = Create_preprocessing_logs()



    def fit(self, X, y=None):
        return self

    def transform(self, X, y=None):

        try:
            Years = []
            for i in X['Years in current job']:

                if i == '8 years':
                    Years.append(8)
                elif i == '6 years':
                    Years.append(6)
                elif i == '3 years':
                    Years.append(3)
                elif i == '5 years':
                    Years.append(5)
                elif i == '< 1 year':
                    Years.append(0.8)
                elif i == '2 years':
                    Years.append(2)
                elif i == '4 years':
                    Years.append(4)
                elif i == '9 years':
                    Years.append(9)
                elif i == '7 years':
                    Years.append(7)
                elif i == '1 year':
                    Years.append(1)
                else:

                    Years.append(10)
            X['Years in current job'] = Years

            self.create_preprocessing_logs.insert_log("Preprocessing_log/preprocessing_log.txt",
                                                      "Text data of year has been converted in number")
            return X
        except Exception as e:
            self.create_preprocessing_logs.insert_log("Preprocessing_log/preprocessing_error_log.txt",
                                                      "Something went wrong in express_text_to_number.py")





