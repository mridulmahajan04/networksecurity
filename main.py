from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.logging.logger import logging
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.entity.config_entity import DataIngestionConfig
from networksecurity.entity.config_entity import DataValidationConfig
from networksecurity.entity.config_entity import TrainingPipelineConfig
from networksecurity.components.data_validation import DataValidation
import os
import sys


if(__name__=='__main__'):
    try:
        logging.info("Inititate Data Ingestion")
        training_pipeline_config=TrainingPipelineConfig()
        data_ingestion_config=DataIngestionConfig(training_pipeline_config=training_pipeline_config)
        data_ingestion=DataIngestion(data_ingestion_config=data_ingestion_config)   
        dataingestionartifact=data_ingestion.initiate_data_ingestion()
        print(dataingestionartifact)

        logging.info("Data Initiation Completed")
        data_validation_config=DataValidationConfig(train_pipeline_config=training_pipeline_config)
        data_validation=DataValidation(dataingestionartifact, data_validation_config=data_validation_config)
        logging.info("Intitiate The data validation")
        data_validation_artifact=data_validation.inititate_data_validation()
        print(data_validation_artifact)
        logging.info("Data Validation Completed")


    except Exception as e:
        raise NetworkSecurityException(e, sys)
        

