import unittest
import pandas as pd
from io import StringIO
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier, \
    GradientBoostingClassifier, VotingClassifier
from sklearn.tree import DecisionTreeClassifier
import pickle
from classfication import \
    train_and_save_ensemble_classifier, \
    load_model_and_compute_metrics, load_model_and_predict


class TestEnsembleClassifier(unittest.TestCase):
    def setUp(self):
        # Sample data for testing
        self.data = pd.DataFrame({
            "mean_likes":
                [10, 20, 30, 40, 50, 60, 70, 80, 90, 100],
            "mean_comments": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
            "mean_shares": [5, 6, 7, 8, 9, 10, 11, 12, 13, 14],
            "label": [0, 0, 0, 1, 1, 1, 0, 0, 1, 1]
        })
        self.model_save_path = "test_model.pkl"

    def test_train_and_save_ensemble_classifier(self):
        selected_classifiers = ["Logistic Regression", "Random Forest"]
        result = train_and_save_ensemble_classifier(self.data, self.model_save_path, selected_classifiers)

        self.assertIn("accuracy", result)
        self.assertIn("precision", result)
        self.assertIn("recall", result)
        self.assertIn("f1", result)
        self.assertIn("roc_auc", result)
        self.assertIn("mean_metrics", result)
        self.assertTrue(isinstance(result["model"], VotingClassifier))
        with open(self.model_save_path, 'rb') as model_file:
            loaded_model = pickle.load(model_file)
            self.assertTrue(isinstance(loaded_model, VotingClassifier))

    def test_load_model_and_compute_metrics(self):
        # train and save the model
        selected_classifiers = ["Logistic Regression", "Random Forest"]
        train_and_save_ensemble_classifier(self.data, self.model_save_path, selected_classifiers)
        # Test the load_model_and_compute_metrics function
        metrics = load_model_and_compute_metrics(self.model_save_path, StringIO(self.data.to_csv(index=False)))
        self.assertIn("accuracy", metrics)
        self.assertIn("precision", metrics)
        self.assertIn("recall", metrics)
        self.assertIn("f1", metrics)
        self.assertIn("roc_auc", metrics)
        self.assertIn("mean_metrics", metrics)

    def test_load_model_and_predict(self):
        #  train and save the model
        selected_classifiers = ["Logistic Regression", "Random Forest"]
        train_and_save_ensemble_classifier(self.data, self.model_save_path, selected_classifiers)
        # Test the load_model_and_predict function
        y_pred, y_pred_proba = load_model_and_predict(self.model_save_path, self.data)
        self.assertEqual(len(y_pred), len(self.data))
        self.assertEqual(len(y_pred_proba), len(self.data))

    def test_model_performance(self):
        # Ensure the trained model has reasonable performance
        selected_classifiers = ["Logistic Regression", "Random Forest"]
        result = train_and_save_ensemble_classifier(self.data, self.model_save_path, selected_classifiers)
        self.assertGreaterEqual(result["accuracy"], 0.5)
        self.assertGreaterEqual(result["precision"], 0.5)
        self.assertGreaterEqual(result["recall"], 0.5)
        self.assertGreaterEqual(result["f1"], 0.5)
        self.assertGreaterEqual(result["roc_auc"], 0.5)

    def test_ensemble_classifier_types(self):
        # Test with all types of classifiers
        selected_classifiers = \
            ["Logistic Regression", "K-Nearest Neighbors",
             "Random Forest", "Decision Tree",
             "Gradient Boosting"]
        result = train_and_save_ensemble_classifier(self.data, self.model_save_path, selected_classifiers)

        self.assertTrue(any(isinstance(est, (
            LogisticRegression, KNeighborsClassifier,
            RandomForestClassifier, DecisionTreeClassifier,
            GradientBoostingClassifier))
                            for _, est in result["model"].estimators))


if __name__ == '__main__':
    unittest.main()
