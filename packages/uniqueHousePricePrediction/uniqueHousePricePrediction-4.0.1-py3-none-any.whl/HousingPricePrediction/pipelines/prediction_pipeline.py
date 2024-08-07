import os
import sys
import pandas as pd
from dataclasses import dataclass

from src.HousingPricePrediction.logger import logging
from src.HousingPricePrediction.exception import CustomException
from src.HousingPricePrediction.utils.utils import load_object

@dataclass
class PredictPipeline:
    def predict(self, features):
        try:
            logging.info('Prediction Pipeline initiated')
            preprocessor_path = os.path.join("artifacts", "preprocessor.pkl")
            model_path = os.path.join("artifacts", "model.pkl")

            preprocessor = load_object(preprocessor_path)
            model = load_object(model_path)

            # Preprocess and scale data
            scaled_data = preprocessor.transform(features)

            pred = model.predict(scaled_data)
            logging.info('Predicted value: {}'.format(pred))
            
            return pred

        except Exception as e:
            raise CustomException(e, sys)
  

class CustomData:
    def __init__(self,
                 area: float,
                 bedrooms: float,
                 bathrooms: float,
                 stories: float,
                 mainroad: str,
                 guestroom: str,
                 basement: str,
                 hotwaterheating: str,
                 airconditioning: str,
                 parking: float,
                 prefarea: str,
                 furnishingstatus: str):
        self.area = area
        self.bedrooms = bedrooms
        self.bathrooms = bathrooms
        self.stories = stories
        self.mainroad = mainroad
        self.guestroom = guestroom
        self.basement = basement
        self.hotwaterheating = hotwaterheating
        self.airconditioning = airconditioning
        self.parking = parking
        self.prefarea = prefarea
        self.furnishingstatus = furnishingstatus
                
    def get_data_as_dataframe(self):
        try:
            custom_data_input_dict = {
                'area': [self.area],
                'bedrooms': [self.bedrooms],
                'bathrooms': [self.bathrooms],
                'stories': [self.stories],
                'mainroad': [self.mainroad],
                'guestroom': [self.guestroom],
                'basement': [self.basement],
                'hotwaterheating': [self.hotwaterheating],
                'airconditioning': [self.airconditioning],
                'parking': [self.parking],
                'prefarea': [self.prefarea],
                'furnishingstatus': [self.furnishingstatus]
            }
            df = pd.DataFrame(custom_data_input_dict)
            logging.info('Custom input is converted to Dataframe: \n{}'.format(df.head()))
            return df
        except Exception as e:
            logging.info('Exception Occured in prediction pipeline')
            raise CustomException(e, sys)
