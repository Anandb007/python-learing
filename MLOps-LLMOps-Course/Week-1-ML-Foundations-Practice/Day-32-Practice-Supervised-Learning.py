# ============================================================
# 📘 DAY 32 PRACTICE: Supervised Learning
# ============================================================
# 
# 🎯 LEARNING GOALS:
# - Understand Supervised Learning
# - Learn Classification vs Regression
# - Build your first ML model!
# - Make predictions
#
# ⏱️ TIME: 45-60 minutes
# ============================================================

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

print("=" * 60)
print("📘 DAY 32: SUPERVISED LEARNING")
print("=" * 60)

# ============================================================
# STEP 1: WHAT IS SUPERVISED LEARNING?
# ============================================================
print("\n" + "=" * 60)
print("🎓 STEP 1: WHAT IS SUPERVISED LEARNING?")
print("=" * 60)

print("""
┌─────────────────────────────────────────────────────────────┐
│                  SUPERVISED LEARNING                        │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  DEFINITION:                                                │
│  Learning from LABELED data (data with correct answers)     │
│                                                             │
│  ANALOGY:                                                   │
│  Like a teacher showing students:                           │
│  "This is an apple 🍎" "This is a banana 🍌"                │
│  Student learns the patterns!                               │
│                                                             │
│  KEY COMPONENTS:                                            │
│  • Input (X): Features we use to predict                    │
│  • Output (y): Labels/Answers we want to predict            │
│  • Model: Learns the pattern X → y                          │
│                                                             │
└─────────────────────────────────────────────────────────────┘
""")

# ============================================================
# STEP 2: CLASSIFICATION vs REGRESSION
# ============================================================
print("\n" + "=" * 60)
print("🔄 STEP 2: CLASSIFICATION vs REGRESSION")
print("=" * 60)

print("""
┌─────────────────────────────────────────────────────────────┐
│            CLASSIFICATION vs REGRESSION                     │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  CLASSIFICATION:                                            │
│  → Predicts CATEGORIES                                      │
│  → Output: Yes/No, Cat/Dog, Spam/Not Spam                   │
│  → Example: Is this email spam? (Yes/No)                    │
│                                                             │
│  REGRESSION:                                                │
│  → Predicts NUMBERS                                         │
│  → Output: 50.5, $100,000, 25°C                             │
│  → Example: What's the house price? ($250,000)              │
│                                                             │
│  QUICK RULE:                                                │
│  • Predict CATEGORY → Classification                        │
│  • Predict NUMBER → Regression                              │
│                                                             │
└─────────────────────────────────────────────────────────────┘
""")

# Let's see examples
print("📊 EXAMPLES:")
print("-" * 50)

examples = [
    ("Email spam detection", "Spam / Not Spam", "Classification"),
    ("House price prediction", "$250,000", "Regression"),
    ("Disease diagnosis", "Sick / Healthy", "Classification"),
    ("Temperature forecast", "32°C", "Regression"),
    ("Loan approval", "Approve / Reject", "Classification"),
    ("Stock price", "$152.50", "Regression"),
]

print(f"{'Problem':<30} {'Output':<20} {'Type'}")
print("-" * 70)
for problem, output, ml_type in examples:
    print(f"{problem:<30} {output:<20} {ml_type}")

# ============================================================
# STEP 3: CREATE A REGRESSION DATASET
# ============================================================
print("\n" + "=" * 60)
print("📊 STEP 3: CREATE A REGRESSION DATASET")
print("=" * 60)

# Create house price data
np.random.seed(42)

# Simulating: Price = 50 * Area (roughly)
area = np.array([1000, 1200, 1400, 1600, 1800, 2000, 2200, 2400, 2600, 2800, 
                 3000, 1100, 1300, 1500, 1700, 1900, 2100, 2300, 2500, 2700])
# Price with some noise
price = area * 0.05 + np.random.normal(0, 5, len(area))  # Price in Lakhs

# Create DataFrame
df = pd.DataFrame({
    'Area_sqft': area,
    'Price_lakhs': price
})

print("\n📋 Our House Price Dataset:")
print(df.head(10))
print(f"\nTotal samples: {len(df)}")

# Visualize
plt.figure(figsize=(10, 6))
plt.scatter(df['Area_sqft'], df['Price_lakhs'], color='blue', alpha=0.7, s=100)
plt.xlabel('Area (sqft)', fontsize=12)
plt.ylabel('Price (Lakhs)', fontsize=12)
plt.title('House Area vs Price', fontsize=14)
plt.grid(True, alpha=0.3)
plt.savefig('day32_scatter.png', dpi=100)
plt.show()

