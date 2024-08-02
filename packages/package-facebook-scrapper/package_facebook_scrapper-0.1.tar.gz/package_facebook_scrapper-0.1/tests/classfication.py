import streamlit as st
import pandas as pd
import numpy as np
import pickle
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier, VotingClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score


# Function to train and save the ensemble classifier
def train_and_save_ensemble_classifier(data, model_save_path, selected_classifiers):
    X = data[["mean_likes", "mean_comments", "mean_shares"]]
    y = data["label"]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, shuffle=True, random_state=45)

    # Initialize an empty list for classifiers
    classifiers = []

    # Add selected classifiers to the list
    for classifier in selected_classifiers:
        if classifier == "Logistic Regression":
            classifiers.append(('lr', LogisticRegression()))
        elif classifier == "K-Nearest Neighbors":
            classifiers.append(('knn', KNeighborsClassifier()))
        elif classifier == "Random Forest":
            classifiers.append(('rf', RandomForestClassifier()))
        elif classifier == "Decision Tree":
            classifiers.append(('dt', DecisionTreeClassifier()))
        elif classifier == "Gradient Boosting":
            classifiers.append(('gb', GradientBoostingClassifier()))

    # Create the ensemble classifier
    ensemble_classifier = VotingClassifier(estimators=classifiers, voting='soft')

    # Train the ensemble classifier
    ensemble_classifier.fit(X_train, y_train)

    # Predict using the trained model
    y_pred = ensemble_classifier.predict(X_test)
    y_pred_proba = ensemble_classifier.predict_proba(X_test)[:, 1]

    # Evaluate the model
    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred)
    recall = recall_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)
    roc_auc = roc_auc_score(y_test, y_pred_proba)

    # Save the trained model
    with open(model_save_path, 'wb') as model_file:
        pickle.dump(ensemble_classifier, model_file)

    # Calculate the mean of the metrics
    metrics = np.array([accuracy, precision, recall, f1, roc_auc])
    mean_metrics = np.mean(metrics)

    return {
        "accuracy": accuracy,
        "precision": precision,
        "recall": recall,
        "f1": f1,
        "roc_auc": roc_auc,
        "mean_metrics": mean_metrics,
        "model": ensemble_classifier
    }


def load_model_and_compute_metrics(model_save_path, data):
    data = pd.read_csv(data)
    X = data[["mean_likes", "mean_comments", "mean_shares"]]
    y = data["label"]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, shuffle=True, random_state=45)
    # Load the trained model
    with open(model_save_path, 'rb') as model_file:
        ensemble_classifier = pickle.load(model_file)

    # Predict using the loaded model
    y_pred = ensemble_classifier.predict(X_test)
    y_pred_proba = ensemble_classifier.predict_proba(X_test)[:, 1]

    # Evaluate the model
    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred)
    recall = recall_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)
    roc_auc = roc_auc_score(y_test, y_pred_proba)

    # Calculate the mean of the metrics
    metrics = np.array([accuracy, precision, recall, f1, roc_auc])
    mean_metrics = np.mean(metrics)

    return {
        "accuracy": accuracy,
        "precision": precision,
        "recall": recall,
        "f1": f1,
        "roc_auc": roc_auc,
        "mean_metrics": mean_metrics
    }


def load_model_and_predict(model_save_path, data):

    # Load the trained model
    with open(model_save_path, 'rb') as model_file:
        ensemble_classifier = pickle.load(model_file)

    # Make predictions using the loaded model
    X = data[["mean_likes", "mean_comments", "mean_shares"]]
    y_pred = ensemble_classifier.predict(X)
    y_pred_proba = ensemble_classifier.predict_proba(X)[:, 1]

    return y_pred, y_pred_proba