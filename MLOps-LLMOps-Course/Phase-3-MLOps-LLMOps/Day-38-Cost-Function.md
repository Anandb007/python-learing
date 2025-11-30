# 📘 Day 38: Cost Function (Loss Function) — The Heart of Machine Learning

## 🎯 Learning Objectives
By the end of today, you will understand:
- What a Cost Function is and why it's essential
- How cost functions guide model learning
- Mean Squared Error (MSE) for regression
- Cross-Entropy Loss for classification
- How cost functions connect to AWS & DevOps scenarios
- Practical code examples with AWS-inspired datasets

---

## 📚 Section 1: What is a Cost Function?

### 🤔 The Simple Explanation

A **Cost Function** (also called **Loss Function**) tells a machine learning model:

> **"How wrong are you?"**

```
┌─────────────────────────────────────────────────────────────────┐
│                     COST FUNCTION                                │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│   Think of it like a TEACHER grading your exam:                  │
│                                                                  │
│   ┌────────────────────┐    ┌────────────────────┐              │
│   │   SCHOOL EXAM      │    │   MACHINE LEARNING │              │
│   ├────────────────────┤    ├────────────────────┤              │
│   │ Wrong answers      │ →  │ Wrong predictions  │              │
│   │ = More red marks   │    │ = High cost        │              │
│   │                    │    │                    │              │
│   │ Correct answers    │ →  │ Correct predictions│              │
│   │ = Less red marks   │    │ = Low cost         │              │
│   └────────────────────┘    └────────────────────┘              │
│                                                                  │
│   🎯 MODEL'S GOAL: Minimize the cost (reduce mistakes)           │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### 🔧 AWS/DevOps Analogy: CloudWatch Alarms

```
┌─────────────────────────────────────────────────────────────────┐
│              COST FUNCTION = AWS CLOUDWATCH ALARM                │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│   Just like CloudWatch monitors your AWS resources:              │
│                                                                  │
│   CloudWatch says:                                               │
│   ┌─────────────────────────────────────────────────────────┐   │
│   │ "Your EC2 CPU is at 95%! That's TOO HIGH!"               │   │
│   │ "Your Lambda execution time is 10s! That's TOO SLOW!"    │   │
│   │ "Your S3 request errors are 5%! That's NOT ACCEPTABLE!"  │   │
│   └─────────────────────────────────────────────────────────┘   │
│                                                                  │
│   Cost Function says:                                            │
│   ┌─────────────────────────────────────────────────────────┐   │
│   │ "Your prediction error is 10 lakhs! That's TOO HIGH!"    │   │
│   │ "Your prediction error is 1 lakh! That's ACCEPTABLE!"    │   │
│   └─────────────────────────────────────────────────────────┘   │
│                                                                  │
│   Both help MONITOR and CORRECT problems!                        │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 📚 Section 2: Why Do We Need a Cost Function?

### 📋 The Core Reason

Without knowing the mistake, the model **CANNOT**:

```
┌─────────────────────────────────────────────────────────────────┐
│           WITHOUT COST FUNCTION, MODEL CANNOT:                   │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│   ❌ Learn from mistakes                                         │
│   ❌ Improve predictions                                         │
│   ❌ Adjust weights and biases                                   │
│   ❌ Become accurate                                             │
│   ❌ Know when to stop training                                  │
│                                                                  │
│   ✅ Cost Function = Model's "SCORE CARD"                        │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### 🔧 DevOps Analogy: CI/CD Pipeline Feedback

```
┌─────────────────────────────────────────────────────────────────┐
│           COST FUNCTION ≈ CI/CD PIPELINE TESTS                   │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│   In Jenkins/GitHub Actions, after each build:                   │
│                                                                  │
│   ┌─────────────────────────────────────────────────────────┐   │
│   │  Tests Run: 100                                          │   │
│   │  Passed: 85                                              │   │
│   │  Failed: 15  ← This is like "COST"                       │   │
│   └─────────────────────────────────────────────────────────┘   │
│                                                                  │
│   Without this feedback:                                         │
│   → Developers don't know what's broken                          │
│   → Can't fix bugs                                               │
│   → Can't improve code                                           │
│                                                                  │
│   SAME with ML models:                                           │
│   → Without cost, model doesn't know what's wrong                │
│   → Can't adjust parameters                                      │
│   → Can't improve predictions                                    │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 📚 Section 3: Mean Squared Error (MSE) — For Regression

