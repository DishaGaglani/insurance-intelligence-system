import pandas as pd
from sklearn.preprocessing import LabelEncoder

def preprocess_customer(df):
    le = LabelEncoder()
    df['sex'] = le.fit_transform(df['sex'])
    df['smoker'] = le.fit_transform(df['smoker'])
    df['region'] = le.fit_transform(df['region'])
    return df