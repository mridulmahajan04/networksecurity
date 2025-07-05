import sys
import os
from networksecurity.entity.artifact_entity import ClassificationMetricArtifact
from networksecurity.logging.logger import logging
from networksecurity.exception.exception import NetworkSecurityException
from sklearn.metrics import recall_score, precision_score, f1_score

def get_classification_score(y_true, y_pred):
    try:
        model_f1_score=f1_score(y_true, y_pred)
        model_precision_score=precision_score(y_true, y_pred)
        model_recall_score=recall_score(y_true, y_pred)
        classification_artifact=ClassificationMetricArtifact(
            f1_score=model_f1_score,
            precision_score=model_precision_score,
            recall_score=model_recall_score
        )
        return classification_artifact
    except Exception as e:
        raise NetworkSecurityException(e, sys)