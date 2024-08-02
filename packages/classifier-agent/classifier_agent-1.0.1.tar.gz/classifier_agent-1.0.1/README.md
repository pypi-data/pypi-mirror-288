# Machine Learning Classification Python Package

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Scikit-Learn](https://img.shields.io/badge/scikit_learn-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white)

## Overview

This Python package provides a comprehensive solution for performing classification tasks using various popular machine learning algorithms. It allows you to read a dataset, preprocess it, train multiple classifiers, perform hyperparameter tuning, and visualize model performance. Additionally, it provides options for scaling data, saving trained models, and customizing the output display.

## Features

1. **Classification Algorithms**:
   - Logistic Regression
   - K-Nearest Neighbors
   - Decision Tree
   - Random Forest
   - Gradient Boosting
   - Support Vector Classifier
   - Gaussian Naive Bayes
   - Bernoulli Naive Bayes

2. **Advanced Functionality**:
   - **Data Scaling**: Options for Min-Max Scaling or Standard Normalization.
   - **Hyperparameter Tuning**: Option to perform Grid Search for finding the best model parameters.
   - **Model Persistence**: Save and load trained models using `joblib`.
   - **Visualization**: Option to plot confusion matrices and detailed classification reports.
   - **Cross-Validation**: Evaluate models using cross-validation scores.
   - **Configurable Outputs**: Options to control the display of confusion matrices and classification reports.

3. **Results**:
   - Returns a DataFrame with model names, accuracy, F1-score, and optionally the best hyperparameters.

## Parameters

The package takes the following parameters as input:
- `dataset`: Path to the CSV or Excel dataset file or a pandas DataFrame.
- `output_column`: Name of the output column containing the target variable.
- `train_test_ratio`: Ratio in which the dataset is divided into train and test splits (must be between 0 and 1).
- `scaling_method` (optional): Method to scale the data ('minmax' or 'normalize').
- `perform_grid_search` (optional): Whether to perform grid search for hyperparameter tuning (default is `False`).
- `save_models` (optional): Whether to save trained models to disk (default is `False`).
- `show_confusion_matrix` (optional): Whether to display confusion matrix plots (default is `False`).
- `show_classification_report` (optional): Whether to print classification reports (default is `False`).

## Installation

Make sure you have Python installed on your system. You can install the package using pip:

```sh
pip install classifier_agent
```

## Usage

Here's an example of how to use the package:

```python
from classifier_agent import classifier_agent

dataset_path = "diabetes.csv"
output_column = "Outcome"
train_test_ratio = 0.25
scaling_method = 'minmax'  # Choose 'minmax' or 'normalize'
perform_grid_search = True  # Whether to perform grid search
save_models = True  # Whether to save models
show_confusion_matrix = True  # Whether to plot the confusion matrix
show_classification_report = True  # Whether to print the classification report

results = classifier_agent(dataset_path, output_column, train_test_ratio, scaling_method, perform_grid_search, save_models, show_confusion_matrix, show_classification_report)
print(results)
```

## Example Output

The output is a DataFrame that looks like this:

| Classifier              | Accuracy | F1-Score | Best Parameters |
|-------------------------|----------|----------|-----------------|
| KNeighborsClassifier    | 0.78     | 0.76     | {'n_neighbors': 5, 'weights': 'uniform'} |
| LogisticRegression      | 0.80     | 0.79     | {'C': 0.1, 'solver': 'liblinear'} |
| DecisionTreeClassifier  | 0.72     | 0.70     | {'criterion': 'entropy', 'max_depth': 20} |
| RandomForestClassifier  | 0.85     | 0.84     | {'n_estimators': 200, 'max_depth': 20} |
| GradientBoostingClassifier | 0.83 | 0.82     | {'n_estimators': 200, 'learning_rate': 0.1} |
| SVC                     | 0.81     | 0.80     | {'C': 1, 'kernel': 'rbf'} |
| GaussianNB              | 0.75     | 0.73     | {} |
| BernoulliNB             | 0.73     | 0.72     | {} |

## Notes

- The package is actively developed and may receive updates.
- The project is developed with Python version `3.10`.
- If you encounter any issues or have questions, feel free to contact me on [LinkedIn](https://www.linkedin.com/in/adnan-karol-aa1666179/).

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Publishing to PyPI

To publish this package to PyPI, follow these steps:

1. **Ensure Your Package is Ready:**
   - Make sure your `setup.py` and `README.md` are correctly configured.
   - Verify that your package is properly structured and tested.

2. **Create Distribution Archives:**
   Run the following command to create distribution archives of your package:
   ```sh
   python setup.py sdist bdist_wheel
   ```

3. **Install Twine:**
   If you haven't already, install Twine, a utility for publishing packages to PyPI:
   ```sh
   pip install twine
   ```

4. **Upload to PyPI:**
   Use Twine to upload your package to PyPI:
   ```sh
   twine upload dist/*
   ```
   You will be prompted to enter your PyPI username and password.

5. **Verify Upload:**
   After uploading, check your package on [PyPI](https://pypi.org/) to ensure it appears correctly.

For more detailed instructions, refer to the [PyPI documentation](https://packaging.python.org/tutorials/packaging-projects/).