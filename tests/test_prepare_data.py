import pandas as pd
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split

def test_iris_prepare_data_split():
    df = load_iris(as_frame=True).frame.dropna().copy()
    train_df, test_df = train_test_split(
        df, test_size=0.2, random_state=42, stratify=df["target"]
    )
    assert len(train_df) == 120
    assert len(test_df) == 30
    assert set(train_df["target"].unique()) == {0, 1, 2}
    assert set(test_df["target"].unique()) == {0, 1, 2}
