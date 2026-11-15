from pathlib import Path
if 'data_exporter' not in globals():
    from mage_ai.data_preparation.decorators import data_exporter
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test

@data_exporter
def export_data(df, *args, **kwargs):
    path = Path('/content/iris_project/iris_predictions.csv')
    df.to_csv(path, index=False)
    print(f"Saved {len(df)} predictions to {path}")

@test
def test_export(output, *args):
    path = Path('/content/iris_project/iris_predictions.csv')
    assert path.exists()
    assert path.stat().st_size > 0
