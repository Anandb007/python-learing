# ============================================================
# 📘 DAY 37 PRACTICE: Regularization
# ============================================================
# 
# 🎯 LEARNING GOALS:
# - Understand what regularization is
# - Learn Ridge (L2) and Lasso (L1)
# - See how regularization prevents overfitting
# - Compare regularized vs non-regularized models
#
# ⏱️ TIME: 45-60 minutes
# ============================================================

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression, Ridge, Lasso, ElasticNet
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error, r2_score

print("=" * 60)
print("📘 DAY 37: REGULARIZATION")
print("=" * 60)

# ============================================================
# STEP 1: WHAT IS REGULARIZATION?
# ============================================================
print("\n" + "=" * 60)
print("🎓 STEP 1: WHAT IS REGULARIZATION?")
print("=" * 60)

print("""
┌─────────────────────────────────────────────────────────────┐
│                    REGULARIZATION                           │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  PROBLEM:                                                   │
│  Complex models can OVERFIT (memorize training data)        │
│                                                             │
│  SOLUTION: REGULARIZATION                                   │
│  Add a PENALTY for model complexity                         │
│                                                             │
│  HOW IT WORKS:                                              │
│  Normal: Minimize (prediction error)                        │
│  Regularized: Minimize (error + penalty for large weights)  │
│                                                             │
│  EFFECT:                                                    │
│  → Keeps weights small                                      │
│  → Prevents overfitting                                     │
│  → Better generalization                                    │
│                                                             │
│  ANALOGY:                                                   │
│  Like keeping a kid's toy collection small                  │
│  → Too many toys = confusion                                │
│  → Limited toys = better focus                              │
│                                                             │
└─────────────────────────────────────────────────────────────┘
""")

# ============================================================
# STEP 2: TYPES OF REGULARIZATION
# ============================================================
print("\n" + "=" * 60)
print("📚 STEP 2: TYPES OF REGULARIZATION")
print("=" * 60)

print("""
┌─────────────────────────────────────────────────────────────┐
│               TYPES OF REGULARIZATION                       │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  1. L1 (LASSO):                                             │
│     → Penalty = sum of |weights|                            │
│     → Can make weights EXACTLY ZERO                         │
│     → Good for FEATURE SELECTION                            │
│     → "Removes" unimportant features                        │
│                                                             │
│  2. L2 (RIDGE):                                             │
│     → Penalty = sum of weights²                             │
│     → SHRINKS weights (but not to zero)                     │
│     → Keeps ALL features, just smaller                      │
│     → Most commonly used                                    │
│                                                             │
│  3. ELASTIC NET (L1 + L2):                                  │
│     → Combines both penalties                               │
│     → Best of both worlds                                   │
│                                                             │
└─────────────────────────────────────────────────────────────┘

Summary:
┌───────────┬────────────────────────┬─────────────────────┐
│ Method    │ What it does           │ Best for            │
├───────────┼────────────────────────┼─────────────────────┤
│ Lasso (L1)│ Removes features       │ Feature selection   │
│ Ridge (L2)│ Shrinks all weights    │ General use         │
│ ElasticNet│ Both                   │ Many features       │
└───────────┴────────────────────────┴─────────────────────┘
""")

# ============================================================
# STEP 3: CREATE A DATASET
# ============================================================
print("\n" + "=" * 60)
print("📊 STEP 3: CREATE DATASET WITH MANY FEATURES")
print("=" * 60)

np.random.seed(42)
n_samples = 100

# Create dataset with many features (some useful, some not)
data = {
    'Area': np.random.randint(800, 3500, n_samples),
    'Bedrooms': np.random.randint(1, 6, n_samples),
    'Age': np.random.randint(0, 30, n_samples),
    'Location_Score': np.random.randint(1, 10, n_samples),
    'Parking': np.random.randint(0, 3, n_samples),
    # Less useful features (noise)
    'Random1': np.random.normal(0, 1, n_samples),
    'Random2': np.random.normal(0, 1, n_samples),
    'Random3': np.random.normal(0, 1, n_samples),
}

df = pd.DataFrame(data)

# Price based mainly on first few features
df['Price'] = (
    df['Area'] * 50 +
    df['Bedrooms'] * 20000 +
    df['Location_Score'] * 15000 -
    df['Age'] * 3000 +
    df['Parking'] * 10000 +
    np.random.normal(0, 15000, n_samples)  # Noise
)

print("📋 Dataset with 8 features:")
print(df.head())
print(f"\nTotal samples: {len(df)}")
print(f"Features: {list(df.columns[:-1])}")

# ============================================================
# STEP 4: PREPARE DATA
# ============================================================
print("\n" + "=" * 60)
print("⚙️ STEP 4: PREPARE DATA")
print("=" * 60)

# Features and target
X = df.drop('Price', axis=1)
y = df['Price']

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# IMPORTANT: Scale features for regularization
# Regularization is sensitive to feature scales
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