### 📐 The Formula

For regression problems (predicting continuous values), we use **Mean Squared Error (MSE)**:

```
┌─────────────────────────────────────────────────────────────────┐
│                   MEAN SQUARED ERROR (MSE)                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│                      1   n                                       │
│   MSE = ─── × Σ (y_actual - y_predicted)²                        │
│                      n  i=1                                      │
│                                                                  │
│   BREAKDOWN:                                                     │
│   ───────────                                                    │
│   Step 1: Find difference (error) for each prediction            │
│   Step 2: Square each error (makes all positive + penalizes big) │
│   Step 3: Add all squared errors                                 │
│   Step 4: Divide by total number of samples                      │
│                                                                  │
│   THE SMALLER THE MSE → THE BETTER THE MODEL                     │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### 🧮 Simple Example: EC2 Cost Prediction

Let's say we're predicting **monthly AWS EC2 costs** in dollars:

```
┌─────────────────────────────────────────────────────────────────┐
│              AWS EC2 COST PREDICTION EXAMPLE                     │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│   Actual EC2 Costs:    $500,  $1000,  $1500                      │
│   Model Predicted:     $450,  $1100,  $1400                      │
│                                                                  │
│   STEP 1: Calculate Errors                                       │
│   ─────────────────────────                                      │
│   (500 - 450)   = +50                                            │
│   (1000 - 1100) = -100                                           │
│   (1500 - 1400) = +100                                           │
│                                                                  │
│   STEP 2: Square the Errors                                      │
│   ─────────────────────────                                      │
│   50²  = 2,500                                                   │
│   100² = 10,000                                                  │
│   100² = 10,000                                                  │
│                                                                  │
│   STEP 3: Calculate Mean                                         │
│   ─────────────────────────                                      │
│   MSE = (2,500 + 10,000 + 10,000) / 3                            │
│   MSE = 22,500 / 3                                               │
│   MSE = 7,500                                                    │
│                                                                  │
│   Model tries to REDUCE this MSE further!                        │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### 💻 Code: Calculate MSE (AWS EC2 Cost Example)

```python
from sklearn.metrics import mean_squared_error
import numpy as np

# AWS EC2 monthly costs (in dollars)
actual_costs = [500, 1000, 1500]
predicted_costs = [450, 1100, 1400]

# Calculate MSE using sklearn
mse = mean_squared_error(actual_costs, predicted_costs)
print(f"MSE: {mse}")  # Output: MSE: 7500.0

# Manual calculation
errors = np.array(actual_costs) - np.array(predicted_costs)
squared_errors = errors ** 2
manual_mse = np.mean(squared_errors)
print(f"Manual MSE: {manual_mse}")  # Output: Manual MSE: 7500.0
```

---

## 📚 Section 4: Root Mean Squared Error (RMSE)

### 📐 Why RMSE?

MSE gives squared units. RMSE gives **same units as original data**.

```
┌─────────────────────────────────────────────────────────────────┐
│                ROOT MEAN SQUARED ERROR (RMSE)                    │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│   RMSE = √MSE                                                    │
│                                                                  │
│   From our EC2 example:                                          │
│   MSE = 7,500                                                    │
│   RMSE = √7,500 = 86.6                                           │
│                                                                  │
│   MEANING:                                                       │
│   "On average, our EC2 cost predictions are off by $86.6"        │
│                                                                  │
│   This is MUCH more interpretable than MSE!                      │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### 💻 Code: RMSE Calculation

```python
from sklearn.metrics import mean_squared_error
import numpy as np

actual_costs = [500, 1000, 1500]
predicted_costs = [450, 1100, 1400]

# RMSE using sklearn
mse = mean_squared_error(actual_costs, predicted_costs)
rmse = np.sqrt(mse)
print(f"RMSE: ${rmse:.2f}")  # Output: RMSE: $86.60

