# ============================================================
# 📘 DAY 35-36 PRACTICE: Train-Test Split & Model Evaluation
# ============================================================
# 
# 🎯 LEARNING GOALS:
# - Understand Train-Test Split
# - Learn evaluation metrics (MAE, MSE, RMSE, R²)
# - Practice proper model evaluation
# - Interpret model performance
#
# ⏱️ TIME: 45-60 minutes
# ============================================================

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

print("=" * 60)
print("📘 DAY 35-36: TRAIN-TEST SPLIT & MODEL EVALUATION")
print("=" * 60)

# ============================================================
# STEP 1: WHY SPLIT DATA?
# ============================================================
print("\n" + "=" * 60)
print("🎓 STEP 1: WHY DO WE SPLIT DATA?")
print("=" * 60)

print("""
┌─────────────────────────────────────────────────────────────┐
│                  WHY SPLIT DATA?                            │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  PROBLEM:                                                   │
│  If we test on the SAME data we trained on, the model      │
│  might just MEMORIZE the answers (cheating!)                │
│                                                             │
│  SOLUTION:                                                  │
│  Split data into:                                           │
│  • TRAINING SET (70-80%): Model LEARNS from this            │
│  • TEST SET (20-30%): Model is EVALUATED on this            │
│                                                             │
│  ANALOGY:                                                   │
│  • Training = Studying with textbook                        │
│  • Testing = Taking an exam with NEW questions              │
│                                                             │
└─────────────────────────────────────────────────────────────┘
""")

# ============================================================
# STEP 2: CREATE A DATASET
# ============================================================
print("\n" + "=" * 60)
print("📊 STEP 2: CREATE HOUSE PRICE DATASET")
print("=" * 60)

np.random.seed(42)

# Create realistic house data
n_samples = 100

data = {
    'Area_sqft': np.random.randint(800, 3500, n_samples),
    'Bedrooms': np.random.randint(1, 6, n_samples),
    'Age_years': np.random.randint(0, 30, n_samples),
}

df = pd.DataFrame(data)

# Create price based on features + noise
# Price = 50*Area + 15000*Bedrooms - 2000*Age + noise
df['Price'] = (
    df['Area_sqft'] * 50 +
    df['Bedrooms'] * 15000 -
    df['Age_years'] * 2000 +
    np.random.normal(0, 20000, n_samples)
)

print("📋 House Price Dataset:")
print(df.head(10))
print(f"\nTotal samples: {len(df)}")

# ============================================================
# STEP 3: PERFORM TRAIN-TEST SPLIT
# ============================================================
print("\n" + "=" * 60)
print("✂️ STEP 3: TRAIN-TEST SPLIT")
print("=" * 60)

# Separate features and target
X = df[['Area_sqft', 'Bedrooms', 'Age_years']]
y = df['Price']

# Split: 80% training, 20% testing
X_train, X_test, y_train, y_test = train_test_split(
    X, y, 
    test_size=0.2,      # 20% for testing
    random_state=42     # For reproducibility
)

print(f"""
📦 DATA SPLIT RESULTS:
─────────────────────────────────────────
Total samples:    {len(df)}
Training samples: {len(X_train)} ({len(X_train)/len(df)*100:.0f}%)
Testing samples:  {len(X_test)} ({len(X_test)/len(df)*100:.0f}%)
─────────────────────────────────────────
""")

print("📊 Training Features (first 5):")
print(X_train.head())

print("\n📊 Testing Features (first 5):")
print(X_test.head())

# ============================================================
# STEP 4: TRAIN THE MODEL
# ============================================================
print("\n" + "=" * 60)
print("🏋️ STEP 4: TRAIN THE MODEL")
print("=" * 60)

model = LinearRegression()
model.fit(X_train, y_train)  # Train ONLY on training data!

print("✅ Model trained on TRAINING data only!")
print(f"""
📈 What the model learned:
   Price = {model.coef_[0]:.2f}×Area + {model.coef_[1]:.2f}×Bedrooms + {model.coef_[2]:.2f}×Age + {model.intercept_:.2f}
""")

# ============================================================
# STEP 5: MAKE PREDICTIONS
# ============================================================
print("\n" + "=" * 60)
print("🔮 STEP 5: MAKE PREDICTIONS")
print("=" * 60)

# Predict on BOTH train and test
y_train_pred = model.predict(X_train)
y_test_pred = model.predict(X_test)

