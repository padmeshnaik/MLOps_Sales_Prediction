import pandas as pd

def preprocess():
    df = pd.read_csv('/tmp/train.csv')
    df.fillna(0, inplace=True)
    df.to_csv('/tmp/preprocessed_train.csv', index=False)