print(f"Training samples: {len(X_train)}")
print(f"Testing samples: {len(X_test)}")
print("\n✅ Features scaled (important for regularization!)")

# ============================================================
# STEP 5: COMPARE MODELS
# ============================================================
print("\n" + "=" * 60)
print("🔬 STEP 5: COMPARE DIFFERENT MODELS")
print("=" * 60)

# Define models
models = {
    'Linear Regression (No Regularization)': LinearRegression(),
    'Ridge (L2, alpha=1)': Ridge(alpha=1.0),
    'Ridge (L2, alpha=10)': Ridge(alpha=10.0),
    'Lasso (L1, alpha=1)': Lasso(alpha=1.0),
    'Lasso (L1, alpha=10)': Lasso(alpha=10.0),
    'ElasticNet (alpha=1)': ElasticNet(alpha=1.0, l1_ratio=0.5),
}

print(f"{'Model':<45} {'Train R²':<12} {'Test R²':<12} {'Gap'}")
print("-" * 80)

results = []
for name, model in models.items():
    model.fit(X_train_scaled, y_train)
    
    train_r2 = r2_score(y_train, model.predict(X_train_scaled))
    test_r2 = r2_score(y_test, model.predict(X_test_scaled))
    gap = train_r2 - test_r2
    
    print(f"{name:<45} {train_r2:<12.4f} {test_r2:<12.4f} {gap:.4f}")
    results.append({'Model': name, 'Train_R2': train_r2, 'Test_R2': test_r2, 'Gap': gap})

print("""
📌 OBSERVATIONS:
- Regularized models may have slightly lower training R²
- But often have BETTER or similar test R² (better generalization)
- Smaller gap = better model
""")

# ============================================================
# STEP 6: EFFECT OF ALPHA (REGULARIZATION STRENGTH)
# ============================================================
print("\n" + "=" * 60)
print("📈 STEP 6: EFFECT OF ALPHA (REGULARIZATION STRENGTH)")
print("=" * 60)

alphas = [0.001, 0.01, 0.1, 1, 10, 100, 1000]
train_scores = []
test_scores = []

print(f"{'Alpha':<15} {'Train R²':<15} {'Test R²':<15}")
print("-" * 45)

for alpha in alphas:
    ridge = Ridge(alpha=alpha)
    ridge.fit(X_train_scaled, y_train)
    
    train_r2 = r2_score(y_train, ridge.predict(X_train_scaled))
    test_r2 = r2_score(y_test, ridge.predict(X_test_scaled))
    
    train_scores.append(train_r2)
    test_scores.append(test_r2)
    
    print(f"{alpha:<15} {train_r2:<15.4f} {test_r2:<15.4f}")

# Plot
plt.figure(figsize=(10, 6))
plt.plot(alphas, train_scores, 'b-o', label='Training R²', linewidth=2, markersize=8)
plt.plot(alphas, test_scores, 'r-s', label='Test R²', linewidth=2, markersize=8)
plt.xscale('log')
plt.xlabel('Alpha (Regularization Strength)', fontsize=12)
plt.ylabel('R² Score', fontsize=12)
plt.title('Effect of Regularization Strength (Ridge)', fontsize=14)
plt.legend(fontsize=11)
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('day37_alpha_effect.png', dpi=100)
plt.show()

print("\n✅ Plot saved as 'day37_alpha_effect.png'")

print("""
📌 INTERPRETATION:
- Very LOW alpha (0.001): Almost no regularization
- OPTIMAL alpha: Best test performance (balance)
- Very HIGH alpha (1000): Too much regularization (underfits)
""")

# ============================================================
# STEP 7: FEATURE WEIGHTS COMPARISON
# ============================================================
print("\n" + "=" * 60)
print("📊 STEP 7: COMPARE FEATURE WEIGHTS")
print("=" * 60)

# Train models
lr = LinearRegression().fit(X_train_scaled, y_train)
ridge = Ridge(alpha=1.0).fit(X_train_scaled, y_train)
lasso = Lasso(alpha=100).fit(X_train_scaled, y_train)  # Higher alpha for Lasso to see effect

feature_names = X.columns.tolist()

print(f"{'Feature':<20} {'Linear':<15} {'Ridge':<15} {'Lasso'}")
print("-" * 65)

for i, feat in enumerate(feature_names):
    lr_w = lr.coef_[i]
    ridge_w = ridge.coef_[i]
    lasso_w = lasso.coef_[i]
    
    # Highlight if Lasso made it zero
    marker = " ← REMOVED" if abs(lasso_w) < 0.01 else ""
    print(f"{feat:<20} {lr_w:<15.2f} {ridge_w:<15.2f} {lasso_w:<.2f}{marker}")

print("""
📌 KEY INSIGHT:
- Linear Regression: All weights can be large
- Ridge: All weights shrunk (but none zero)
- Lasso: Some weights become EXACTLY ZERO (feature selection!)
- Notice: Random features have smaller weights or removed!
""")

# Visualize weights
fig, axes = plt.subplots(1, 3, figsize=(15, 5))