print("📊 Predictions on TEST set (first 10):")
comparison = pd.DataFrame({
    'Actual': y_test.head(10).values,
    'Predicted': y_test_pred[:10].round(0),
    'Error': (y_test.head(10).values - y_test_pred[:10]).round(0)
})
print(comparison.to_string(index=False))

# ============================================================
# STEP 6: EVALUATION METRICS
# ============================================================
print("\n" + "=" * 60)
print("📊 STEP 6: EVALUATION METRICS")
print("=" * 60)

print("""
┌─────────────────────────────────────────────────────────────┐
│               REGRESSION EVALUATION METRICS                 │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  1. MAE (Mean Absolute Error):                              │
│     → Average of |actual - predicted|                       │
│     → "On average, predictions are off by $X"               │
│     → LOWER is better                                       │
│                                                             │
│  2. MSE (Mean Squared Error):                               │
│     → Average of (actual - predicted)²                      │
│     → Punishes large errors MORE                            │
│     → LOWER is better                                       │
│                                                             │
│  3. RMSE (Root Mean Squared Error):                         │
│     → √MSE                                                  │
│     → Same units as target variable                         │
│     → LOWER is better                                       │
│                                                             │
│  4. R² Score (Coefficient of Determination):                │
│     → How much variance the model explains                  │
│     → Range: 0 to 1 (1 = perfect)                           │
│     → HIGHER is better                                      │
│                                                             │
└─────────────────────────────────────────────────────────────┘
""")

# Calculate metrics
def evaluate_model(y_true, y_pred, set_name):
    """Calculate and display evaluation metrics"""
    mae = mean_absolute_error(y_true, y_pred)
    mse = mean_squared_error(y_true, y_pred)
    rmse = np.sqrt(mse)
    r2 = r2_score(y_true, y_pred)
    
    print(f"\n📈 {set_name} SET METRICS:")
    print("-" * 50)
    print(f"   MAE:  ${mae:,.2f}")
    print(f"   MSE:  {mse:,.2f}")
    print(f"   RMSE: ${rmse:,.2f}")
    print(f"   R²:   {r2:.4f} ({r2*100:.1f}%)")
    
    return mae, mse, rmse, r2

train_metrics = evaluate_model(y_train, y_train_pred, "TRAINING")
test_metrics = evaluate_model(y_test, y_test_pred, "TEST")

# ============================================================
# STEP 7: INTERPRET THE RESULTS
# ============================================================
print("\n" + "=" * 60)
print("🔍 STEP 7: INTERPRET THE RESULTS")
print("=" * 60)

train_r2 = train_metrics[3]
test_r2 = test_metrics[3]
gap = train_r2 - test_r2

print(f"""
📊 COMPARISON:
─────────────────────────────────────────
Training R²: {train_r2:.4f} ({train_r2*100:.1f}%)
Testing R²:  {test_r2:.4f} ({test_r2*100:.1f}%)
Gap:         {gap:.4f} ({gap*100:.1f}%)
─────────────────────────────────────────
""")

# Diagnose
print("🔍 DIAGNOSIS:")
if train_r2 < 0.5 and test_r2 < 0.5:
    print("   ⚠️ HIGH BIAS (Underfitting)")
    print("   → Both scores are low")
    print("   → Model is too simple")
elif gap > 0.15:
    print("   ⚠️ HIGH VARIANCE (Overfitting)")
    print("   → Large gap between train and test")
    print("   → Model memorized training data")
else:
    print("   ✅ GOOD FIT!")
    print("   → Both scores are reasonable")
    print("   → Small gap between train and test")

# R² interpretation
print(f"\n📌 R² INTERPRETATION (Test R² = {test_r2:.2f}):")
if test_r2 >= 0.9:
    print("   🌟 EXCELLENT - Model explains 90%+ of variance")
elif test_r2 >= 0.7:
    print("   ✅ STRONG - Good for production")
elif test_r2 >= 0.5:
    print("   🟡 MODERATE - May need improvement")
else:
    print("   🔴 WEAK - Consider different approach")

# ============================================================
# STEP 8: VISUALIZE PREDICTIONS
# ============================================================
print("\n" + "=" * 60)
print("📊 STEP 8: VISUALIZE PREDICTIONS")
print("=" * 60)

fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# Plot 1: Actual vs Predicted
axes[0].scatter(y_test, y_test_pred, alpha=0.6, color='blue')
axes[0].plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 
             'r--', linewidth=2, label='Perfect Prediction')
axes[0].set_xlabel('Actual Price ($)', fontsize=12)
axes[0].set_ylabel('Predicted Price ($)', fontsize=12)
axes[0].set_title(f'Actual vs Predicted (R² = {test_r2:.3f})', fontsize=14)
axes[0].legend()
axes[0].grid(True, alpha=0.3)

# Plot 2: Residuals (Errors)
residuals = y_test - y_test_pred
axes[1].scatter(y_test_pred, residuals, alpha=0.6, color='green')
axes[1].axhline(y=0, color='red', linestyle='--', linewidth=2)
axes[1].set_xlabel('Predicted Price ($)', fontsize=12)
axes[1].set_ylabel('Residual (Error)', fontsize=12)
axes[1].set_title('Residual Plot', fontsize=14)
axes[1].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('day35_36_evaluation.png', dpi=100)
plt.show()

print("✅ Evaluation plots saved as 'day35_36_evaluation.png'")

# ============================================================
# STEP 9: DIFFERENT SPLIT SIZES
# ============================================================
print("\n" + "=" * 60)
print("🔬 STEP 9: EXPERIMENT WITH DIFFERENT SPLIT SIZES")
print("=" * 60)

print(f"{'Test Size':<15} {'Train Samples':<15} {'Test Samples':<15} {'Test R²'}")
print("-" * 60)

for test_size in [0.1, 0.2, 0.3, 0.4]:
    X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=test_size, random_state=42)
    
    model_temp = LinearRegression()
    model_temp.fit(X_tr, y_tr)
    y_pred_temp = model_temp.predict(X_te)
    r2_temp = r2_score(y_te, y_pred_temp)
    
    print(f"{test_size*100:.0f}%{'':<12} {len(X_tr):<15} {len(X_te):<15} {r2_temp:.4f}")

print("""
📌 OBSERVATIONS:
- Smaller test size → More training data → Better model
- But too small test size → Unreliable evaluation
- Common practice: 20-30% for testing
""")

# ============================================================
# STEP 10: PRACTICE EXERCISE
# ============================================================
print("\n" + "=" * 60)
print("💪 STEP 10: YOUR TURN - PRACTICE EXERCISE")
print("=" * 60)

print("""
🎯 EXERCISE: Evaluate a Model

Given these metrics:
- Training MAE: $15,000
- Training R²: 0.92
- Test MAE: $45,000
- Test R²: 0.68

Questions:
1. Is the model overfitting or underfitting?
2. How much worse is test performance vs training?
3. What would you do to improve?

ANSWER BELOW:
""")

print("""
✅ ANSWERS:

1. The model is OVERFITTING
   - Training R² (0.92) >> Test R² (0.68)
   - Training MAE ($15K) << Test MAE ($45K)
   - Big gap indicates memorization of training data

2. Performance comparison:
   - R² dropped by: 0.92 - 0.68 = 0.24 (24 percentage points)
   - MAE increased by: $45K - $15K = $30K (3x worse!)

3. To improve:
   - Get more training data
   - Use regularization (Ridge/Lasso)
   - Simplify the model
   - Remove irrelevant features
   - Use cross-validation
""")

# ============================================================
# SUMMARY
# ============================================================
print("\n" + "=" * 60)
print("📋 DAY 35-36 SUMMARY")
print("=" * 60)

print("""
✅ What you learned today:

1. TRAIN-TEST SPLIT:
   - Training (70-80%): Model learns
   - Testing (20-30%): Model evaluated
   - NEVER evaluate on training data!

2. EVALUATION METRICS:
   - MAE: Average absolute error (LOWER = better)
   - MSE: Squared error (LOWER = better)
   - RMSE: √MSE, same units (LOWER = better)
   - R²: Variance explained (HIGHER = better, max 1.0)

3. INTERPRETATION:
   - Compare train vs test scores
   - Small gap = good generalization
   - Large gap = overfitting
   - Both low = underfitting

4. PYTHON CODE:
   - train_test_split(X, y, test_size=0.2)
   - mean_absolute_error(y_true, y_pred)
   - r2_score(y_true, y_pred)

🎉 Great job mastering model evaluation!
""")


