# ============================================================
# 🎯 WEEK 1 COMPLETE PRACTICE: ML FOUNDATIONS (Days 31-37)
# ============================================================
# 
# This file covers ALL concepts from Week 1 in one complete project:
# - Day 31: ML Basics & Terminology
# - Day 32: Supervised Learning
# - Day 33-34: Bias & Variance
# - Day 35-36: Train-Test Split & Evaluation
# - Day 37: Regularization
#
# PROJECT: Complete House Price Prediction System
# ⏱️ TIME: 60-90 minutes
# ============================================================

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.preprocessing import StandardScaler, PolynomialFeatures
from sklearn.pipeline import make_pipeline
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

print("=" * 70)
print("🏠 WEEK 1 COMPLETE PROJECT: HOUSE PRICE PREDICTION SYSTEM")
print("=" * 70)
print("""
This project combines ALL Week 1 concepts:
✅ Day 31: Creating & exploring datasets
✅ Day 32: Supervised learning (regression)
✅ Day 33-34: Understanding bias & variance
✅ Day 35-36: Train-test split & evaluation metrics
✅ Day 37: Regularization techniques
""")

# ============================================================
# PART 1: DATA CREATION & EXPLORATION (Day 31)
# ============================================================
print("\n" + "=" * 70)
print("📊 PART 1: DATA CREATION & EXPLORATION (Day 31 Concepts)")
print("=" * 70)

# Create a realistic house price dataset
np.random.seed(42)
n_houses = 200

# Generate features
data = {
    # Main features (will affect price)
    'Area_sqft': np.random.randint(600, 4000, n_houses),
    'Bedrooms': np.random.randint(1, 6, n_houses),
    'Bathrooms': np.random.randint(1, 4, n_houses),
    'Age_years': np.random.randint(0, 50, n_houses),
    'Location_Score': np.random.randint(1, 10, n_houses),  # 1=bad, 10=great
    'Parking_Spaces': np.random.randint(0, 3, n_houses),
    'Has_Garden': np.random.choice([0, 1], n_houses),
    'Floor_Level': np.random.randint(0, 20, n_houses),
}

df = pd.DataFrame(data)

# Create realistic price based on features
# Price = base + (50 * area) + (25000 * bedrooms) + (15000 * bathrooms) 
#         - (2000 * age) + (20000 * location) + (15000 * parking) 
#         + (30000 * garden) + noise
df['Price'] = (
    50000 +  # Base price
    df['Area_sqft'] * 55 +
    df['Bedrooms'] * 25000 +
    df['Bathrooms'] * 18000 +
    df['Location_Score'] * 22000 +
    df['Parking_Spaces'] * 15000 +
    df['Has_Garden'] * 35000 -
    df['Age_years'] * 2500 -
    df['Floor_Level'] * 500 +
    np.random.normal(0, 25000, n_houses)  # Market noise
)

# Ensure no negative prices
df['Price'] = df['Price'].clip(lower=50000)

print("\n📋 DATASET CREATED:")
print(df.head(10))

print(f"""
📊 DATASET SUMMARY:
─────────────────────────────────────
Total Samples: {len(df)}
Number of Features: {len(df.columns) - 1}
Target Variable: Price

FEATURES (X):
{list(df.columns[:-1])}

LABEL (y):
Price
─────────────────────────────────────
""")

# Basic statistics
print("\n📈 DESCRIPTIVE STATISTICS:")
print(df.describe().round(2))

# Check for missing values
print(f"\n❓ Missing Values: {df.isnull().sum().sum()}")

# ============================================================
# PART 2: DATA VISUALIZATION (Day 31)
# ============================================================
print("\n" + "=" * 70)
print("📊 PART 2: DATA VISUALIZATION")
print("=" * 70)

fig, axes = plt.subplots(2, 3, figsize=(15, 10))

# Plot 1: Area vs Price
axes[0, 0].scatter(df['Area_sqft'], df['Price'], alpha=0.5, c='blue')
axes[0, 0].set_xlabel('Area (sqft)')
axes[0, 0].set_ylabel('Price ($)')
axes[0, 0].set_title('Area vs Price')

