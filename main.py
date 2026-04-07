import pandas as pd
import numpy as np
from pathlib import Path

from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.cluster import KMeans
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import roc_auc_score


df = pd.read_csv("/Users/dishagaglani/Downloads/PROJ/insurance-intelligence-system/data/insurance.csv")
# Encode categorical
le = LabelEncoder()
df['sex'] = le.fit_transform(df['sex'])
df['smoker'] = le.fit_transform(df['smoker'])
df['region'] = le.fit_transform(df['region'])

# Create target (risk)
df['risk'] = (df['charges'] > df['charges'].median()).astype(int)

# Features
X = df.drop(['charges', 'risk'], axis=1)
y = df['risk']

# Scale
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# -------------------------
# Clustering
kmeans = KMeans(n_clusters=3, random_state=42)
df['cluster'] = kmeans.fit_predict(X_scaled)

# -------------------------
# Train model
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2)

model = RandomForestClassifier()
model.fit(X_train, y_train)

# Predictions
y_prob = model.predict_proba(X_test)[:,1]

print("ROC-AUC:", roc_auc_score(y_test, y_prob))

# -------------------------
# Risk score (FIXED)
df['risk_score'] = model.predict_proba(X_scaled)[:,1]

# -------------------------
# Premium logic
BASE_PREMIUM = 5000

def calculate_premium(risk):
    return BASE_PREMIUM + (risk * 10000)

df['premium'] = df['risk_score'].apply(calculate_premium)

# -------------------------
# Output
print(df[['age','bmi','risk_score','premium']].head())

# Group insight
print("\nAverage Premium by Cluster:")
print(df.groupby('cluster')['premium'].mean())

# -------------------------
# Load Allstate dataset

try:
    allstate_path = Path(__file__).resolve().parent / "/Users/dishagaglani/Downloads/PROJ/insurance-intelligence-system/data/train.csv"
    df_allstate = pd.read_csv(allstate_path)
except:
    print("Allstate dataset not found, skipping...")
    df_allstate = None

if df_allstate is not None:
    # Drop ID
    df_allstate = df_allstate.drop(['id'], axis=1)
    
    # Separate features & target
    X_all = df_allstate.drop(['loss'], axis=1)
    y_all = df_allstate['loss']
    
    # Encode categorical columns
    for col in X_all.columns:
        if X_all[col].dtype == 'object':
            X_all[col] = LabelEncoder().fit_transform(X_all[col])

from sklearn.ensemble import RandomForestRegressor

if df_allstate is not None:
    X_train_a, X_test_a, y_train_a, y_test_a = train_test_split(
        X_all, y_all, test_size=0.2, random_state=42
    )
    
    loss_model = RandomForestRegressor(n_estimators=50)
    loss_model.fit(X_train_a, y_train_a)
    
    print("Loss model trained successfully")

if df_allstate is not None:
    # Predict loss using average features
    sample_loss = loss_model.predict(X_all.sample(len(df), replace=True))
    df['predicted_loss'] = sample_loss
else:
    df['predicted_loss'] = 3000  # fallback

def calculate_premium(risk, cluster, loss):
    premium = BASE_PREMIUM + (risk * 8000)
    
    # Add expected loss
    premium += loss * 0.1
    
    # Cluster penalty
    if cluster == 2:
        premium += 2000
        
    return premium

df['premium'] = df.apply(
    lambda row: calculate_premium(
        row['risk_score'],
        row['cluster'],
        row['predicted_loss']
    ),
    axis=1
)
