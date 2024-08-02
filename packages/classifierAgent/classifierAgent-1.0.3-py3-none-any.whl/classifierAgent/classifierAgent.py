__author__ = "Adnan Karol"
__version__ = "1.0.3"
__maintainer__ = "Adnan Karol"
__email__ = "adnanmushtaq5@gmail.com"
__status__ = "PROD"

# Import Dependencies
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.svm import SVC
from sklearn.naive_bayes import GaussianNB, BernoulliNB
from sklearn.metrics import f1_score, accuracy_score, classification_report, confusion_matrix
from sklearn.preprocessing import MinMaxScaler, StandardScaler

import pandas as pd
import os
import matplotlib.pyplot as plt
import seaborn as sns
import joblib
from termcolor import colored
from datetime import datetime
import warnings

# Suppress warnings
warnings.filterwarnings('ignore')

def load_data(dataset):
    """
    Load data into a pandas DataFrame.

    Parameters:
    dataset (str or pd.DataFrame): Path to the dataset file or a pandas DataFrame.

    Returns:
    pd.DataFrame: Loaded data.
    """
    if isinstance(dataset, pd.DataFrame):
        return dataset

    if isinstance(dataset, str):
        file_extension = os.path.splitext(dataset)[1].lower()
        try:
            if file_extension == '.csv':
                print(colored("Loading dataset from CSV file...", "cyan"))
                return pd.read_csv(dataset)
            elif file_extension in ['.xlsx', '.xls']:
                print(colored("Loading dataset from Excel file...", "cyan"))
                return pd.read_excel(dataset)
            else:
                raise ValueError(f"Unsupported file extension: {file_extension}. Supported extensions are: 'csv', 'xlsx', 'xls'.")
        except Exception as e:
            raise ValueError(f"Failed to read file: {e}")

    raise TypeError("The dataset must be either a file path (str) or a pandas DataFrame.")

def scale_data(X_train, X_test, method):
    """
    Scale the data using the specified method.

    Parameters:
    X_train (pd.DataFrame): Training features.
    X_test (pd.DataFrame): Testing features.
    method (str): Scaling method ('minmax' or 'normalize').

    Returns:
    pd.DataFrame, pd.DataFrame: Scaled training and testing features.
    """
    if method == 'minmax':
        scaler = MinMaxScaler()
    elif method == 'normalize':
        scaler = StandardScaler()
    else:
        raise ValueError(f"Unsupported scaling method: {method}. Supported methods are: 'minmax', 'normalize'.")

    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    return pd.DataFrame(X_train_scaled, columns=X_train.columns), pd.DataFrame(X_test_scaled, columns=X_test.columns)

def plot_confusion_matrix(y_true, y_pred, model_name, show_plot=True):
    """
    Plot the confusion matrix for the given model.

    Parameters:
    y_true (pd.Series): True labels.
    y_pred (np.array): Predicted labels.
    model_name (str): Name of the model.
    show_plot (bool): Whether to display the plot or not.
    """
    cm = confusion_matrix(y_true, y_pred)
    plt.figure(figsize=(10, 7))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', cbar=False,
                xticklabels=['Negative', 'Positive'], yticklabels=['Negative', 'Positive'])
    plt.xlabel('Predicted')
    plt.ylabel('True')
    plt.title(f'Confusion Matrix for {model_name}')
    if show_plot:
        plt.show()

