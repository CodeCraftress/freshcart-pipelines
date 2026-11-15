if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test

@transformer
def validate_iris(df, *args, **kwargs):
    assert not df.isna().any().any(), "Iris data contains missing values"
    assert df['target'].nunique() == 3, "Expected exactly 3 classes"
    print("Validation passed: no missing values and exactly 3 classes.")
    return df

@test
def test_iris_validation(output, *args):
    assert output.isna().sum().sum() == 0
    assert output['target'].nunique() == 3
