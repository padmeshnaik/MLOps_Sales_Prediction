from sklearn.ensemble import RandomForestRegressor
import pickle
import pandas as pd

def train():
    df = pd.read_csv('/tmp/preprocessed_train.csv')
    X = df[['Item_MRP', 'Item_Weight','Outlet_Establishment_Year']]  # Define your features
    y = df['Item_Outlet_Sales'] 

    model = RandomForestRegressor()
    model.fit(X, y)

    with open('/tmp/model.pkl', 'wb') as f:
        pickle.dump(model, f)
