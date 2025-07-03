from networksecurity.entity.config_entity import DataTransformationConfig
from networksecurity.logging.logger import logging
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.constants.training_pipeline import TARGET_COLUMN
from networksecurity.constants.training_pipeline import DATA_TRANSFORMATION_IMPUTER_PARAMS
from networksecurity.entity.artifact_entity import (
    DataTransformationArtifact,
    DataValidationArtifact
)
import os
import sys
import numpy as np
import pandas as pd
from sklearn.impute import KNNImputer
from sklearn.pipeline import Pipeline
from networksecurity.utils.main_utils.utils import (
    save_numpy_array_data,
    save_object
)


class DataTransformation:
    def __init__(self, data_validation_artifact:DataValidationArtifact, data_transformation_config:DataTransformationConfig):
        try:
            self.data_validation_artifact = data_validation_artifact
            self.data_transformation_config = data_transformation_config

        except Exception as e:
            raise NetworkSecurityException(e, sys)
        

    def read_data(self, file_path):
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise NetworkSecurityException(e, sys)
        

    def get_data_transformer_object(cls):
        logging.info("Entered get_data_transformer_object")
        try:
            imputer=KNNImputer(**DATA_TRANSFORMATION_IMPUTER_PARAMS)
            logging.info(f"Initialize KNN Imputer with {DATA_TRANSFORMATION_IMPUTER_PARAMS}")
            processor=Pipeline(steps=[
                ("imputer", imputer)
            ])
            return processor
        except Exception as e:
            raise NetworkSecurityException(e, sys)


    def initiate_data_transformation(self):
        logging.info("Entered initiate_data_transformation")

        try:
            logging.info("Starting Data Transformation")
            train_data=self.read_data(file_path=self.data_validation_artifact.valid_train_file_path)
            test_data=self.read_data(file_path=self.data_validation_artifact.valid_test_file_path)

            # Training Dataframe
            input_feature_train_data_frame=train_data.drop(TARGET_COLUMN, axis=1)
            target_feature_train_data_frame=train_data[TARGET_COLUMN]
            target_feature_train_data_frame=target_feature_train_data_frame.replace(-1, 0)

            input_feature_test_data_frame=test_data.drop(TARGET_COLUMN, axis=1)
            target_feature_test_data_frame=test_data[TARGET_COLUMN]
            target_feature_test_data_frame=target_feature_test_data_frame.replace(-1, 0)

            preprocessor= self.get_data_transformer_object()  
            preprocessor_obj=preprocessor.fit(input_feature_train_data_frame)
            transform_input_train_feature=preprocessor_obj.transform(input_feature_train_data_frame)   

            transform_input_test_feature=preprocessor_obj.transform(input_feature_test_data_frame)

            train_arr = np.c_[transform_input_train_feature, np.array(target_feature_train_data_frame)]
            test_arr = np.c_[transform_input_test_feature, np.array(target_feature_test_data_frame)]

            save_numpy_array_data(self.data_transformation_config.transformed_train_file_path, array=train_arr)
            save_numpy_array_data(self.data_transformation_config.transformed_test_file_path, array=test_arr)
            save_object(file_path=self.data_transformation_config.transformed_object_file_path, obj=preprocessor_obj)
            data_transformation_artifact=DataTransformationArtifact(
                transformed_object_file_path=self.data_transformation_config.transformed_object_file_path,
                transformed_train_file_path=self.data_transformation_config.transformed_train_file_path,
                transformed_test_file_path=self.data_transformation_config.transformed_test_file_path
            )
            return data_transformation_artifact
            
        except Exception as e:
            raise NetworkSecurityException(e, sys)