# Plot 2: Bedrooms vs Price
axes[0, 1].boxplot([df[df['Bedrooms']==i]['Price'] for i in range(1, 6)])
axes[0, 1].set_xlabel('Bedrooms')
axes[0, 1].set_ylabel('Price ($)')
axes[0, 1].set_title('Price by Bedrooms')

# Plot 3: Location Score vs Price
axes[0, 2].scatter(df['Location_Score'], df['Price'], alpha=0.5, c='green')
axes[0, 2].set_xlabel('Location Score')
axes[0, 2].set_ylabel('Price ($)')
axes[0, 2].set_title('Location vs Price')

# Plot 4: Price Distribution
axes[1, 0].hist(df['Price'], bins=30, color='orange', edgecolor='black')
axes[1, 0].set_xlabel('Price ($)')
axes[1, 0].set_ylabel('Count')
axes[1, 0].set_title('Price Distribution')

# Plot 5: Age vs Price
axes[1, 1].scatter(df['Age_years'], df['Price'], alpha=0.5, c='red')
axes[1, 1].set_xlabel('Age (years)')
axes[1, 1].set_ylabel('Price ($)')
axes[1, 1].set_title('Age vs Price')

# Plot 6: Correlation Heatmap (simplified)
corr = df.corr()['Price'].drop('Price').sort_values(ascending=True)
axes[1, 2].barh(corr.index, corr.values, color='purple')
axes[1, 2].set_xlabel('Correlation with Price')
axes[1, 2].set_title('Feature Correlations')
axes[1, 2].axvline(x=0, color='black', linestyle='-', linewidth=0.5)

plt.tight_layout()
plt.savefig('week1_eda.png', dpi=100)
plt.show()

print("✅ Visualization saved as 'week1_eda.png'")

# ============================================================
# PART 3: TRAIN-TEST SPLIT (Day 35)
# ============================================================
print("\n" + "=" * 70)
print("✂️ PART 3: TRAIN-TEST SPLIT (Day 35 Concepts)")
print("=" * 70)

# Separate features and target
X = df.drop('Price', axis=1)
y = df['Price']

# Split data: 80% train, 20% test
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

print(f"""
📦 DATA SPLIT:
─────────────────────────────────────
Total samples:    {len(df)}
Training samples: {len(X_train)} ({len(X_train)/len(df)*100:.0f}%)
Testing samples:  {len(X_test)} ({len(X_test)/len(df)*100:.0f}%)
─────────────────────────────────────

✅ Model will LEARN from {len(X_train)} houses
✅ Model will be TESTED on {len(X_test)} NEW houses
""")

# ============================================================
# PART 4: BUILD & COMPARE MODELS (Day 32, 33-34, 37)
# ============================================================
print("\n" + "=" * 70)
print("🏋️ PART 4: BUILD & COMPARE MODELS (Day 32, 33-34, 37 Concepts)")
print("=" * 70)

# Scale features (important for regularization)
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Define multiple models to compare
models = {
    'Linear Regression': LinearRegression(),
    'Ridge (alpha=0.1)': Ridge(alpha=0.1),
    'Ridge (alpha=1.0)': Ridge(alpha=1.0),
    'Ridge (alpha=10)': Ridge(alpha=10),
    'Lasso (alpha=0.1)': Lasso(alpha=0.1),
    'Lasso (alpha=1.0)': Lasso(alpha=1.0),
    'Lasso (alpha=10)': Lasso(alpha=10),
}

# Store results
results = []

print(f"\n{'Model':<25} {'Train R²':<12} {'Test R²':<12} {'MAE ($)':<15} {'Status'}")
print("-" * 80)

for name, model in models.items():
    # Train
    model.fit(X_train_scaled, y_train)
    
    # Predict
    y_train_pred = model.predict(X_train_scaled)
    y_test_pred = model.predict(X_test_scaled)
    
    # Calculate metrics
    train_r2 = r2_score(y_train, y_train_pred)
    test_r2 = r2_score(y_test, y_test_pred)
    mae = mean_absolute_error(y_test, y_test_pred)
    gap = train_r2 - test_r2
    
    # Determine status
    if gap > 0.1:
        status = "⚠️ Overfitting"
    elif train_r2 < 0.5:
        status = "⚠️ Underfitting"
    else:
        status = "✅ Good"
    
    print(f"{name:<25} {train_r2:<12.4f} {test_r2:<12.4f} ${mae:<14,.0f} {status}")
    
    results.append({
        'Model': name,
        'Train_R2': train_r2,
        'Test_R2': test_r2,
        'MAE': mae,
        'Gap': gap
    })

