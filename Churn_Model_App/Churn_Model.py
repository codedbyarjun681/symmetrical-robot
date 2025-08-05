import os
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score
from sklearn.preprocessing import LabelEncoder, StandardScaler
from imblearn.over_sampling import SMOTE
import lightgbm as lgb
import joblib
import shap
import warnings

warnings.filterwarnings("ignore")

# Set path to dataset relative to this script
current_dir = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(current_dir, "Telco-Customer-Churn.csv")

# Load dataset
df = pd.read_csv(data_path)

# Drop customerID column
df.drop("customerID", axis=1, inplace=True)

# Replace empty/space in 'TotalCharges' and convert to numeric
df['TotalCharges'] = df['TotalCharges'].replace(" ", np.nan)
df['TotalCharges'] = pd.to_numeric(df['TotalCharges'])
df.dropna(inplace=True)

# Encode target column
df['Churn'] = df['Churn'].map({'Yes': 1, 'No': 0})

# Encode categorical features
cat_cols = df.select_dtypes(include='object').columns
le = LabelEncoder()
for col in cat_cols:
    df[col] = le.fit_transform(df[col])

# Split features and target
X = df.drop("Churn", axis=1)
y = df["Churn"]

# Save feature column names
feature_columns = X.columns.tolist()

# Handle class imbalance using SMOTE
smote = SMOTE(random_state=42)
X_resampled, y_resampled = smote.fit_resample(X, y)

# Train/test split
X_train, X_test, y_train, y_test = train_test_split(
    X_resampled, y_resampled, test_size=0.2, random_state=42
)

# Scale features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# LightGBM classifier with hyperparameter tuning
params = {
    'num_leaves': [15, 31],
    'learning_rate': [0.05, 0.1],
    'n_estimators': [100, 200],
    'max_depth': [5, 10]
}

model = lgb.LGBMClassifier(random_state=42)

grid = GridSearchCV(model, params, cv=3, scoring='roc_auc', verbose=1, n_jobs=-1)
grid.fit(X_train_scaled, y_train)

# Best model
best_model = grid.best_estimator_

# Evaluate
y_pred = best_model.predict(X_test_scaled)
y_proba = best_model.predict_proba(X_test_scaled)[:, 1]

print("Confusion Matrix:")
print(confusion_matrix(y_test, y_pred))
print("\nClassification Report:")
print(classification_report(y_test, y_pred))
print("ROC AUC Score:", roc_auc_score(y_test, y_proba))

# Save model and preprocessing artifacts
joblib.dump(best_model, os.path.join(current_dir, "lightgbm_churn_model.pkl"))
joblib.dump(scaler, os.path.join(current_dir, "scaler.pkl"))
joblib.dump(le, os.path.join(current_dir, "label_encoder.pkl"))
joblib.dump(feature_columns, os.path.join(current_dir, "feature_columns.pkl"))

# SHAP explainer (tree-based for LightGBM)
explainer = shap.Explainer(best_model)
joblib.dump(explainer, os.path.join(current_dir, "shap_explainer.pkl"))

print("\n✅ All model artifacts saved successfully in:", current_dir)
