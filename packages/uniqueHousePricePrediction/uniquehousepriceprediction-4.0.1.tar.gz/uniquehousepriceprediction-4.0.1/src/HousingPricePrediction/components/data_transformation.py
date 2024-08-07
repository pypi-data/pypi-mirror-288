import os
import sys
import pandas as pd
import numpy as np

from dataclasses import dataclass
from src.HousingPricePrediction.exception import CustomException
from src.HousingPricePrediction.logger import logging

from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import LabelEncoder, StandardScaler
from src.HousingPricePrediction.utils.utils import save_object

@dataclass
class DataTransformationConfig:
    """
    This is configuration class for Data Transformation
    """
    preprocessor_obj_file_path: str = os.path.join('artifacts', 'preprocessor.pkl')

class DataTransformation:
    """
    This class handles Data Transformation
    """
    def __init__(self):
        self.data_transformation_config = DataTransformationConfig()

    def transform_data(self):
        try:
            logging.info('Data Transformation initiated')

            # Define which columns should be ordinal-encoded and which should be scaled
            categorical_cols = [
                'mainroad', 'guestroom', 'basement', 
                'hotwaterheating', 'airconditioning', 
                'prefarea', 'furnishingstatus'
            ]
            numerical_cols = [
                'area', 'bedrooms', 'bathrooms', 'stories', 'parking'
            ]
            
            # Define the custom ranking for each ordinal variable
            categorical_categories = {
                'mainroad': ['yes', 'no'],
                'guestroom': ['yes', 'no'],
                'basement': ['yes', 'no'],
                'hotwaterheating': ['yes', 'no'],
                'airconditioning': ['yes', 'no'],
                'prefarea': ['yes', 'no'],
                'furnishingstatus': ['furnished', 'semi-furnished', 'unfurnished']
            }

            logging.info('Pipeline Initiated')

            # Numerical Pipeline
            num_pipeline = Pipeline(
                steps=[
                    ('imputer', SimpleImputer(strategy='median')),
                    ('scaler', StandardScaler())
                ]
            )

            # Categorical Pipeline
            cat_pipeline = Pipeline(
                steps=[
                    ('imputer', SimpleImputer(strategy='most_frequent')),
                    ('labelencoder', LabelEncoder())
                ]
            )

            # Combine pipelines
            preprocessor = ColumnTransformer([
                ('num_pipeline', num_pipeline, numerical_cols),
                ('cat_pipeline', cat_pipeline, categorical_cols)
            ])

            return preprocessor

        except Exception as e:
            logging.error("Exception occurred in the transform_data method")
            raise CustomException(e, sys)

    def initiate_data_transformation(self, train_path, test_path):
        try:
            train_df = pd.read_csv(train_path)
            test_df = pd.read_csv(test_path)

            logging.info(f'Train Dataframe Head : \n{train_df.head().to_string()}')
            logging.info(f'Test Dataframe Head : \n{test_df.head().to_string()}')

            preprocessing_obj = self.transform_data()

            target_column_name = 'price'
            drop_columns = [target_column_name, 'id']

            # Split features and target
            input_feature_train_df = train_df.drop(columns=drop_columns, axis=1)
            target_feature_train_df = train_df[target_column_name]
               
            input_feature_test_df = test_df.drop(columns=drop_columns, axis=1)
            target_feature_test_df = test_df[target_column_name]

            # Apply transformations
            input_feature_train_arr = preprocessing_obj.fit_transform(input_feature_train_df)
            input_feature_test_arr = preprocessing_obj.transform(input_feature_test_df)

            print(f"Columns before transformation: {input_feature_train_df.columns}")

            # Convert arrays back to DataFrame for easy manipulation
            input_feature_train_arr_df = pd.DataFrame(input_feature_train_arr, columns=input_feature_train_df.columns)
            input_feature_test_arr_df = pd.DataFrame(input_feature_test_arr, columns=input_feature_test_df.columns)

            logging.info("Applying preprocessing object on training and testing datasets")

            # Combine transformed features with target values
            train_df = pd.concat([input_feature_train_arr_df, target_feature_train_df.reset_index(drop=True)], axis=1)
            test_df = pd.concat([input_feature_test_arr_df, target_feature_test_df.reset_index(drop=True)], axis=1)

            # Save the preprocessing object
            save_object(
                file_path=self.data_transformation_config.preprocessor_obj_file_path,
                obj=preprocessing_obj
            )

            logging.info("Preprocessing pickle file saved")

            return (
                train_df,
                test_df
            )

        except Exception as e:
            logging.error("Exception occurred in the initiate_data_transformation method")
            raise CustomException(e, sys)
