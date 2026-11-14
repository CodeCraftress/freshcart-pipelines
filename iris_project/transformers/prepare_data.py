
try:
    from mage_ai.data_preparation.decorators import transformer
except ImportError:
    def transformer(func):
        return func

from sklearn.model_selection import train_test_split


@transformer
def transform(data, *args, **kwargs):
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