# ============================================================
# PART 5: BIAS-VARIANCE ANALYSIS (Day 33-34)
# ============================================================
print("\n" + "=" * 70)
print("📊 PART 5: BIAS-VARIANCE ANALYSIS (Day 33-34 Concepts)")
print("=" * 70)

# Compare simple vs complex models
print("""
🔍 BIAS-VARIANCE TRADEOFF DEMONSTRATION:

We'll compare 3 models of different complexity:
1. SIMPLE (Degree 1): May underfit (high bias)
2. MODERATE (Degree 2): Balanced
3. COMPLEX (Degree 4): May overfit (high variance)
""")

# Use only one feature for visualization
X_simple = df[['Area_sqft']].values
y_simple = df['Price'].values

X_train_s, X_test_s, y_train_s, y_test_s = train_test_split(
    X_simple, y_simple, test_size=0.2, random_state=42
)

print(f"\n{'Complexity':<20} {'Train R²':<12} {'Test R²':<12} {'Gap':<12} {'Diagnosis'}")
print("-" * 70)

fig, axes = plt.subplots(1, 3, figsize=(15, 5))
degrees = [1, 2, 4]
titles = ['Simple (Degree 1)', 'Moderate (Degree 2)', 'Complex (Degree 4)']
colors = ['red', 'green', 'orange']

for idx, (degree, title, color) in enumerate(zip(degrees, titles, colors)):
    # Create polynomial model
    poly_model = make_pipeline(
        PolynomialFeatures(degree),
        LinearRegression()
    )
    poly_model.fit(X_train_s, y_train_s)
    
    # Calculate scores
    train_r2 = r2_score(y_train_s, poly_model.predict(X_train_s))
    test_r2 = r2_score(y_test_s, poly_model.predict(X_test_s))
    gap = train_r2 - test_r2
    
    # Diagnosis
    if gap > 0.15:
        diagnosis = "High Variance"
    elif train_r2 < 0.3:
        diagnosis = "High Bias"
    else:
        diagnosis = "Balanced"
    
    print(f"{title:<20} {train_r2:<12.4f} {test_r2:<12.4f} {gap:<12.4f} {diagnosis}")
    
    # Plot
    axes[idx].scatter(X_train_s, y_train_s, alpha=0.5, label='Train', color='blue')
    axes[idx].scatter(X_test_s, y_test_s, alpha=0.5, label='Test', color='green')
    
    # Prediction line
    X_line = np.linspace(X_simple.min(), X_simple.max(), 100).reshape(-1, 1)
    y_line = poly_model.predict(X_line)
    axes[idx].plot(X_line, y_line, color=color, linewidth=2, label='Model')
    
    axes[idx].set_title(f'{title}\nTrain: {train_r2:.3f}, Test: {test_r2:.3f}')
    axes[idx].set_xlabel('Area (sqft)')
    axes[idx].set_ylabel('Price ($)')
    axes[idx].legend()

plt.tight_layout()
plt.savefig('week1_bias_variance.png', dpi=100)
plt.show()

print("\n✅ Bias-Variance comparison saved as 'week1_bias_variance.png'")

# ============================================================
# PART 6: MODEL EVALUATION (Day 36)
# ============================================================
print("\n" + "=" * 70)
print("📊 PART 6: DETAILED MODEL EVALUATION (Day 36 Concepts)")
print("=" * 70)

# Select best model (Ridge with alpha=1.0)
best_model = Ridge(alpha=1.0)
best_model.fit(X_train_scaled, y_train)

y_train_pred = best_model.predict(X_train_scaled)
y_test_pred = best_model.predict(X_test_scaled)

# Calculate all metrics
print("""
┌────────────────────────────────────────────────────────────────────┐
│                    BEST MODEL EVALUATION                           │
│                    (Ridge, alpha=1.0)                              │
├────────────────────────────────────────────────────────────────────┤
""")

# Training metrics
train_mae = mean_absolute_error(y_train, y_train_pred)
train_mse = mean_squared_error(y_train, y_train_pred)
train_rmse = np.sqrt(train_mse)
train_r2 = r2_score(y_train, y_train_pred)