print("✅ Scatter plot saved as 'day32_scatter.png'")

# ============================================================
# STEP 4: BUILD YOUR FIRST ML MODEL!
# ============================================================
print("\n" + "=" * 60)
print("🚀 STEP 4: BUILD YOUR FIRST ML MODEL!")
print("=" * 60)

print("""
We'll use LINEAR REGRESSION - the simplest regression algorithm.

It finds the best straight line through our data points:
    Price = slope × Area + intercept
""")

# Prepare data
X = df[['Area_sqft']]  # Features (must be 2D array)
y = df['Price_lakhs']   # Label (1D array)

print(f"📊 Features (X) shape: {X.shape}")
print(f"📊 Labels (y) shape: {y.shape}")

# Create and train the model
print("\n🏋️ Training the model...")
model = LinearRegression()
model.fit(X, y)  # This is where learning happens!

print("✅ Model trained!")

# What did the model learn?
print(f"""
📈 MODEL LEARNED:
   Price = {model.coef_[0]:.4f} × Area + {model.intercept_:.4f}
   
   In simple terms:
   • For every 1 sqft increase → Price increases by ₹{model.coef_[0]*1000:.0f}
   • Base price (intercept): ₹{model.intercept_:.2f} Lakhs
""")

# ============================================================
# STEP 5: MAKE PREDICTIONS
# ============================================================
print("\n" + "=" * 60)
print("🔮 STEP 5: MAKE PREDICTIONS")
print("=" * 60)

# Predict for houses in our dataset
predictions = model.predict(X)

print("📊 Actual vs Predicted:")
print("-" * 50)
comparison = pd.DataFrame({
    'Area': df['Area_sqft'],
    'Actual_Price': df['Price_lakhs'].round(2),
    'Predicted_Price': predictions.round(2),
    'Difference': (df['Price_lakhs'] - predictions).round(2)
})
print(comparison.head(10))

# Predict for NEW houses (never seen before!)
print("\n🔮 PREDICTING NEW HOUSES:")
print("-" * 50)
new_areas = [[1050], [1750], [2250], [3200]]  # New house areas

for area in new_areas:
    pred_price = model.predict([area])[0]
    print(f"   {area[0]} sqft house → Predicted: ₹{pred_price:.2f} Lakhs")

# ============================================================
# STEP 6: VISUALIZE THE MODEL
# ============================================================
print("\n" + "=" * 60)
print("📊 STEP 6: VISUALIZE THE MODEL")
print("=" * 60)

plt.figure(figsize=(10, 6))

# Plot actual data points
plt.scatter(df['Area_sqft'], df['Price_lakhs'], color='blue', 
            alpha=0.7, s=100, label='Actual Data')

# Plot prediction line
X_line = np.linspace(900, 3100, 100).reshape(-1, 1)
y_line = model.predict(X_line)
plt.plot(X_line, y_line, color='red', linewidth=2, label='Prediction Line')

# Plot new predictions
new_areas_flat = [a[0] for a in new_areas]
new_predictions = model.predict(new_areas)
plt.scatter(new_areas_flat, new_predictions, color='green', 
            s=200, marker='*', label='New Predictions', zorder=5)

plt.xlabel('Area (sqft)', fontsize=12)
plt.ylabel('Price (Lakhs)', fontsize=12)
plt.title('Linear Regression: House Price Prediction', fontsize=14)
plt.legend()
plt.grid(True, alpha=0.3)
plt.savefig('day32_prediction.png', dpi=100)
plt.show()

print("✅ Prediction visualization saved as 'day32_prediction.png'")

# ============================================================
# STEP 7: CLASSIFICATION EXAMPLE
# ============================================================
print("\n" + "=" * 60)
print("📊 STEP 7: CLASSIFICATION EXAMPLE (Conceptual)")
print("=" * 60)

print("""
Let's understand Classification with a simple example:

PROBLEM: Predict if a server will FAIL based on CPU usage

Training Data:
┌─────────┬─────────────┐
│ CPU %   │ Status      │
├─────────┼─────────────┤
│   25    │ Normal      │
│   30    │ Normal      │
│   45    │ Normal      │
│   92    │ Will Fail   │
│   95    │ Will Fail   │
│   98    │ Will Fail   │
└─────────┴─────────────┘

MODEL LEARNS: 
- CPU < 80% → Normal
- CPU > 80% → Will Fail

NEW PREDICTION:
- CPU = 55% → "Normal" ✅
- CPU = 88% → "Will Fail" 🚨
""")

