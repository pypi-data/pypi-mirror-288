# Import necessary libraries
import pytest
import joblib
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import os

@pytest.fixture
def load_data():
    iris = load_iris()
    X, y = iris.data, iris.target
    _, X_test, _, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
    return X_test, y_test


@pytest.fixture
def load_model():
    knn_model = joblib.load('src/knn_model.joblib')
    scaler = joblib.load('src/scaler.joblib')
    
    return knn_model, scaler

def test_model_performance(load_data, load_model):
    X_test, y_test = load_data
    knn_model, scaler = load_model

    # Standardize features using the loaded scaler
    X_test = scaler.transform(X_test)

    # Predict the labels for the test set
    y_pred = knn_model.predict(X_test)

    # Calculate performance metrics
    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred, average='weighted')
    recall = recall_score(y_test, y_pred, average='weighted')
    f1 = f1_score(y_test, y_pred, average='weighted')

    # Print the performance metrics
    print(f'Accuracy: {accuracy:.4f}')
    print(f'Precision: {precision:.4f}')
    print(f'Recall: {recall:.4f}')
    print(f'F1 Score: {f1:.4f}')

    # Assert statements to validate the results
    assert accuracy > 0.9, f'Accuracy {accuracy} is below the expected threshold'
    assert precision > 0.9, f'Precision {precision} is below the expected threshold'
    assert recall > 0.9, f'Recall {recall} is below the expected threshold'
    assert f1 > 0.9, f'F1 Score {f1} is below the expected threshold'

    print('All assertions passed.')