# Test metrics
test_mae = mean_absolute_error(y_test, y_test_pred)
test_mse = mean_squared_error(y_test, y_test_pred)
test_rmse = np.sqrt(test_mse)
test_r2 = r2_score(y_test, y_test_pred)

print(f"""
│  TRAINING SET METRICS:                                             │
│  ─────────────────────                                             │
│  MAE:  ${train_mae:,.2f}                                          
│  RMSE: ${train_rmse:,.2f}                                         
│  R²:   {train_r2:.4f} ({train_r2*100:.1f}%)                        
│                                                                    │
│  TEST SET METRICS:                                                 │
│  ────────────────────                                              │
│  MAE:  ${test_mae:,.2f}                                           
│  RMSE: ${test_rmse:,.2f}                                          
│  R²:   {test_r2:.4f} ({test_r2*100:.1f}%)                          
│                                                                    │
│  COMPARISON:                                                       │
│  ───────────                                                       │
│  R² Gap: {train_r2 - test_r2:.4f} (smaller = better)              
│                                                                    │
└────────────────────────────────────────────────────────────────────┘
""")

# R² Interpretation
print("📌 R² INTERPRETATION:")
if test_r2 >= 0.9:
    print("   🌟 EXCELLENT - Model explains 90%+ of variance")
elif test_r2 >= 0.7:
    print("   ✅ STRONG - Good for production")
elif test_r2 >= 0.5:
    print("   🟡 MODERATE - May need improvement")
else:
    print("   🔴 WEAK - Consider different approach")

# ============================================================
# PART 7: FEATURE IMPORTANCE (Day 37)
# ============================================================
print("\n" + "=" * 70)
print("📊 PART 7: FEATURE IMPORTANCE (Day 37 Concepts)")
print("=" * 70)

# Get feature importance from coefficients
feature_names = X.columns.tolist()
coefficients = best_model.coef_

# Sort by absolute importance
importance_df = pd.DataFrame({
    'Feature': feature_names,
    'Coefficient': coefficients,
    'Abs_Importance': np.abs(coefficients)
}).sort_values('Abs_Importance', ascending=True)

print("\n📊 FEATURE IMPORTANCE (sorted by impact):")
print("-" * 50)
for _, row in importance_df.iterrows():
    direction = "↑" if row['Coefficient'] > 0 else "↓"
    print(f"   {row['Feature']:<20} {direction} {row['Coefficient']:>10.2f}")

# Visualize
plt.figure(figsize=(10, 6))
colors = ['green' if c > 0 else 'red' for c in importance_df['Coefficient']]
plt.barh(importance_df['Feature'], importance_df['Coefficient'], color=colors, alpha=0.7)
plt.xlabel('Coefficient Value (Impact on Price)', fontsize=12)
plt.title('Feature Importance (Green = Positive, Red = Negative)', fontsize=14)
plt.axvline(x=0, color='black', linestyle='-', linewidth=0.5)
plt.tight_layout()
plt.savefig('week1_feature_importance.png', dpi=100)
plt.show()

print("\n✅ Feature importance saved as 'week1_feature_importance.png'")

# ============================================================
# PART 8: MAKE PREDICTIONS
# ============================================================
print("\n" + "=" * 70)
print("🔮 PART 8: MAKE PREDICTIONS ON NEW HOUSES")
print("=" * 70)

# Create some new houses to predict
new_houses = pd.DataFrame({
    'Area_sqft': [1200, 2500, 1800, 3500],
    'Bedrooms': [2, 4, 3, 5],
    'Bathrooms': [1, 3, 2, 4],
    'Age_years': [5, 2, 15, 0],
    'Location_Score': [6, 9, 5, 10],
    'Parking_Spaces': [1, 2, 1, 3],
    'Has_Garden': [0, 1, 0, 1],
    'Floor_Level': [3, 5, 10, 1],
})

print("📋 NEW HOUSES TO PREDICT:")
print(new_houses)

# Scale and predict
new_houses_scaled = scaler.transform(new_houses)
predictions = best_model.predict(new_houses_scaled)