# Or directly using squared=False (sklearn >= 0.24)
rmse_direct = mean_squared_error(actual_costs, predicted_costs, squared=False)
print(f"RMSE (direct): ${rmse_direct:.2f}")
```

---

## 📚 Section 5: Mean Absolute Error (MAE)

### 📐 Another Option

MAE doesn't square errors, just takes absolute values:

```
┌─────────────────────────────────────────────────────────────────┐
│                  MEAN ABSOLUTE ERROR (MAE)                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│                      1   n                                       │
│   MAE = ─── × Σ |y_actual - y_predicted|                         │
│                      n  i=1                                      │
│                                                                  │
│   From our EC2 example:                                          │
│   Errors: |50| + |-100| + |100| = 50 + 100 + 100 = 250           │
│   MAE = 250 / 3 = 83.33                                          │
│                                                                  │
│   MSE vs MAE:                                                    │
│   ────────────                                                   │
│   • MSE penalizes BIG errors more (due to squaring)              │
│   • MAE treats all errors equally                                │
│   • MSE is more common in ML (easier math for optimization)      │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 📚 Section 6: How Cost Function Connects to Training

### 🔄 The Training Loop

When you call `model.fit(X, y)`, this happens inside:

```
┌─────────────────────────────────────────────────────────────────┐
│                    THE TRAINING LOOP                             │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│   ┌──────────────────────────────────────────────────────────┐  │
│   │                                                           │  │
│   │    STEP 1: Model makes predictions (y_pred)               │  │
│   │              ↓                                            │  │
│   │    STEP 2: Calculate COST (using MSE)                     │  │
│   │            "How wrong am I?"                              │  │
│   │              ↓                                            │  │
│   │    STEP 3: Adjust weights & bias                          │  │
│   │            "Let me fix my mistakes"                       │  │
│   │              ↓                                            │  │
│   │    STEP 4: Repeat until cost is minimal                   │  │
│   │              ↓                                            │  │
│   │    DONE: Model is TRAINED!                                │  │
│   │                                                           │  │
│   └──────────────────────────────────────────────────────────┘  │
│                                                                  │
│   This cycle is called TRAINING / OPTIMIZATION                   │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### 🔧 DevOps Analogy: Auto-Scaling Feedback Loop

```
┌─────────────────────────────────────────────────────────────────┐
│          TRAINING LOOP ≈ AWS AUTO-SCALING LOOP                   │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│   AWS AUTO-SCALING:                                              │
│   ─────────────────                                              │
│   1. CloudWatch monitors CPU/Memory                              │
│   2. If metric HIGH → scale UP (add EC2 instances)               │
│   3. If metric LOW → scale DOWN (remove instances)               │
│   4. Repeat until optimal                                        │
│                                                                  │
│   ML TRAINING:                                                   │
│   ─────────────────                                              │
│   1. Cost function monitors prediction error                     │
│   2. If cost HIGH → adjust weights                               │
│   3. If cost LOW → model is good                                 │
│   4. Repeat until optimal                                        │
│                                                                  │
│   BOTH use FEEDBACK LOOPS to reach optimal state!                │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 📚 Section 7: Cost Function for Classification

### 📐 Cross-Entropy Loss (Log Loss)

For classification problems (yes/no, categories), we use **Cross-Entropy Loss**:

```
┌─────────────────────────────────────────────────────────────────┐
│                   CROSS-ENTROPY LOSS                             │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│   Used for CLASSIFICATION (predicting categories)                │
│                                                                  │
│   FORMULA (Binary):                                              │
│   ──────────────────                                             │
│   Loss = -[y × log(p) + (1-y) × log(1-p)]                        │
│                                                                  │
│   Where:                                                         │
│   • y = actual label (0 or 1)                                    │
│   • p = predicted probability                                    │
│                                                                  │
│   AWS EXAMPLE: Predicting Deployment Success                     │
│   ─────────────────────────────────────────────                  │
│   Actual: Deployment SUCCEEDED (1)                               │
│   Model predicts: 90% chance of success                          │
│   → Low loss (correct prediction)                                │
│                                                                  │
│   Actual: Deployment SUCCEEDED (1)                               │
│   Model predicts: 10% chance of success                          │
│   → HIGH loss (wrong prediction)                                 │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### 🔧 AWS Example: Predicting Deployment Failure

```python
from sklearn.metrics import log_loss
import numpy as np

