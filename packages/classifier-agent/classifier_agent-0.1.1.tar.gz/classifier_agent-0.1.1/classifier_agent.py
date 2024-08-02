__author__ = "Adnan Karol"
__version__ = "1.0.1"
__maintainer__ = "Adnan Karol"
__email__ = "adnanmushtaq5@gmail.com"
__status__ = "PROD"

# Import Dependencies
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.svm import SVC
from sklearn.naive_bayes import GaussianNB, BernoulliNB, MultinomialNB
from sklearn.metrics import f1_score, accuracy_score

import pandas as pd

def classifier_agent(dataset_path, output_column, train_test_ratio):
    """
    Trains multiple classifiers on the provided dataset and returns their performance metrics.

    Parameters:
    dataset_path (str): Path to the dataset file (CSV or Excel).
    output_column (str): Name of the column to be predicted.
    train_test_ratio (float): Ratio of the dataset to be used as the test set.

    Returns:
    pd.DataFrame: A dataframe containing the classifier names, accuracy, and F1-score.
    """
    # Initialize an empty DataFrame to store results
    results = pd.DataFrame(columns=["Classifier", "Accuracy", "F1-Score"])

    # Load the dataset
    try:
        df = pd.read_csv(dataset_path)
    except Exception as e:
        print(f"Failed to read CSV file: {e}. Trying to read as Excel file.")
        try:
            df = pd.read_excel(dataset_path)
        except Exception as e:
            print(f"Failed to read Excel file: {e}.")
            return results

    # Split the dataset into features and target
    y = df[output_column]
    X = df.drop(output_column, axis=1)

    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=train_test_ratio, random_state=42)

    # List of models to train
    list_of_models = [
        KNeighborsClassifier(), LogisticRegression(max_iter=1000), DecisionTreeClassifier(),
        RandomForestClassifier(), GradientBoostingClassifier(), SVC(), GaussianNB(),
        BernoulliNB(), MultinomialNB()
    ]

    # Train and evaluate each model
    for model in list_of_models:
        model_name = model.__class__.__name__
        try:
            print(f"Training on Model: {model_name}")
            model.fit(X_train, y_train)
            y_pred = model.predict(X_test)
            acc = accuracy_score(y_test, y_pred)
            f1score = f1_score(y_test, y_pred, average='weighted')
            results = results.append({"Classifier": model_name, "Accuracy": acc, "F1-Score": f1score}, ignore_index=True)
        except Exception as e:
            print(f"Failed to Train on Model: {model_name}. Error: {e}")

    print("Training on multiple models complete. Returning results of training as a dataframe.")
    return results
