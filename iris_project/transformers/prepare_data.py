import pandas as pd
from sklearn.model_selection import train_test_split
if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test

@transformer
def transform(df, *args, **kwargs):
    df = df.dropna().copy()
    train_df, test_df = train_test_split(
        df, test_size=0.2, random_state=42, stratify=df['target']
    )
    train_df['split'] = 'train'
    test_df['split'] = 'test'
    result = pd.concat([train_df, test_df]).sort_index()
    print("Train rows:", len(train_df), "| Test rows:", len(test_df))
    return result

@test
def test_output(output, *args):
    assert 'split' in output.columns
    assert (output['split'] == 'train').sum() == 120
    assert (output['split'] == 'test').sum() == 30