# AWS Deployment outcomes (1 = success, 0 = failure)
actual_outcomes = [1, 1, 0, 1, 0]

# Model's predicted PROBABILITIES of success
predicted_probs = [0.9, 0.8, 0.2, 0.7, 0.3]

# Calculate Cross-Entropy Loss
loss = log_loss(actual_outcomes, predicted_probs)
print(f"Cross-Entropy Loss: {loss:.4f}")

# Good predictions = low loss
# Bad predictions = high loss
```

---

## 📚 Section 8: Complete AWS EC2 Cost Prediction Example

### 💻 Full Code with Cost Function

```python
"""
AWS EC2 Cost Prediction Example
================================
Predicting monthly EC2 costs based on:
- Number of instances
- Hours running
- Instance type (vCPU count)

This demonstrates how cost function guides the model.
"""

import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, mean_absolute_error
import matplotlib.pyplot as plt

# Create AWS EC2 cost dataset
np.random.seed(42)

data = {
    'num_instances': [1, 2, 3, 5, 8, 10, 15, 20, 25, 30],
    'hours_running': [100, 200, 300, 500, 700, 720, 720, 720, 720, 720],
    'vcpu_count': [2, 4, 4, 8, 8, 16, 16, 32, 32, 64],
    'monthly_cost': [50, 150, 250, 500, 900, 1200, 1800, 3000, 4000, 7000]
}

df = pd.DataFrame(data)

print("=" * 60)
print("📊 AWS EC2 COST DATASET")
print("=" * 60)
print(df)

# Prepare features and target
X = df[['num_instances', 'hours_running', 'vcpu_count']]
y = df['monthly_cost']

# Split data
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42
)

# Train model
model = LinearRegression()
model.fit(X_train, y_train)

# Make predictions
y_train_pred = model.predict(X_train)
y_test_pred = model.predict(X_test)

# Calculate COST (MSE, RMSE, MAE)
print("\n" + "=" * 60)
print("📈 COST FUNCTION METRICS")
print("=" * 60)

# Training metrics
train_mse = mean_squared_error(y_train, y_train_pred)
train_rmse = np.sqrt(train_mse)
train_mae = mean_absolute_error(y_train, y_train_pred)

print(f"\n🏋️ TRAINING SET:")
print(f"   MSE:  ${train_mse:,.2f}")
print(f"   RMSE: ${train_rmse:,.2f}")
print(f"   MAE:  ${train_mae:,.2f}")

# Testing metrics
test_mse = mean_squared_error(y_test, y_test_pred)
test_rmse = np.sqrt(test_mse)
test_mae = mean_absolute_error(y_test, y_test_pred)

print(f"\n🧪 TESTING SET:")
print(f"   MSE:  ${test_mse:,.2f}")
print(f"   RMSE: ${test_rmse:,.2f}")
print(f"   MAE:  ${test_mae:,.2f}")

print(f"\n💡 INTERPRETATION:")
print(f"   On average, our EC2 cost predictions are off by ${test_rmse:,.2f}")
```

---

## 📚 Section 9: Visualizing Cost Function

### 📊 How Cost Changes During Training

```
┌─────────────────────────────────────────────────────────────────┐
│              COST DECREASING DURING TRAINING                     │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│   Cost                                                           │
│   ▲                                                              │
│   │ ████                                                         │
│   │ ████████                                                     │
│   │ ████████████                                                 │
│   │ ████████████████                                             │
│   │ ████████████████████                                         │
│   │ ████████████████████████                                     │
│   │ ████████████████████████████                                 │
│   │ ████████████████████████████████                             │
│   │ ████████████████████████████████████                         │
│   │ ████████████████████████████████████████                     │
│   └──────────────────────────────────────────────────► Training  │
│     Epoch 1  2  3  4  5  6  7  8  9  10                Epochs    │
│                                                                  │
│   GOAL: Keep training until cost stops decreasing!               │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### 💻 Code: Visualize MSE Comparison

