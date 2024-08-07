from src.HousingPricePrediction.components.data_ingestion import DataIngestion
from src.HousingPricePrediction.components.data_transformation import DataTransformation
from src.HousingPricePrediction.components.model_trainer import ModelTrainer
from src.HousingPricePrediction.components.model_evaluation import ModelEvaluation
from dataclasses import dataclass


@dataclass
class TrainingPipeline:
    
    def start(self):
        # Data Ingestion
        data_ingestion = DataIngestion()
        train_data_path, test_data_path = data_ingestion.initiate_data_ingestion()

        # Data Transformation
        data_transformation = DataTransformation()
        train_arr, test_arr = data_transformation.initiate_data_transformation(train_data_path, test_data_path)

        # Model Training
        model_trainer = ModelTrainer()
        model_trainer.initiate_model_training(train_arr, test_arr)

        # Model Evaluation
        model_evaluation = ModelEvaluation()
        model_evaluation.initiate_model_evaluation(train_arr, test_arr)


if __name__ == '__main__':
    training_pipeline = TrainingPipeline()
    training_pipeline.start()