# Simple classification simulation
print("\n🖥️ Server Status Prediction:")
print("-" * 50)

def predict_server_status(cpu):
    """Simple rule-based classifier (for demonstration)"""
    if cpu > 80:
        return "🚨 Will Fail"
    else:
        return "✅ Normal"

test_cpus = [25, 55, 75, 82, 91, 99]
for cpu in test_cpus:
    status = predict_server_status(cpu)
    print(f"   CPU: {cpu}% → {status}")

# ============================================================
# STEP 8: SUPERVISED LEARNING WORKFLOW
# ============================================================
print("\n" + "=" * 60)
print("📋 STEP 8: SUPERVISED LEARNING WORKFLOW")
print("=" * 60)

print("""
┌─────────────────────────────────────────────────────────────┐
│            SUPERVISED LEARNING WORKFLOW                     │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  STEP 1: COLLECT DATA                                       │
│  → Gather historical data with outcomes                     │
│  → Example: Past house sales with prices                    │
│                                                             │
│  STEP 2: PREPARE DATA                                       │
│  → Clean data, handle missing values                        │
│  → Split into features (X) and labels (y)                   │
│                                                             │
│  STEP 3: TRAIN MODEL                                        │
│  → model.fit(X, y)                                          │
│  → Model learns patterns                                    │
│                                                             │
│  STEP 4: MAKE PREDICTIONS                                   │
│  → model.predict(new_data)                                  │
│  → Apply to new, unseen data                                │
│                                                             │
│  STEP 5: EVALUATE                                           │
│  → Check how good predictions are                           │
│  → Improve if needed                                        │
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
🎯 EXERCISE: Predict Salary based on Experience

1. Create a dataset with:
   - Years of Experience: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
   - Salary (in thousands): [30, 35, 42, 50, 58, 65, 73, 82, 90, 100]

2. Train a Linear Regression model

3. Predict salary for:
   - 2.5 years experience
   - 7.5 years experience
   - 15 years experience

TRY IT YOURSELF! (Uncomment and complete the code below)
""")

# YOUR CODE HERE:
# ---------------
# experience = np.array([...]).reshape(-1, 1)
# salary = np.array([...])
# 
# model_salary = LinearRegression()
# model_salary.fit(experience, salary)
# 
# print("Model coefficients:", model_salary.coef_[0])
# print("Model intercept:", model_salary.intercept_)
# 
# new_exp = [[2.5], [7.5], [15]]
# for exp in new_exp:
#     pred = model_salary.predict([exp])[0]
#     print(f"{exp[0]} years → ${pred:.0f}K salary")

# ============================================================
# SOLUTION (Scroll down after trying!)
# ============================================================
print("\n" + "=" * 60)
print("✅ SOLUTION")
print("=" * 60)

experience = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10]).reshape(-1, 1)
salary = np.array([30, 35, 42, 50, 58, 65, 73, 82, 90, 100])

model_salary = LinearRegression()
model_salary.fit(experience, salary)

print(f"Model: Salary = {model_salary.coef_[0]:.2f} × Experience + {model_salary.intercept_:.2f}")

new_exp = [[2.5], [7.5], [15]]
print("\nPredictions:")
for exp in new_exp:
    pred = model_salary.predict([exp])[0]
    print(f"   {exp[0]} years → ${pred:.0f}K salary")

# ============================================================
# SUMMARY
# ============================================================
print("\n" + "=" * 60)
print("📋 DAY 32 SUMMARY")
print("=" * 60)

print("""
✅ What you learned today:

1. SUPERVISED LEARNING:
   - Learning from labeled data
   - Has inputs (X) and outputs (y)
   - Model learns the pattern X → y

2. CLASSIFICATION vs REGRESSION:
   - Classification: Predict categories (Yes/No)
   - Regression: Predict numbers (50.5, $100)

3. LINEAR REGRESSION:
   - Finds best straight line through data
   - Price = slope × feature + intercept
   - model.fit(X, y) to train
   - model.predict(X_new) to predict

4. WORKFLOW:
   - Collect → Prepare → Train → Predict → Evaluate

🎉 You built your FIRST ML model! Great job!
""")


