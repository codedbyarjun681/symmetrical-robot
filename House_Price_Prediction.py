import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.datasets import fetch_california_housing
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error, r2_score
from xgboost import XGBRegressor

# 1. Load California Housing Dataset
housing = fetch_california_housing()
X = pd.DataFrame(housing.data, columns=housing.feature_names)
y = housing.target

# 2. Train-Test Split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 3. Feature Scaling
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# 4. Hyperparameter Tuning using GridSearchCV
param_grid = {
    'n_estimators': [50, 100, 150],
    'max_depth': [3, 4, 5],
    'learning_rate': [0.01, 0.1, 0.2]
}

xgb = XGBRegressor(random_state=42)
grid_search = GridSearchCV(estimator=xgb, param_grid=param_grid, cv=3, scoring='neg_mean_squared_error', verbose=1)
grid_search.fit(X_train_scaled, y_train)

# 5. Best Model
xgb_model = grid_search.best_estimator_

# 6. Predict & Evaluate
y_pred = xgb_model.predict(X_test_scaled)
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)
print(f"Mean Squared Error: {mse:.4f}")
print(f"R² Score: {r2:.4f}")

# 7. Combined Visualization (Subplots)
importances = xgb_model.feature_importances_
features = housing.feature_names
indices = np.argsort(importances)

fig, axs = plt.subplots(1, 2, figsize=(16, 6))

# Plot 1: Actual vs Predicted Prices
axs[0].scatter(y_test, y_pred, alpha=0.6, color='blue')
axs[0].plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], '--r', linewidth=2)
axs[0].set_xlabel("Actual Median House Value")
axs[0].set_ylabel("Predicted Median House Value")
axs[0].set_title("Actual vs Predicted House Prices")
axs[0].grid(True)

# Plot 2: Feature Importance
axs[1].barh(range(len(indices)), importances[indices], color="skyblue")
axs[1].set_yticks(range(len(indices)))
axs[1].set_yticklabels(np.array(features)[indices])
axs[1].set_title("Feature Importance (XGBoost)")
axs[1].set_xlabel("Relative Importance")

plt.tight_layout()
plt.show()