def classifierAgent(dataset, output_column, train_test_ratio, scaling_method=None, perform_grid_search=False, save_models=False, show_confusion_matrix=False, show_classification_report=False):
    """
    Trains multiple classifiers on the provided dataset and returns their performance metrics.
    
    Optionally performs grid search for hyperparameter tuning, saves models, and shows confusion matrix and classification report.

    Parameters:
    dataset (str or pd.DataFrame): Path to the dataset file (CSV or Excel) or a pandas DataFrame.
    output_column (str): Name of the column to be predicted.
    train_test_ratio (float): Ratio of the dataset to be used as the test set.
    scaling_method (str, optional): Method to scale the data ('minmax' or 'normalize').
    perform_grid_search (bool, optional): Whether to perform grid search for hyperparameter tuning.
    save_models (bool, optional): Whether to save the trained models.
    show_confusion_matrix (bool, optional): Whether to plot the confusion matrix.
    show_classification_report (bool, optional): Whether to print the classification report.

    Returns:
    pd.DataFrame: A DataFrame containing the classifier names, accuracy, F1-score, and optionally the best parameters.
    """
    # Validate train_test_ratio
    if not (0 < train_test_ratio < 1):
        raise ValueError("train_test_ratio must be between 0 and 1.")

    # Create models directory if not existing
    if save_models and not os.path.exists('models'):
        os.makedirs('models')

    # Load the dataset
    df = load_data(dataset)
    print(colored("Dataset loaded successfully!", "green"))

    # Split the dataset into features and target
    y = df[output_column]
    X = df.drop(output_column, axis=1)
    print(colored(f"Dataset split into features and target: {output_column}", "cyan"))

    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=train_test_ratio, random_state=42)
    print(colored("Training and testing sets created.", "cyan"))

    # Scale the data if a scaling method is provided
    if scaling_method:
        X_train, X_test = scale_data(X_train, X_test, scaling_method)
        print(colored(f"Data scaled using {scaling_method} method.", "cyan"))

    # List of models and their respective hyperparameter grids for grid search
    models_and_params = {
        'KNeighborsClassifier': {
            'model': KNeighborsClassifier(),
            'params': {'n_neighbors': [3, 5, 7], 'weights': ['uniform', 'distance']}
        },
        'LogisticRegression': {
            'model': LogisticRegression(),
            'params': {'C': [0.01, 0.1, 1, 10], 'solver': ['liblinear', 'saga']}
        },
        'DecisionTreeClassifier': {
            'model': DecisionTreeClassifier(),
            'params': {'criterion': ['gini', 'entropy'], 'max_depth': [None, 10, 20]}
        },
        'RandomForestClassifier': {
            'model': RandomForestClassifier(),
            'params': {'n_estimators': [100, 200], 'max_depth': [None, 10, 20]}
        },
        'GradientBoostingClassifier': {
            'model': GradientBoostingClassifier(),
            'params': {'n_estimators': [100, 200], 'learning_rate': [0.01, 0.1, 0.2]}
        },
        'SVC': {
            'model': SVC(),
            'params': {'C': [0.01, 0.1, 1, 10], 'kernel': ['linear', 'rbf']}
        },
        'GaussianNB': {
            'model': GaussianNB(),
            'params': {}
        },
        'BernoulliNB': {
            'model': BernoulliNB(),
            'params': {}
        }
    }

    # Initialize an empty DataFrame to store results
    results = pd.DataFrame(columns=["Classifier", "Accuracy", "F1-Score", "Best Parameters"])

    # Train and evaluate each model
    for model_name, config in models_and_params.items():
        model = config['model']
        params = config['params']
        
        try:
            print(colored(f"Training on Model: {model_name}", "yellow"))
            if perform_grid_search and params:
                grid_search = GridSearchCV(model, params, cv=5, scoring='accuracy')
                grid_search.fit(X_train, y_train)
                best_model = grid_search.best_estimator_
                best_params = grid_search.best_params_
                model = best_model
            else:
                model.fit(X_train, y_train)
                best_params = {}

            y_pred = model.predict(X_test)
            acc = accuracy_score(y_test, y_pred)
            f1score = f1_score(y_test, y_pred, average='weighted')
            new_result = pd.DataFrame({"Classifier": [model_name], "Accuracy": [acc], "F1-Score": [f1score], "Best Parameters": [best_params]})
            results = pd.concat([results, new_result], ignore_index=True)
            print(colored(f"Training on Model: {model_name} complete.", "green"))

            # Plot confusion matrix
            if show_confusion_matrix:
                plot_confusion_matrix(y_test, y_pred, model_name, show_plot=True)

            # Print classification report
            if show_classification_report:
                print(colored(f"Classification Report for {model_name}:\n{classification_report(y_test, y_pred)}", "cyan"))

            # Save the model if requested
            if save_models:
                model_filename = f"models/{model_name}_{datetime.now().strftime('%Y-%m-%d')}.pkl"
                joblib.dump(model, model_filename)
                print(colored(f"Model {model_name} saved as {model_filename}", "green"))

        except Exception as e:
            print(colored(f"Failed to train on Model: {model_name}. Error: {e}", "red"))

    print(colored("Training on multiple models complete. Returning results of training as a dataframe.", "green"))
    return results
