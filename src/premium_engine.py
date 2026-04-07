def calculate_premium(base, risk_score, loss_pred, fraud_flag):
    premium = base + (risk_score * 10000) + loss_pred
    if fraud_flag == -1:
        premium += 5000  # penalty
    return premium