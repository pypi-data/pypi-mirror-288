import os
import sys

import mlflow
import mlflow.sklearn
import numpy as np

from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from urllib.parse import urlparse
from dataclasses import dataclass

from src.HousingPricePrediction.utils.utils import load_object, CustomException

@dataclass
class ModelEvaluation:

    def eval_metrics(self, actual, pred):
        rmse = np.sqrt(mean_squared_error(actual, pred))
        mae = mean_absolute_error(actual, pred)
        r2 = r2_score(actual, pred)
        return rmse, mae, r2
    
    def initiate_model_evaluation(self, train_array, test_array):
        try:
            X_test, y_test = (test_array.iloc[:, :-1], test_array.iloc[:, -1])
            model_path = os.path.join("artifacts", "model.pkl")
            model = load_object(model_path)

            tracking_url_type=urlparse(mlflow.get_tracking_uri()).scheme
            print(tracking_url_type)

            with mlflow.start_run():
                predicted_prices = model.predict(X_test)

                (rmse, mae, r2) = self.eval_metrics(actual=y_test, pred=predicted_prices)

                mlflow.log_metric("rmse", rmse)
                mlflow.log_metric("mae", mae)
                mlflow.log_metric("r2", r2)

                mlflow.sklearn.log_model(model, "model")

                if tracking_url_type != "file":
                    mlflow.sklearn.log_model(model, "model", registered_model_name="ml_model")
                else:
                    mlflow.sklearn.log_model(model, "model")

        except Exception as e:
            raise CustomException(e, sys)
