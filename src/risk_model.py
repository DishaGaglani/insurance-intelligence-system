from sklearn.ensemble import RandomForestClassifier

def train_risk_model(X, y):
    model = RandomForestClassifier()
    model.fit(X, y)
    return model