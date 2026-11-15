import pandas as pd
from sklearn.metrics import confusion_matrix, accuracy_score, precision_score, recall_score, f1_score
if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test

@transformer
def evaluate(df, *args, **kwargs):
    labels = sorted(df['target'].unique())
    cm = confusion_matrix(df['target'], df['predicted'], labels=labels)
    print("Confusion matrix (rows=true, columns=predicted):")
    print(pd.DataFrame(cm, index=labels, columns=labels))
    metrics = pd.DataFrame([{
        'accuracy': accuracy_score(df['target'], df['predicted']),
        'precision_macro': precision_score(df['target'], df['predicted'], average='macro', zero_division=0),
        'recall_macro': recall_score(df['target'], df['predicted'], average='macro', zero_division=0),
        'f1_macro': f1_score(df['target'], df['predicted'], average='macro', zero_division=0),
    }])
    print("Metrics:")
    print(metrics.to_string(index=False))
    return df

@test
def test_evaluation(output, *args):
    assert 'predicted' in output.columns
    assert len(output) == 30