# Linear Regression weights
axes[0].barh(feature_names, lr.coef_, color='blue', alpha=0.7)
axes[0].set_title('Linear Regression\n(No Regularization)', fontsize=12)
axes[0].set_xlabel('Weight')
axes[0].axvline(x=0, color='black', linestyle='-', linewidth=0.5)

# Ridge weights
axes[1].barh(feature_names, ridge.coef_, color='green', alpha=0.7)
axes[1].set_title('Ridge (L2)\nalpha=1.0', fontsize=12)
axes[1].set_xlabel('Weight')
axes[1].axvline(x=0, color='black', linestyle='-', linewidth=0.5)

# Lasso weights
axes[2].barh(feature_names, lasso.coef_, color='orange', alpha=0.7)
axes[2].set_title('Lasso (L1)\nalpha=100', fontsize=12)
axes[2].set_xlabel('Weight')
axes[2].axvline(x=0, color='black', linestyle='-', linewidth=0.5)

plt.tight_layout()
plt.savefig('day37_weights.png', dpi=100)
plt.show()

print("✅ Weight comparison saved as 'day37_weights.png'")

# ============================================================
# STEP 8: PRACTICAL CODE REFERENCE
# ============================================================
print("\n" + "=" * 60)
print("💻 STEP 8: PRACTICAL CODE REFERENCE")
print("=" * 60)

print("""
┌─────────────────────────────────────────────────────────────┐
│                    CODE REFERENCE                           │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  # Import                                                   │
│  from sklearn.linear_model import Ridge, Lasso, ElasticNet  │
│  from sklearn.preprocessing import StandardScaler           │
│                                                             │
│  # IMPORTANT: Scale features first!                         │
│  scaler = StandardScaler()                                  │
│  X_train_scaled = scaler.fit_transform(X_train)             │
│  X_test_scaled = scaler.transform(X_test)                   │
│                                                             │
│  # Ridge (L2)                                               │
│  ridge = Ridge(alpha=1.0)                                   │
│  ridge.fit(X_train_scaled, y_train)                         │
│  predictions = ridge.predict(X_test_scaled)                 │
│                                                             │
│  # Lasso (L1)                                               │
│  lasso = Lasso(alpha=1.0)                                   │
│  lasso.fit(X_train_scaled, y_train)                         │
│                                                             │
│  # ElasticNet (L1 + L2)                                     │
│  elastic = ElasticNet(alpha=1.0, l1_ratio=0.5)              │
│  # l1_ratio: 0=Ridge, 1=Lasso, 0.5=equal mix                │
│                                                             │
│  # View weights                                             │
│  print(model.coef_)                                         │
│                                                             │
└─────────────────────────────────────────────────────────────┘
""")

# ============================================================
# STEP 9: PRACTICE EXERCISE
# ============================================================
print("\n" + "=" * 60)
print("💪 STEP 9: YOUR TURN - PRACTICE EXERCISE")
print("=" * 60)

print("""
🎯 EXERCISE: Choose the Right Regularization

Scenario: You have a dataset with 100 features, but you suspect
only about 10 of them are actually useful.

Questions:
1. Which regularization method would you use? Why?
2. What would happen to the 90 useless feature weights?
3. What alpha value would you start with?

ANSWER BELOW:
""")

print("""
✅ ANSWERS:

1. Use LASSO (L1) because:
   - Lasso can make weights EXACTLY ZERO
   - This effectively removes useless features
   - Ridge would shrink all 100 weights but keep them

2. With Lasso:
   - The 90 useless features would have weights = 0
   - They're effectively "removed" from the model
   - Only ~10 useful features would have non-zero weights

3. Alpha value:
   - Start with alpha=1.0 as a baseline
   - Try range: 0.01, 0.1, 1.0, 10.0, 100.0
   - Use cross-validation to find optimal alpha
   - Higher alpha = more features removed

BONUS: Could also use ElasticNet with high l1_ratio (e.g., 0.7)
for feature selection with some L2 stability.
""")

# ============================================================
# SUMMARY
# ============================================================
print("\n" + "=" * 60)
print("📋 DAY 37 SUMMARY")
print("=" * 60)

print("""
✅ What you learned today:

1. REGULARIZATION:
   - Adds penalty for model complexity
   - Prevents overfitting
   - Improves generalization

2. TYPES:
   - L1 (Lasso): Feature selection (weights → 0)
   - L2 (Ridge): Weight shrinking (all non-zero)
   - ElasticNet: Combination of both

3. ALPHA (Regularization Strength):
   - Low alpha: Weak regularization
   - High alpha: Strong regularization
   - Need to find optimal balance

4. IMPORTANT STEPS:
   - ALWAYS scale features first!
   - Compare train vs test performance
   - Check feature weights

5. WHEN TO USE:
   - Overfitting → Add regularization
   - Many features → Use Lasso
   - General purpose → Use Ridge

🎉 Congratulations on completing Week 1!
""")