```python
import matplotlib.pyplot as plt
import numpy as np

# Comparing two models
models = ['Model A\n(Bad)', 'Model B\n(Better)', 'Model C\n(Best)']
mse_values = [50000, 15000, 5000]
rmse_values = [np.sqrt(m) for m in mse_values]

fig, axes = plt.subplots(1, 2, figsize=(12, 5))

# MSE Comparison
axes[0].bar(models, mse_values, color=['red', 'orange', 'green'])
axes[0].set_title('MSE Comparison (Lower is Better)', fontsize=14)
axes[0].set_ylabel('Mean Squared Error')
for i, v in enumerate(mse_values):
    axes[0].text(i, v + 1000, f'{v:,}', ha='center', fontweight='bold')

# RMSE Comparison (more interpretable)
axes[1].bar(models, rmse_values, color=['red', 'orange', 'green'])
axes[1].set_title('RMSE Comparison (Average Error in $)', fontsize=14)
axes[1].set_ylabel('Root Mean Squared Error ($)')
for i, v in enumerate(rmse_values):
    axes[1].text(i, v + 5, f'${v:.0f}', ha='center', fontweight='bold')

plt.tight_layout()
plt.savefig('cost_function_comparison.png', dpi=150)
plt.show()
```

---

## 📚 Section 10: Cost Function in MLOps Context

### 🔧 Why Cost Function is Critical for MLOps

```
┌─────────────────────────────────────────────────────────────────┐
│              COST FUNCTION IN MLOps PIPELINE                     │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│   WITHOUT COST FUNCTION, YOU CANNOT:                             │
│                                                                  │
│   ❌ Measure model quality                                       │
│   ❌ Compare two models objectively                              │
│   ❌ Decide when to stop training                                │
│   ❌ Automate MLOps pipelines                                    │
│   ❌ Tune hyperparameters (needs a metric!)                      │
│   ❌ Track metrics in MLflow / AWS SageMaker                     │
│   ❌ Monitor model drift in production                           │
│                                                                  │
│   Cost Function is the FOUNDATION for:                           │
│   ─────────────────────────────────────                          │
│   ✅ Model Training                                              │
│   ✅ Model Evaluation                                            │
│   ✅ Hyperparameter Tuning                                       │
│   ✅ Experiment Tracking (MLflow)                                │
│   ✅ Model Registry Decisions                                    │
│   ✅ A/B Testing in Production                                   │
│   ✅ Alerting on Performance Degradation                         │
│   ✅ LLM Fine-tuning Loss                                        │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### 🔧 AWS SageMaker + MLflow Metrics Logging

```python
"""
Logging Cost Function Metrics to MLflow
(Used in MLOps pipelines)
"""

import mlflow

# Start MLflow experiment
mlflow.set_experiment("aws-ec2-cost-prediction")

with mlflow.start_run(run_name="linear-regression-v1"):
    
    # Log model parameters
    mlflow.log_param("model_type", "LinearRegression")
    mlflow.log_param("features", "num_instances,hours_running,vcpu_count")
    
    # Log COST FUNCTION METRICS (this is what matters!)
    mlflow.log_metric("train_mse", 15000)
    mlflow.log_metric("train_rmse", 122.47)
    mlflow.log_metric("test_mse", 18000)
    mlflow.log_metric("test_rmse", 134.16)
    
    # Now you can compare runs in MLflow UI!
    print("✅ Metrics logged to MLflow")
