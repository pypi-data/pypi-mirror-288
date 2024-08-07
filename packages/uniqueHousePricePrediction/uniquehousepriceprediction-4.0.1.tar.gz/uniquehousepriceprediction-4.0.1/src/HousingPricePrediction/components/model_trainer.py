import os
import sys

from dataclasses import dataclass
from sklearn.linear_model import LinearRegression, Ridge, Lasso, ElasticNet
from sklearn.model_selection import GridSearchCV

from src.HousingPricePrediction.logger import logging
from src.HousingPricePrediction.exception import CustomException
from src.HousingPricePrediction.utils.utils import save_object, load_object
from src.HousingPricePrediction.utils.utils import evaluate_model
from explainerdashboard import RegressionExplainer, ExplainerDashboard

@dataclass
class ModelTrainerConfig:
    """
    This is configuration class for Model Trainer
    """
    trained_model_file_path = os.path.join('artifacts', 'model.pkl')
    trained_model_report_path = os.path.join('artifacts', 'model_report.pkl')
    dashboard_file_path = os.path.join('artifacts', 'dashboard.yaml')
    explainer_file = os.path.join('explainer.joblib')

class ModelTrainer:
    """
    This class handles Model Training
    """
    def __init__(self):
        self.model_trainer_config = ModelTrainerConfig()
    
    def initiate_model_training(self, train_array, test_array):
        try:
            logging.info('Splitting Dependent and Independent variables from train and test data')
            X_train, y_train, X_test, y_test = (
                train_array.iloc[:, :-1],
                train_array.iloc[:, -1],
                test_array.iloc[:, :-1],
                test_array.iloc[:, -1]
            )

            models = {
                'LinearRegression': LinearRegression(),
                'Lasso': Lasso(),
                'Ridge': Ridge(),
                'ElasticNet': ElasticNet()
            }
            
            # Define hyperparameter grid for each model
            param_grid = {
                'LinearRegression': {},
                'Lasso': {'alpha': [0.1, 1, 10, 100]},
                'Ridge': {'alpha': [0.1, 1, 10, 100]},
                'ElasticNet': {'alpha': [0.1, 1, 10, 100], 'l1_ratio': [0.1, 0.5, 0.9]}
            }

            best_model = None
            best_model_name = None
            best_model_score = -float('inf')

            for model_name in models.keys():
                logging.info(f'Training {model_name} with hyperparameter tuning')
                grid_search = GridSearchCV(models[model_name], param_grid[model_name], scoring='r2', cv=5, n_jobs=-1)
                grid_search.fit(X_train, y_train)

                best_estimator = grid_search.best_estimator_
                best_score = grid_search.best_score_

                logging.info(f'{model_name} best score: {best_score} with params: {grid_search.best_params_}')
                
                if best_score > best_model_score:
                    best_model_score = best_score
                    best_model_name = model_name
                    best_model = best_estimator
            
            print(f'{model_name} best score: {best_score} with params: {grid_search.best_params_}')
            print('\n====================================================================================\n')
            print(f'Best Model Found, Model Name: {best_model_name}, R2 Score: {best_model_score}')
            print('\n====================================================================================\n')
            logging.info(f'Best Model Found, Model Name: {best_model_name}, R2 Score: {best_model_score}')
            
            # Create an explainer and dashboard for the best model
            explainer = RegressionExplainer(best_model, X_test, y_test)
            db = ExplainerDashboard(explainer, title="Housing Price Explainer Dashboard", shap_interaction=False)
            db.to_yaml(
                self.model_trainer_config.dashboard_file_path, 
                explainerfile=self.model_trainer_config.explainer_file,
                dump_explainer=True
            )

            # Save the best model and model report
            save_object(
                 file_path=self.model_trainer_config.trained_model_file_path,
                 obj=best_model
            )

            model_report = {
                best_model_name: best_model_score
            }
            save_object(
                 file_path=self.model_trainer_config.trained_model_report_path,
                 obj=model_report
            )
          
        except Exception as e:
            logging.error('Exception occurred during Model Training')
            raise CustomException(e, sys)
        
    def show_model_score(self):
        try:
            model_report = load_object(self.model_trainer_config.trained_model_report_path)
            logging.info(f'Model Report: {model_report}')

            # To get best model score from dictionary 
            best_model_score = max(sorted(model_report.values()))

            best_model_name = list(model_report.keys())[
                list(model_report.values()).index(best_model_score)
            ]

            logging.info(f'Best Model Found, Model Name: {best_model_name}, R2 Score: {best_model_score}')
            return best_model_score
        except Exception as e:
            logging.error('Exception occurred while showing model score')
            raise CustomException(e, sys)
