# ============================================================
# 📘 DAY 33-34 PRACTICE: Bias & Variance
# ============================================================
# 
# 🎯 LEARNING GOALS:
# - Understand Bias (underfitting)
# - Understand Variance (overfitting)
# - See the bias-variance tradeoff visually
# - Learn how to detect these problems
#
# ⏱️ TIME: 45-60 minutes
# ============================================================

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import make_pipeline
from sklearn.metrics import mean_squared_error, r2_score

print("=" * 60)
print("📘 DAY 33-34: BIAS & VARIANCE")
print("=" * 60)

# ============================================================
# STEP 1: WHAT IS BIAS & VARIANCE?
# ============================================================
print("\n" + "=" * 60)
print("🎓 STEP 1: UNDERSTANDING BIAS & VARIANCE")
print("=" * 60)

print("""
┌─────────────────────────────────────────────────────────────┐
│                   BIAS vs VARIANCE                          │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  BIAS (Underfitting):                                       │
│  → Model is TOO SIMPLE                                      │
│  → Doesn't learn enough patterns                            │
│  → BAD on training data                                     │
│  → BAD on test data                                         │
│  → Like a straight line for curved data                     │
│                                                             │
│  VARIANCE (Overfitting):                                    │
│  → Model is TOO COMPLEX                                     │
│  → Memorizes training data (including noise)                │
│  → GREAT on training data                                   │
│  → BAD on test data                                         │
│  → Like a wiggly line through every point                   │
│                                                             │
│  GOAL:                                                      │
│  → Find the BALANCE (low bias + low variance)               │
│  → Model generalizes well to new data                       │
│                                                             │
└─────────────────────────────────────────────────────────────┘
""")

# ============================================================
# STEP 2: CREATE COMPLEX DATA
# ============================================================
print("\n" + "=" * 60)
print("📊 STEP 2: CREATE NON-LINEAR DATA")
print("=" * 60)

# Create non-linear data (sine wave with noise)
np.random.seed(42)
X = np.linspace(0, 10, 30)  # 30 data points
y_true = np.sin(X)  # True pattern (sine wave)
y = y_true + np.random.normal(0, 0.3, len(X))  # Add noise

# Convert to proper shape
X = X.reshape(-1, 1)

print(f"📊 Data created:")
print(f"   - {len(X)} data points")
print(f"   - X range: {X.min():.1f} to {X.max():.1f}")
print(f"   - True pattern: Sine wave")
print(f"   - Added random noise")

# ============================================================
# STEP 3: TRAIN THREE DIFFERENT MODELS
# ============================================================
print("\n" + "=" * 60)
print("🏋️ STEP 3: TRAIN THREE MODELS (Simple → Complex)")
print("=" * 60)

# Model 1: Very Simple (Degree 1 = Straight Line) - HIGH BIAS
model_simple = make_pipeline(PolynomialFeatures(1), LinearRegression())
model_simple.fit(X, y)
y_pred_simple = model_simple.predict(X)

# Model 2: Just Right (Degree 4)
model_good = make_pipeline(PolynomialFeatures(4), LinearRegression())
model_good.fit(X, y)
y_pred_good = model_good.predict(X)

# Model 3: Too Complex (Degree 15) - HIGH VARIANCE
model_complex = make_pipeline(PolynomialFeatures(15), LinearRegression())
model_complex.fit(X, y)
y_pred_complex = model_complex.predict(X)

print("""
Three models trained:
1. SIMPLE (Degree 1): Straight line → Likely HIGH BIAS
2. BALANCED (Degree 4): Moderate curve → Likely GOOD FIT
3. COMPLEX (Degree 15): Wiggly line → Likely HIGH VARIANCE
""")

# ============================================================
# STEP 4: EVALUATE EACH MODEL
# ============================================================
print("\n" + "=" * 60)
print("📊 STEP 4: EVALUATE EACH MODEL")
print("=" * 60)

# Calculate metrics
models = [
    ("Simple (Degree 1)", y_pred_simple),
    ("Balanced (Degree 4)", y_pred_good),
    ("Complex (Degree 15)", y_pred_complex)
]

print(f"{'Model':<25} {'MSE':<15} {'R² Score':<15} {'Status'}")
print("-" * 70)

for name, y_pred in models:
    mse = mean_squared_error(y, y_pred)
    r2 = r2_score(y, y_pred)
    
    if r2 < 0.5:
        status = "❌ High Bias (Underfitting)"
    elif r2 > 0.98:
        status = "⚠️ Possibly High Variance"
    else:
        status = "✅ Good Fit"
    
    print(f"{name:<25} {mse:<15.4f} {r2:<15.4f} {status}")

# ============================================================
# STEP 5: VISUALIZE BIAS vs VARIANCE
# ============================================================
print("\n" + "=" * 60)
print("📊 STEP 5: VISUALIZE THE DIFFERENCE")
print("=" * 60)

fig, axes = plt.subplots(1, 3, figsize=(15, 5))