print("\n🔮 PRICE PREDICTIONS:")
print("-" * 60)
for i, (_, house) in enumerate(new_houses.iterrows()):
    print(f"""
   House {i+1}: {house['Area_sqft']} sqft, {house['Bedrooms']} bed, {house['Bathrooms']} bath
           Location: {house['Location_Score']}/10, Age: {house['Age_years']} years
           → Predicted Price: ${predictions[i]:,.2f}
""")

# ============================================================
# PART 9: VISUALIZATION OF PREDICTIONS
# ============================================================
print("\n" + "=" * 70)
print("📊 PART 9: FINAL VISUALIZATION")
print("=" * 70)

fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# Plot 1: Actual vs Predicted
axes[0].scatter(y_test, y_test_pred, alpha=0.6, color='blue', s=50)
axes[0].plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 
             'r--', linewidth=2, label='Perfect Prediction')
axes[0].set_xlabel('Actual Price ($)', fontsize=12)
axes[0].set_ylabel('Predicted Price ($)', fontsize=12)
axes[0].set_title(f'Actual vs Predicted (R² = {test_r2:.3f})', fontsize=14)
axes[0].legend()
axes[0].grid(True, alpha=0.3)

# Plot 2: Residuals
residuals = y_test - y_test_pred
axes[1].hist(residuals, bins=20, color='purple', edgecolor='black', alpha=0.7)
axes[1].axvline(x=0, color='red', linestyle='--', linewidth=2)
axes[1].set_xlabel('Prediction Error ($)', fontsize=12)
axes[1].set_ylabel('Count', fontsize=12)
axes[1].set_title('Distribution of Prediction Errors', fontsize=14)

plt.tight_layout()
plt.savefig('week1_final_results.png', dpi=100)
plt.show()

print("✅ Final results saved as 'week1_final_results.png'")

# ============================================================
# SUMMARY
# ============================================================
print("\n" + "=" * 70)
print("📋 WEEK 1 COMPLETE - SUMMARY")
print("=" * 70)

print(f"""
┌────────────────────────────────────────────────────────────────────┐
│                   WEEK 1 LEARNING SUMMARY                          │
├────────────────────────────────────────────────────────────────────┤
│                                                                    │
│  📚 DAY 31 - ML BASICS:                                            │
│     ✅ Created dataset with {n_houses} houses                        
│     ✅ Understood features (X) vs labels (y)                       │
│     ✅ Explored and visualized data                                │
│                                                                    │
│  📚 DAY 32 - SUPERVISED LEARNING:                                  │
│     ✅ Built regression models                                     │
│     ✅ Made predictions                                            │
│     ✅ Understood model.fit() and model.predict()                  │
│                                                                    │
│  📚 DAY 33-34 - BIAS & VARIANCE:                                   │
│     ✅ Compared simple vs complex models                           │
│     ✅ Identified overfitting vs underfitting                      │
│     ✅ Learned the bias-variance tradeoff                          │
│                                                                    │
│  📚 DAY 35-36 - EVALUATION:                                        │
│     ✅ Split data: {len(X_train)} train / {len(X_test)} test              
│     ✅ Calculated MAE, RMSE, R²                                    │
│     ✅ Best Model Test R²: {test_r2:.4f} ({test_r2*100:.1f}%)               
│                                                                    │
│  📚 DAY 37 - REGULARIZATION:                                       │
│     ✅ Compared Linear, Ridge, and Lasso                           │
│     ✅ Understood how regularization prevents overfitting          │
│     ✅ Analyzed feature importance                                 │
│                                                                    │
├────────────────────────────────────────────────────────────────────┤
│                                                                    │
│  🎯 KEY TAKEAWAYS:                                                 │
│  • Always split data into train/test sets                          │
│  • Compare train vs test scores to detect overfitting              │
│  • Use regularization (Ridge/Lasso) to improve generalization      │
│  • R² > 0.7 is generally good for production                       │
│  • Lower MAE/RMSE = Better predictions                             │
│                                                                    │
└────────────────────────────────────────────────────────────────────┘

🎉 CONGRATULATIONS! You've completed Week 1 of ML Foundations!
   You can now build, evaluate, and improve ML models!

📁 FILES CREATED:
   • week1_eda.png
   • week1_bias_variance.png
   • week1_feature_importance.png
   • week1_final_results.png
""")




