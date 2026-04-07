from sklearn.ensemble import IsolationForest

def detect_fraud(X):
    model = IsolationForest(contamination=0.05)
    preds = model.fit_predict(X)
    return preds