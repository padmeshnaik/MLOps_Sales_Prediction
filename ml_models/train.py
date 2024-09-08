from sklearn.ensemble import RandomForestRegressor
import pickle
import pandas as pd

def train():
    df = pd.read_csv('/tmp/preprocessed_train.csv')
    X = df[['feature1', 'feature2']]  # Your features
    y = df['target']  # Your target

    model = RandomForestRegressor()
    model.fit(X, y)

    with open('/tmp/model.pkl', 'wb') as f:
        pickle.dump(model, f)
