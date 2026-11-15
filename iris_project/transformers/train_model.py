import joblib
from pathlib import Path
from sklearn.tree import DecisionTreeClassifier
if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test

FEATURES = ['sepal length (cm)', 'sepal width (cm)',
            'petal length (cm)', 'petal width (cm)']

@transformer
def train(df, *args, **kwargs):
    max_depth = int(kwargs.get('max_depth', 3))
    train_df = df[df['split'] == 'train']
    test_df = df[df['split'] == 'test'].copy()
    model = DecisionTreeClassifier(max_depth=max_depth, random_state=42)
    model.fit(train_df[FEATURES], train_df['target'])
    test_df['predicted'] = model.predict(test_df[FEATURES])
    accuracy = (test_df['predicted'] == test_df['target']).mean()
    test_df['test_accuracy'] = accuracy
    test_df['max_depth'] = max_depth
    print(f"max_depth={max_depth} | Test accuracy={accuracy:.4f}")
    joblib.dump(model, '/content/iris_project/iris_model.pkl')
    return test_df

@test
def test_accuracy(output, *args):
    accuracy = (output['predicted'] == output['target']).mean()
    assert accuracy >= 0.8, f"Model accuracy {accuracy:.3f} is below 80%"
