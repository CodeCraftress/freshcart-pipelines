import numpy as np
from sklearn.datasets import load_iris

from iris_project.transformers.prepare_data import transform


def test_prepare_data():
    iris = load_iris()

    result = transform(iris)

    assert set(result.keys()) == {
        "X_train", "X_test", "y_train", "y_test"
    }

    assert len(result["X_train"]) == 120
    assert len(result["X_test"]) == 30

    assert len(result["y_train"]) == 120
    assert len(result["y_test"]) == 30

    assert result["X_train"].shape[1] == 4
    assert result["X_test"].shape[1] == 4

    assert len(np.unique(result["y_train"])) == 3