# For smooth prediction lines
X_smooth = np.linspace(0, 10, 200).reshape(-1, 1)

# Plot 1: High Bias (Underfitting)
axes[0].scatter(X, y, color='blue', alpha=0.6, label='Data Points')
axes[0].plot(X_smooth, model_simple.predict(X_smooth), color='red', 
             linewidth=2, label='Model')
axes[0].set_title('HIGH BIAS (Underfitting)\nDegree 1 - Too Simple', fontsize=12)
axes[0].set_xlabel('X')
axes[0].set_ylabel('y')
axes[0].legend()
axes[0].grid(True, alpha=0.3)
mse1 = mean_squared_error(y, y_pred_simple)
axes[0].text(0.05, 0.95, f'MSE: {mse1:.3f}', transform=axes[0].transAxes, 
             fontsize=10, verticalalignment='top', bbox=dict(boxstyle='round', 
             facecolor='red', alpha=0.3))

# Plot 2: Good Fit
axes[1].scatter(X, y, color='blue', alpha=0.6, label='Data Points')
axes[1].plot(X_smooth, model_good.predict(X_smooth), color='green', 
             linewidth=2, label='Model')
axes[1].set_title('GOOD FIT (Balanced)\nDegree 4 - Just Right', fontsize=12)
axes[1].set_xlabel('X')
axes[1].set_ylabel('y')
axes[1].legend()
axes[1].grid(True, alpha=0.3)
mse2 = mean_squared_error(y, y_pred_good)
axes[1].text(0.05, 0.95, f'MSE: {mse2:.3f}', transform=axes[1].transAxes, 
             fontsize=10, verticalalignment='top', bbox=dict(boxstyle='round', 
             facecolor='green', alpha=0.3))

# Plot 3: High Variance (Overfitting)
axes[2].scatter(X, y, color='blue', alpha=0.6, label='Data Points')
y_complex_smooth = model_complex.predict(X_smooth)
# Clip extreme values for visualization
y_complex_smooth = np.clip(y_complex_smooth, -3, 3)
axes[2].plot(X_smooth, y_complex_smooth, color='orange', 
             linewidth=2, label='Model')
axes[2].set_title('HIGH VARIANCE (Overfitting)\nDegree 15 - Too Complex', fontsize=12)
axes[2].set_xlabel('X')
axes[2].set_ylabel('y')
axes[2].legend()
axes[2].grid(True, alpha=0.3)
axes[2].set_ylim(-2, 2)  # Limit y-axis for visualization
mse3 = mean_squared_error(y, y_pred_complex)
axes[2].text(0.05, 0.95, f'MSE: {mse3:.3f}', transform=axes[2].transAxes, 
             fontsize=10, verticalalignment='top', bbox=dict(boxstyle='round', 
             facecolor='orange', alpha=0.3))

plt.tight_layout()
plt.savefig('day33_34_bias_variance.png', dpi=100)
plt.show()

print("✅ Visualization saved as 'day33_34_bias_variance.png'")

# ============================================================
# STEP 6: TRAIN vs TEST ERROR
# ============================================================
print("\n" + "=" * 60)
print("📊 STEP 6: TRAIN vs TEST ERROR (Key Diagnostic!)")
print("=" * 60)

# Split data into train and test
from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

print(f"Train samples: {len(X_train)}")
print(f"Test samples: {len(X_test)}")

print(f"\n{'Model':<20} {'Train R²':<12} {'Test R²':<12} {'Gap':<10} {'Diagnosis'}")
print("-" * 75)

for degree, name in [(1, 'Simple'), (4, 'Balanced'), (15, 'Complex')]:
    model = make_pipeline(PolynomialFeatures(degree), LinearRegression())
    model.fit(X_train, y_train)
    
    train_r2 = r2_score(y_train, model.predict(X_train))
    test_r2 = r2_score(y_test, model.predict(X_test))
    gap = train_r2 - test_r2
    
    if train_r2 < 0.5 and test_r2 < 0.5:
        diagnosis = "High Bias"
    elif gap > 0.2:
        diagnosis = "High Variance"
    else:
        diagnosis = "Good Fit"
    
    print(f"{name:<20} {train_r2:<12.3f} {test_r2:<12.3f} {gap:<10.3f} {diagnosis}")

print("""
📌 HOW TO DIAGNOSE:

┌─────────────────────────────────────────────────────────────┐
│  Train R² │ Test R² │ Gap  │ Diagnosis                      │
├───────────┼─────────┼──────┼────────────────────────────────┤
│   Low     │  Low    │ Small│ HIGH BIAS (Underfitting)       │
│   High    │  Low    │ Large│ HIGH VARIANCE (Overfitting)    │
│   High    │  High   │ Small│ GOOD FIT ✅                    │
└───────────┴─────────┴──────┴────────────────────────────────┘
""")

# ============================================================
# STEP 7: DART BOARD ANALOGY
# ============================================================
print("\n" + "=" * 60)
print("🎯 STEP 7: DART BOARD ANALOGY")
print("=" * 60)

