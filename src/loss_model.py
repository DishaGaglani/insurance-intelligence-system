from sklearn.ensemble import RandomForestRegressor

def train_loss_model(X, y):
    model = RandomForestRegressor()
    model.fit(X, y)
    return model