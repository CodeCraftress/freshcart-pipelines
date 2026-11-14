from sklearn.model_selection import train_test_split
from mage_ai.data_preparation.decorators import transformer


@transformer
def transform(data, *args, **kwargs):
    """
    Split the Iris dataset into training and testing sets.

    Accepts a scikit-learn Iris dataset object or a dictionary
    containing data and target arrays.
    """
    if isinstance(data, dict):
        X = data["data"]
        y = data["target"]
    else:
        X = data.data
        y = data.target

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42,
        stratify=y
    )

    return {
        "X_train": X_train,
        "X_test": X_test,
        "y_train": y_train,
        "y_test": y_test
    }