print("""
┌─────────────────────────────────────────────────────────────┐
│                  DART BOARD ANALOGY                         │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Imagine throwing darts at a target:                        │
│                                                             │
│  HIGH BIAS, LOW VARIANCE:                                   │
│  → All darts land together                                  │
│  → But they're AWAY from the center                         │
│  → Consistently wrong in the SAME way                       │
│                                                             │
│  LOW BIAS, HIGH VARIANCE:                                   │
│  → Darts are scattered all over                             │
│  → Some near center, some far                               │
│  → Predictions are INCONSISTENT                             │
│                                                             │
│  LOW BIAS, LOW VARIANCE (IDEAL):                            │
│  → All darts land near the center                           │
│  → Tight cluster at the target                              │
│  → ACCURATE and CONSISTENT ✅                               │
│                                                             │
└─────────────────────────────────────────────────────────────┘
""")

# Visualize dart board analogy
fig, axes = plt.subplots(1, 3, figsize=(12, 4))

def draw_target(ax, title, points):
    # Draw circles
    for r in [0.3, 0.6, 0.9]:
        circle = plt.Circle((0, 0), r, fill=False, color='black')
        ax.add_patch(circle)
    ax.scatter([0], [0], color='red', s=50, zorder=5)  # Center
    ax.scatter(*zip(*points), color='blue', s=80, alpha=0.7)
    ax.set_xlim(-1.2, 1.2)
    ax.set_ylim(-1.2, 1.2)
    ax.set_aspect('equal')
    ax.set_title(title, fontsize=11)
    ax.grid(True, alpha=0.3)

# High Bias, Low Variance (consistent but off-target)
np.random.seed(42)
points1 = [(0.7 + np.random.normal(0, 0.05), 0.7 + np.random.normal(0, 0.05)) for _ in range(8)]
draw_target(axes[0], 'High Bias, Low Variance\n(Consistent but Wrong)', points1)

# Low Bias, High Variance (scattered around center)
points2 = [(np.random.normal(0, 0.5), np.random.normal(0, 0.5)) for _ in range(8)]
draw_target(axes[1], 'Low Bias, High Variance\n(Scattered)', points2)

# Low Bias, Low Variance (ideal)
points3 = [(np.random.normal(0, 0.1), np.random.normal(0, 0.1)) for _ in range(8)]
draw_target(axes[2], 'Low Bias, Low Variance\n(IDEAL ✅)', points3)

plt.tight_layout()
plt.savefig('day33_34_dartboard.png', dpi=100)
plt.show()

print("✅ Dart board visualization saved as 'day33_34_dartboard.png'")

# ============================================================
# STEP 8: HOW TO FIX BIAS & VARIANCE
# ============================================================
print("\n" + "=" * 60)
print("🔧 STEP 8: HOW TO FIX BIAS & VARIANCE")
print("=" * 60)

print("""
┌─────────────────────────────────────────────────────────────┐
│              FIXING HIGH BIAS (Underfitting)                │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ✅ Use MORE COMPLEX model                                   │
│  ✅ Add MORE FEATURES                                        │
│  ✅ Train LONGER                                             │
│  ✅ REDUCE regularization                                    │
│                                                             │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│             FIXING HIGH VARIANCE (Overfitting)              │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ✅ Use SIMPLER model                                        │
│  ✅ Get MORE DATA                                            │
│  ✅ Use REGULARIZATION                                       │
│  ✅ REMOVE unnecessary features                              │
│  ✅ Use EARLY STOPPING                                       │
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
🎯 EXERCISE: Diagnose the Model!

Given this scenario:
- Training R² = 0.95 (very high)
- Test R² = 0.62 (moderate)
- Gap = 0.33 (large)

Questions:
1. Is this high bias or high variance?
2. What is the problem called?
3. What are 2 ways to fix it?

ANSWER BELOW:
""")

print("""
✅ ANSWERS:

1. This is HIGH VARIANCE

2. The problem is called OVERFITTING
   - Model performs great on training data
   - But poorly on new/test data

3. Ways to fix:
   - Get more training data
   - Use regularization (Ridge/Lasso)
   - Use simpler model
   - Remove unnecessary features
""")

# ============================================================
# SUMMARY
# ============================================================
print("\n" + "=" * 60)
print("📋 DAY 33-34 SUMMARY")
print("=" * 60)

print("""
✅ What you learned today:

1. BIAS:
   - Model too SIMPLE
   - UNDERFITTING
   - Bad on BOTH train and test

2. VARIANCE:
   - Model too COMPLEX
   - OVERFITTING
   - Great on train, bad on test

3. HOW TO DIAGNOSE:
   - Compare train vs test scores
   - Large gap = High Variance
   - Both low = High Bias

4. HOW TO FIX:
   - High Bias: More complex model, more features
   - High Variance: Simpler model, more data, regularization

5. GOAL:
   - Low bias + Low variance
   - Good generalization to new data

🎉 Great job understanding Bias & Variance!
""")


