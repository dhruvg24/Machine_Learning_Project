import sys
from dataclasses import dataclass
import pandas as pd
import numpy as np
from sklearn.compose import ColumnTransformer
# column transformer - Standard Scaler, One Hot Encoder
from sklearn.impute import SimpleImputer #for missing values
from sklearn.preprocessing import OneHotEncoder,StandardScaler
from sklearn.pipeline import Pipeline
from src.exception import CustomException
from src.logger import logging
from src.utils import save_object
import os 

# Use @dataclass when the class:
# Primarily stores values (like configuration parameters)
# Doesn't require a lot of custom logic or methods
# Benefits from auto-generated methods (like __init__, __repr__, etc.)

@dataclass
class DataTransformationConfig:
    preprocessor_obj_file_path = os.path.join('artifacts','preprocessor.pkl')

class DataTransformation:
    def __init__(self):
        self.data_transformation_config = DataTransformationConfig()

    def get_data_transformer_obj(self):
        try:
            numerical_columns=['writing_score','reading_score']
            categorical_columns=[
                'gender',
                'race_ethnicity',
                'parental_level_of_education',
                'lunch',
                'test_preparation_course'
            ]
            # create pipeline 
            num_pipeline = Pipeline(
                steps = [
                    ('imputer',SimpleImputer(strategy='median')),
                    # imputer resolves the missing values, also there are outliers which needs to be handled.Missing values (in case of numerical features) replaced by median.
                    ('scaler', StandardScaler())
                ]
            )

            cat_pipeline = Pipeline(
                steps = [
                    ('imputer',SimpleImputer(strategy='most_frequent')),
                    ('one_hot_encoder',OneHotEncoder()),
                    ('scaler',StandardScaler(with_mean=False))
                    # with_mean ensures that for sparse matrix scaling happens without centering.

                ]
            )

            # logging.info('Numerical columns standard scaling completed')
            # logging.info('Categorical columns standard encoding completed')
            logging.info(f'Categorical columns: {categorical_columns}')
            logging.info(f'Numerical columns: {numerical_columns}')

            preprocessor = ColumnTransformer(
                [
                    ('num_pipeline',num_pipeline,numerical_columns),
                    ('cat_pipeline',cat_pipeline,categorical_columns)
                ]
            )

            return preprocessor


        except Exception as e:
            raise CustomException(e,sys)
        
    def initiate_data_transformation(self, train_path, test_path):
        try:
            train_df = pd.read_csv(train_path)
            test_df = pd.read_csv(test_path)
            logging.info('The train and test data completed')

            logging.info('Obtaining preprocessing object')
            preprocessing_obj = self.get_data_transformer_obj()

            target_column_name = 'math_score'
            numerical_columns=['writing_score','reading_score']

            input_feature_train_df = train_df.drop(columns=[target_column_name],axis=1)
            target_feature_train_df = train_df[target_column_name]

            input_feature_test_df = test_df.drop(columns=[target_column_name],axis=1)
            target_feature_test_df = test_df[target_column_name]

            logging.info(
                f'Applying preprocessing object on training dataframe and testing dataframe.'
            )

            input_feature_train_arr = preprocessing_obj.fit_transform(input_feature_train_df)
            input_feature_test_arr = preprocessing_obj.transform(input_feature_test_df)


            train_arr= np.c_[
                # column wise add.
                input_feature_train_arr,np.array(target_feature_train_df)
            ]
            test_arr = np.c_[input_feature_test_arr,np.array(target_feature_test_df)]   

            logging.info('Saving preprocessing object.')

            save_object(
                file_path = self.data_transformation_config.preprocessor_obj_file_path,
                obj=preprocessing_obj
            )

            return(
                train_arr,
                test_arr,
                self.data_transformation_config.preprocessor_obj_file_path
            )

        except Exception as e:
            raise CustomException(e,sys)