```

---

## 📚 Section 11: Different Cost Functions Summary

### 📋 When to Use Which?

| Problem Type | Cost Function | Formula | Use When |
|-------------|---------------|---------|----------|
| **Regression** | MSE | (y - ŷ)² | Default for continuous values |
| **Regression** | RMSE | √MSE | When you want interpretable units |
| **Regression** | MAE | \|y - ŷ\| | When outliers shouldn't dominate |
| **Classification** | Cross-Entropy | -[y×log(p) + (1-y)×log(1-p)] | Binary classification |
| **Multi-class** | Categorical Cross-Entropy | -Σ y×log(p) | Multiple categories |

### 🔧 AWS/DevOps Use Cases

```
┌─────────────────────────────────────────────────────────────────┐
│              AWS/DEVOPS COST FUNCTION USE CASES                  │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│   USE CASE                           COST FUNCTION               │
│   ────────────────────────────────   ─────────────               │
│   Predict EC2 monthly cost           MSE / RMSE                  │
│   Predict Lambda execution time      MSE / MAE                   │
│   Predict S3 storage growth          RMSE                        │
│   Predict deployment success/fail    Cross-Entropy               │
│   Predict build time in Jenkins      MAE                         │
│   Predict incident severity          Cross-Entropy               │
│   Predict CloudWatch metric value    MSE                         │
│   Predict EKS pod scaling needs      RMSE                        │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 📚 Section 12: Intuitive Visualization — Line Fitting

### 🎯 Cost Function Helps Find the Best Line

```
┌─────────────────────────────────────────────────────────────────┐
│                    FINDING THE BEST FIT LINE                     │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│   Imagine data points scattered:                                 │
│                                                                  │
│   Cost($)                                                        │
│      ▲                                           *               │
│   7K │                                       *                   │
│      │                                   *                       │
│   5K │                              *                            │
│      │                         *                                 │
│   3K │                    *                                      │
│      │               *                                           │
│   1K │          *                                                │
│      │     *                                                     │
│      └───────────────────────────────────────────────► Instances │
│        1   5   10   15   20   25   30                            │
│                                                                  │
│   COST FUNCTION tells us:                                        │
│   ────────────────────────                                       │
│   Line A: "This line is FAR from points → HIGH cost ❌"          │
│   Line B: "This line is CLOSE to points → LOW cost ✔️"           │
│                                                                  │
│   Algorithm keeps adjusting until cost is MINIMAL!               │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 📝 Section 13: Key Takeaways

### 📋 Summary Table

| Concept | Explanation |
|---------|-------------|
| **Cost Function** | Measures how wrong the model is |
| **Purpose** | Learning, improving, optimizing |
| **For Regression** | MSE (Mean Squared Error) |
| **For Classification** | Cross-Entropy Loss |
| **In Training** | Helps adjust weights & biases |
| **In MLOps** | Enables experiment tracking & model comparison |
| **AWS Analogy** | CloudWatch Alarms monitoring metrics |

### 🎯 The Core Formula You Must Remember

```
┌─────────────────────────────────────────────────────────────────┐
│                                                                  │
│                        1   n                                     │
│           MSE =  ─── × Σ (actual - predicted)²                   │
│                        n  i=1                                    │
│                                                                  │
│           LOWER MSE = BETTER MODEL                               │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🔗 Connection to Day 37 & Day 39

```
┌─────────────────────────────────────────────────────────────────┐
│                    LEARNING PROGRESSION                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│   Day 37: Regularization                                         │
│   ──────────────────────                                         │
│   Added PENALTY to cost function to prevent overfitting          │
│   Cost = MSE + λ × (penalty term)                                │
│                                                                  │
│   Day 38: Cost Function (TODAY)                                  │
│   ─────────────────────────────                                  │
│   Understanding HOW the model measures its mistakes              │
│   Cost = MSE or Cross-Entropy                                    │
│                                                                  │
│   Day 39: Gradient Descent (NEXT)                                │
│   ───────────────────────────────                                │
│   Understanding HOW the model reduces the cost                   │
│   Using derivatives to find the minimum cost                     │
│                                                                  │
│   FLOW: Cost Function tells "how wrong"                          │
│         Gradient Descent tells "how to fix"                      │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 📚 Homework

1. **Calculate MSE manually** for your own AWS cost predictions
2. **Try different metrics** (MSE, MAE, RMSE) and see which one suits your data
3. **Log metrics to MLflow** in your practice code
4. **Think about**: What cost function would you use for predicting Lambda cold start times?

---

**Next: Day 39 — Gradient Descent: How Models Learn to Reduce Cost** 🚀

