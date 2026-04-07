def create_features(df):
    df['risk_index'] = df['age'] * 0.3 + df['bmi'] * 0.5 + df['smoker'] * 10
    return df