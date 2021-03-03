from wsgiref import simple_server
#https://drive.google.com/drive/folders/1hnVu6CjsuULA7A9zLmcv-8siPlA5VF4n

from flask import Flask, request, render_template

import os
import json
from flask_cors import CORS, cross_origin
import glob

from sklearn.impute import KNNImputer

from RawDataValidation.rawValidation import Raw_Data_validation
from Data_ingestion.data_ingestion import data_getter
from preprocessingfolder.preprocessing import Preprocessing
import shutil
from application_logging.logger import App_Logger
from problem_utills.preprocessing_utills import utills
from flask import Response
import pandas as pd
import numpy as np
from sklearn.compose import ColumnTransformer,make_column_transformer
from sklearn.pipeline import Pipeline,make_pipeline
from sklearn.base import BaseEstimator,TransformerMixin
from preprocessing_utils.express_text_to_number import ExpTextToNum
from preprocessing_utils.get_dependent_and_indepenedent_data import Get_independet_dependent_data
from preprocessing_utils.CreditScoreNormalizer import CreditScoreNormalizer
from preprocessing_utils.CurrentLoanAmountNormalizer import CurrentLoanAmountNormalizer
from preprocessing_utils.MonthDeliquent import MonthDeliquent
from preprocessing_utils.ArrayToDf import ArrayToDf
from preprocessing_utils.HomeOwnSpell import HomeOwnSpell
from preprocessing_utils.PurposeSpell import PurposeSpell
from preprocessing_utils.ArrayToDfUpdatedKNN import ArrayToDfUpdatedKNN
from preprocessing_utils.ArrayToDfUpdatedOhe import ArrayToDfUpdatedOhe
from sklearn.preprocessing import OneHotEncoder

import joblib
from preprocessing_utils.Knn_Imputer import KNN_Imputer


app = Flask(__name__)
#dashboard.bind(app)
CORS(app)

@app.route("/validate_input_file", methods=['GET'])
@cross_origin()

def validate_input_file():
    file_path = "Input_data"
    raw_validation = Raw_Data_validation(file_path)
    regex = raw_validation.manualRegexCreation()
    raw_validation.validationFileNameRaw(regex)
    return Response("validation successfully!!")



@app.route("/preprocessing_new", methods=['GET','POST'])
@cross_origin()
def preprocessing_new():
    print("started!!!")

    all_batch_files = glob.glob("Training_Raw_files_validated/Good_Raw/*.csv")
    if len(all_batch_files) > 0:
        data_get = data_getter()
        pre = Preprocessing()
        data = data_get.data_load(all_batch_files[0])
        prep = Get_independet_dependent_data()

        X, y = prep.get_independent_dependent_data(data)

        print("independent columns:-",X.columns)



        KNN_CT = make_column_transformer((KNNImputer(), ['Current Loan Amount', 'Credit Score', 'Annual Income', \
                                                          'Years in current job', 'Monthly Debt',
                                                          'Years of Credit History', \
                                                          'Months since last delinquent', 'Number of Open Accounts', \
                                                          'Number of Credit Problems', 'Current Credit Balance', \
                                                          'Maximum Open Credit']), remainder='passthrough')



        OHE_CT = make_column_transformer(
            (OneHotEncoder(handle_unknown='ignore', sparse=False), ['Term', 'Home Ownership', 'Purpose']),
            remainder='passthrough')

        CT_NUM_CAT = make_column_transformer((ExpTextToNum(X), ['Years in current job']), \
                                             (CreditScoreNormalizer(X), ['Credit Score']), \
                                             (CurrentLoanAmountNormalizer(X), ['Current Loan Amount']), \
                                             (MonthDeliquent(X), ['Months since last delinquent']), \
                                             (HomeOwnSpell(X), ['Home Ownership']), \
                                             (PurposeSpell(X), ['Purpose']), \
                                             ('drop', ['Loan ID', 'Customer ID', 'Bankruptcies', 'Tax Liens']), \
                                             remainder='passthrough')

        PREPRO_PIPE = make_pipeline(CT_NUM_CAT, ArrayToDfUpdatedKNN(X), KNN_CT, ArrayToDfUpdatedOhe(X), OHE_CT)
        joblib.dump(PREPRO_PIPE, "preprocessing_pkl/PREPRO_PIPELINE.pkl")

        ##Checking if the saved pkl file can be loaded again
        PIPE_NUM_LOAD = joblib.load('preprocessing_pkl/PREPRO_PIPELINE.pkl')
        data = PIPE_NUM_LOAD.fit_transform(X.head())
        print(data)


        # #shutil.move("Training_Raw_files_validated/Good_Raw/credit.csv", "Preprocessed_Data")
        print("done")



        return Response("preprocessing successfull!!")

@app.route("/test", methods=['GET'])
@cross_origin()
def test():
    return "success"


if __name__ == "__main__":
    port = int(os.getenv('PORT', 5000))
    app.run(debug=False, port=port, host="127.0.0.1")
    #app.run(debug=True)



