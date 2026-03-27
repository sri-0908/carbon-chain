import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error
import joblib
import os

# Create data directory if not exists
os.makedirs('data', exist_ok=True)

# Mock data generation (as requested in the prompt)
np.random.seed(42)
n_samples = 1000

satellite_data = {
    'red_band': np.random.rand(n_samples) * 255,
    'green_band': np.random.rand(n_samples) * 255,
    'blue_band': np.random.rand(n_samples) * 255,
    'nir_band': np.random.rand(n_samples) * 255,  # Near-infrared
    'swir_band': np.random.rand(n_samples) * 255,  # Short-wave infrared
    'ndvi': np.random.rand(n_samples),  # Normalized Diff Vegetation Index
    'soil_moisture': np.random.rand(n_samples) * 100,
    'temperature': np.random.rand(n_samples) * 30,
    'precipitation': np.random.rand(n_samples) * 200,
    'latitude': np.random.rand(n_samples) * 180 - 90,
    'longitude': np.random.rand(n_samples) * 360 - 180,
}

df = pd.DataFrame(satellite_data)

# Target: CO2 tons per hectare (derived from NDVI + biomass relationship)
df['co2_sequestered'] = (
    df['ndvi'] * 50 +  # Vegetation index strongly predicts biomass
    df['soil_moisture'] * 0.3 +  # Soil health matters
    df['temperature'] * 0.5 +  # Climate zone matters
    np.random.randn(n_samples) * 10  # noise
)

print(f"Training dataset shape: {df.shape}")
print(f"CO2 range: {df['co2_sequestered'].min():.1f} - {df['co2_sequestered'].max():.1f} tons/ha")

# Prepare features and target
X = df[['red_band', 'green_band', 'blue_band', 'nir_band', 'swir_band', 
         'ndvi', 'soil_moisture', 'temperature', 'precipitation', 
         'latitude', 'longitude']]
y = df['co2_sequestered']

# Train/test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train GradientBoostingRegressor (using GradientBoostingRegressor as a stable alternative to XGBoost if not installed, but let's stick to the prompt's preference)
# The prompt mentioned XGBoost but the code example used GradientBoostingRegressor. I'll use GBR as it's part of scikit-learn.
model = GradientBoostingRegressor(
    n_estimators=200,
    learning_rate=0.1,
    max_depth=7,
    min_samples_split=5,
    min_samples_leaf=2,
    random_state=42,
    verbose=1
)

model.fit(X_train, y_train)

# Evaluate
y_pred = model.predict(X_test)
r2 = r2_score(y_test, y_pred)
mae = mean_absolute_error(y_test, y_pred)
rmse = np.sqrt(mean_squared_error(y_test, y_pred))
mape = np.mean(np.abs((y_test - y_pred) / y_test)) * 100

print(f"\n=== MODEL PERFORMANCE ===")
print(f"R² Score: {r2:.4f}")
print(f"MAE: {mae:.2f} tons CO2/ha")
print(f"RMSE: {rmse:.2f} tons CO2/ha")
print(f"MAPE: {mape:.2f}%")

# Feature importance
importance = pd.DataFrame({
    'feature': X.columns,
    'importance': model.feature_importances_
}).sort_values('importance', ascending=False)

print(f"\n=== FEATURE IMPORTANCE ===")
print(importance)

# Save model
joblib.dump(model, 'backend/agbp_model.pkl')
print("\n✓ Model saved to backend/agbp_model.pkl")
