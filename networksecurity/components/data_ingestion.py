from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
# Config of Data Ingestion Config
from networksecurity.entity.config_entity import DataIngestionConfig
from networksecurity.entity.artifact_entity import DataIngestionArtifact
import os
import sys
import pymongo
from typing import List
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split

from dotenv import load_dotenv
load_dotenv()

MONGO_DB_URL=os.getenv('MONGO_DB_URL')

class DataIngestion:
    def __init__(self, data_ingestion_config:DataIngestionConfig):
        try:
            self.data_ingestion_config=data_ingestion_config
        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
    def export_collection_as_dataframe(self):
        try:
            database_name=self.data_ingestion_config.database_name
            collection_name=self.data_ingestion_config.collection_name 
            self.mongo_client=pymongo.MongoClient(MONGO_DB_URL)
            collection=self.mongo_client[database_name][collection_name]

            df=pd.DataFrame(list(collection.find()))
            if "_id" in df.columns.to_list():
                df.drop(columns='_id', axis=1, inplace=True)

            df.replace({"na":np.nan}, inplace=True)
            return df
        except Exception as e:
            raise NetworkSecurityException(e, sys)


    def export_data_into_feature_store(self, dataframe:pd.DataFrame):
        try:
            feature_store_file_path=self.data_ingestion_config.feature_store_file_path
            dir_path=os.path.dirname(feature_store_file_path)
            os.makedirs(dir_path, exist_ok=True)
            dataframe.to_csv(feature_store_file_path, index=False, header=True)
            return dataframe
        
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def split_train_test_split(self, dataframe:pd.DataFrame):
        try:
            train_set, test_set = train_test_split(dataframe, test_size=self.data_ingestion_config.train_test_split_ratio)
            logging.info("Performed Train Test split on Dataset")
            logging.info("Exited Split _data_as_train_test method")

            dir_path=os.path.dirname(self.data_ingestion_config.training_file_path)
            os.makedirs(dir_path, exist_ok=True)
            logging.info("Exporting train and test file path")
            train_set.to_csv(
                self.data_ingestion_config.training_file_path, index=False, header=True
            )

            test_set.to_csv(
                self.data_ingestion_config.ingested_test_file_path, index=False, header=True
            )
            logging.info("Exported train and test data")
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def initiate_data_ingestion(self):
        try:
            dataframe=self.export_collection_as_dataframe() #Read From MongoDb
            dataframe=self.export_data_into_feature_store(dataframe=dataframe) #Store to feature_store
            self.split_train_test_split(dataframe=dataframe) #Create a train and test csv
            data_ingestion_artifact=DataIngestionArtifact(self.data_ingestion_config.training_file_path, self.data_ingestion_config.ingested_test_file_path)

            return data_ingestion_artifact
        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
    