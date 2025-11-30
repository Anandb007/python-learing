# ============================================================
# 📘 DAY 38 PRACTICE: Cost Function (Loss Function)
# ============================================================
# 
# 🎯 LEARNING GOALS:
# - Understand what a cost function is
# - Calculate MSE, RMSE, MAE manually and using sklearn
# - Understand Cross-Entropy for classification
# - Apply cost functions to AWS/DevOps scenarios
#
# 🔧 AWS/DEVOPS EXAMPLES USED:
# - EC2 Monthly Cost Prediction
# - Lambda Execution Time Prediction
# - Deployment Success Classification
#
# ⏱️ TIME: 45-60 minutes
# ============================================================

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.metrics import (
    mean_squared_error, 
    mean_absolute_error, 
    log_loss,
    r2_score
)

print("=" * 60)
print("📘 DAY 38: COST FUNCTION (LOSS FUNCTION)")
print("    The Heart of Machine Learning")
print("=" * 60)

# ============================================================
# STEP 1: WHAT IS A COST FUNCTION?
# ============================================================
print("\n" + "=" * 60)
print("🎓 STEP 1: WHAT IS A COST FUNCTION?")
print("=" * 60)

print("""
┌─────────────────────────────────────────────────────────────┐
│                    COST FUNCTION                             │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  A Cost Function tells the model: "HOW WRONG ARE YOU?"       │
│                                                              │
│  ┌────────────────────────────────────────────────────┐     │
│  │  Wrong predictions  →  HIGH COST  ❌               │     │
│  │  Correct predictions →  LOW COST  ✅               │     │
│  └────────────────────────────────────────────────────┘     │
│                                                              │
│  AWS ANALOGY:                                                │
│  ────────────                                                │
│  CloudWatch Alarm says: "CPU is 95%! That's too high!"       │
│  Cost Function says: "Error is $500! That's too high!"       │
│                                                              │
│  Both MONITOR and help CORRECT problems!                     │
│                                                              │
└─────────────────────────────────────────────────────────────┘
""")

# ============================================================
# STEP 2: MANUAL MSE CALCULATION (AWS EC2 COST EXAMPLE)
# ============================================================
print("\n" + "=" * 60)
print("🧮 STEP 2: MANUAL MSE CALCULATION")
print("    Example: AWS EC2 Monthly Cost Prediction")
print("=" * 60)

# Simple example data
actual_ec2_costs = np.array([500, 1000, 1500])
predicted_ec2_costs = np.array([450, 1100, 1400])

print("\n📊 AWS EC2 Monthly Costs:")
print(f"   Actual costs:    ${actual_ec2_costs}")
print(f"   Predicted costs: ${predicted_ec2_costs}")

# Step-by-step MSE calculation
print("\n📐 STEP-BY-STEP MSE CALCULATION:")
print("=" * 40)

# Step 1: Calculate errors
errors = actual_ec2_costs - predicted_ec2_costs
print(f"\n1️⃣ Calculate errors (actual - predicted):")
for i, (a, p, e) in enumerate(zip(actual_ec2_costs, predicted_ec2_costs, errors)):
    print(f"   ${a} - ${p} = ${e:+d}")

# Step 2: Square the errors
squared_errors = errors ** 2
print(f"\n2️⃣ Square the errors:")
for i, (e, se) in enumerate(zip(errors, squared_errors)):
    print(f"   ({e})² = {se}")

# Step 3: Calculate mean
mse_manual = np.mean(squared_errors)
print(f"\n3️⃣ Calculate mean:")
print(f"   ({squared_errors[0]} + {squared_errors[1]} + {squared_errors[2]}) / 3")
print(f"   = {sum(squared_errors)} / 3")
print(f"   = {mse_manual}")

print(f"\n✅ RESULT: MSE = {mse_manual}")
print(f"   The model aims to REDUCE this value!")

# ============================================================
# STEP 3: USING SKLEARN FOR MSE
# ============================================================
print("\n" + "=" * 60)
print("🔧 STEP 3: USING SKLEARN FOR MSE")
print("=" * 60)

# Using sklearn
mse_sklearn = mean_squared_error(actual_ec2_costs, predicted_ec2_costs)

print(f"""
from sklearn.metrics import mean_squared_error

actual = {list(actual_ec2_costs)}
predicted = {list(predicted_ec2_costs)}

mse = mean_squared_error(actual, predicted)
print(mse)  # Output: {mse_sklearn}
""")

print(f"✅ sklearn MSE: {mse_sklearn}")
print(f"✅ Manual MSE:  {mse_manual}")
print(f"   Both match! ✔️")

# ============================================================
# STEP 4: RMSE - ROOT MEAN SQUARED ERROR
# ============================================================
print("\n" + "=" * 60)
print("📏 STEP 4: RMSE (Root Mean Squared Error)")
print("=" * 60)

rmse = np.sqrt(mse_sklearn)

print("""
┌─────────────────────────────────────────────────────────────┐
│                         RMSE                                 │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│   RMSE = √MSE                                                │
│                                                              │
│   WHY RMSE?                                                  │
│   → MSE gives squared units (dollars²)                       │
│   → RMSE gives same units as data (dollars)                  │
│   → RMSE is more INTERPRETABLE                               │
│                                                              │
└─────────────────────────────────────────────────────────────┘
""")

print(f"   MSE  = {mse_sklearn}")
print(f"   RMSE = √{mse_sklearn} = {rmse:.2f}")
print(f"\n💡 INTERPRETATION:")
print(f"   'On average, our EC2 cost predictions are off by ${rmse:.2f}'")

# sklearn direct RMSE
rmse_sklearn = mean_squared_error(actual_ec2_costs, predicted_ec2_costs, squared=False)
print(f"\n   sklearn RMSE (squared=False): ${rmse_sklearn:.2f}")

# ============================================================
# STEP 5: MAE - MEAN ABSOLUTE ERROR
# ============================================================
print("\n" + "=" * 60)
print("📏 STEP 5: MAE (Mean Absolute Error)")
print("=" * 60)

# Manual MAE
absolute_errors = np.abs(errors)
mae_manual = np.mean(absolute_errors)

print("""
┌─────────────────────────────────────────────────────────────┐
│                         MAE                                  │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│   MAE = (1/n) × Σ |actual - predicted|                       │
│                                                              │
│   MSE vs MAE:                                                │
│   → MSE: Penalizes BIG errors more (due to squaring)         │
│   → MAE: Treats all errors equally                           │
│                                                              │
└─────────────────────────────────────────────────────────────┘
""")

print("📐 Manual MAE Calculation:")
for i, (e, ae) in enumerate(zip(errors, absolute_errors)):
    print(f"   |{e}| = {ae}")
print(f"   MAE = ({absolute_errors[0]} + {absolute_errors[1]} + {absolute_errors[2]}) / 3")
print(f"   MAE = {mae_manual:.2f}")

# sklearn MAE
mae_sklearn = mean_absolute_error(actual_ec2_costs, predicted_ec2_costs)
print(f"\n   sklearn MAE: ${mae_sklearn:.2f}")

# ============================================================
# STEP 6: FULL AWS EC2 COST PREDICTION EXAMPLE
# ============================================================
print("\n" + "=" * 60)
print("🖥️ STEP 6: FULL AWS EC2 COST PREDICTION")
print("=" * 60)

# Create realistic AWS EC2 cost dataset
np.random.seed(42)

# Generate data
n_samples = 50
num_instances = np.random.randint(1, 20, n_samples)
hours_running = np.random.randint(100, 750, n_samples)
vcpu_count = np.random.choice([2, 4, 8, 16, 32], n_samples)

# Cost formula: base + instances * hourly_rate + vcpu_premium
# Simulating real AWS pricing patterns
monthly_cost = (
    50 +  # base cost
    num_instances * 0.1 * hours_running +  # compute cost
    vcpu_count * 5 +  # vCPU premium
    np.random.normal(0, 50, n_samples)  # noise
)
monthly_cost = np.maximum(monthly_cost, 50)  # minimum cost

# Create DataFrame
ec2_data = pd.DataFrame({
    'num_instances': num_instances,
    'hours_running': hours_running,
    'vcpu_count': vcpu_count,
    'monthly_cost': monthly_cost.round(2)
})

print("\n📊 AWS EC2 Cost Dataset (first 10 rows):")
print(ec2_data.head(10).to_string(index=False))

# Prepare features and target
X = ec2_data[['num_instances', 'hours_running', 'vcpu_count']]
y = ec2_data['monthly_cost']

# Split data
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42
)

print(f"\n📦 Data Split:")
print(f"   Training samples: {len(X_train)}")
print(f"   Testing samples:  {len(X_test)}")

# Train model
model = LinearRegression()
model.fit(X_train, y_train)

# Make predictions
y_train_pred = model.predict(X_train)
y_test_pred = model.predict(X_test)

# Calculate all metrics
print("\n" + "=" * 60)
print("📈 COST FUNCTION METRICS FOR EC2 PREDICTION MODEL")
print("=" * 60)

metrics = {
    'Training': {
        'MSE': mean_squared_error(y_train, y_train_pred),
        'RMSE': mean_squared_error(y_train, y_train_pred, squared=False),
        'MAE': mean_absolute_error(y_train, y_train_pred),
        'R²': r2_score(y_train, y_train_pred)
    },
    'Testing': {
        'MSE': mean_squared_error(y_test, y_test_pred),
        'RMSE': mean_squared_error(y_test, y_test_pred, squared=False),
        'MAE': mean_absolute_error(y_test, y_test_pred),
        'R²': r2_score(y_test, y_test_pred)
    }
}

print("\n🏋️ TRAINING SET METRICS:")
print(f"   MSE:  ${metrics['Training']['MSE']:,.2f}")
print(f"   RMSE: ${metrics['Training']['RMSE']:,.2f}")
print(f"   MAE:  ${metrics['Training']['MAE']:,.2f}")
print(f"   R²:   {metrics['Training']['R²']:.4f}")

print("\n🧪 TESTING SET METRICS:")
print(f"   MSE:  ${metrics['Testing']['MSE']:,.2f}")
print(f"   RMSE: ${metrics['Testing']['RMSE']:,.2f}")
print(f"   MAE:  ${metrics['Testing']['MAE']:,.2f}")
print(f"   R²:   {metrics['Testing']['R²']:.4f}")

print("\n💡 INTERPRETATION:")
print(f"   On average, our EC2 cost predictions are off by ${metrics['Testing']['RMSE']:,.2f}")

# ============================================================
# STEP 7: LAMBDA EXECUTION TIME PREDICTION
# ============================================================
print("\n" + "=" * 60)
print("⚡ STEP 7: AWS LAMBDA EXECUTION TIME PREDICTION")
print("=" * 60)

# Create Lambda execution dataset
np.random.seed(123)

n_samples = 40
memory_mb = np.random.choice([128, 256, 512, 1024, 2048], n_samples)
payload_size_kb = np.random.randint(1, 500, n_samples)
cold_start = np.random.choice([0, 1], n_samples, p=[0.7, 0.3])

# Execution time formula (in ms)
execution_time = (
    100 +  # base time
    (2048 / memory_mb) * 50 +  # more memory = faster
    payload_size_kb * 0.5 +  # larger payload = slower
    cold_start * 200 +  # cold start penalty
    np.random.normal(0, 30, n_samples)  # noise
)
execution_time = np.maximum(execution_time, 50)

lambda_data = pd.DataFrame({
    'memory_mb': memory_mb,
    'payload_size_kb': payload_size_kb,
    'cold_start': cold_start,
    'execution_time_ms': execution_time.round(2)
})

print("\n📊 AWS Lambda Execution Dataset (first 10 rows):")
print(lambda_data.head(10).to_string(index=False))

# Train model
X_lambda = lambda_data[['memory_mb', 'payload_size_kb', 'cold_start']]
y_lambda = lambda_data['execution_time_ms']

X_train_l, X_test_l, y_train_l, y_test_l = train_test_split(
    X_lambda, y_lambda, test_size=0.3, random_state=42
)

model_lambda = LinearRegression()
model_lambda.fit(X_train_l, y_train_l)

y_pred_l = model_lambda.predict(X_test_l)

# Metrics
lambda_rmse = mean_squared_error(y_test_l, y_pred_l, squared=False)
lambda_mae = mean_absolute_error(y_test_l, y_pred_l)

print("\n📈 LAMBDA EXECUTION TIME PREDICTION METRICS:")
print(f"   RMSE: {lambda_rmse:.2f} ms")
print(f"   MAE:  {lambda_mae:.2f} ms")
print(f"\n💡 On average, predictions are off by {lambda_mae:.2f} ms")

# ============================================================
# STEP 8: CROSS-ENTROPY LOSS FOR CLASSIFICATION
# ============================================================
print("\n" + "=" * 60)
print("🚀 STEP 8: CROSS-ENTROPY LOSS (Classification)")
print("    Example: Deployment Success Prediction")
print("=" * 60)

print("""
┌─────────────────────────────────────────────────────────────┐
│                   CROSS-ENTROPY LOSS                         │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│   Used for CLASSIFICATION (predicting categories)            │
│                                                              │
│   Binary Cross-Entropy:                                      │
│   Loss = -[y × log(p) + (1-y) × log(1-p)]                    │
│                                                              │
│   Where:                                                     │
│   • y = actual label (0 or 1)                                │
│   • p = predicted probability (0 to 1)                       │
│                                                              │
│   EXAMPLE:                                                   │
│   ─────────                                                  │
│   Actual: Deployment SUCCEEDED (1)                           │
│   Model predicts: 90% chance of success                      │
│   → Low loss (correct confident prediction)                  │
│                                                              │
│   Actual: Deployment SUCCEEDED (1)                           │
│   Model predicts: 10% chance of success                      │
│   → HIGH loss (wrong confident prediction)                   │
│                                                              │
└─────────────────────────────────────────────────────────────┘
""")

# Create deployment dataset
np.random.seed(456)

n_deployments = 60
code_coverage = np.random.randint(50, 100, n_deployments)
test_pass_rate = np.random.randint(70, 100, n_deployments)
build_time_minutes = np.random.randint(5, 60, n_deployments)
num_commits = np.random.randint(1, 50, n_deployments)

# Success probability based on features
success_prob = (
    code_coverage * 0.3 +
    test_pass_rate * 0.4 +
    (60 - build_time_minutes) * 0.2 +
    np.random.normal(0, 10, n_deployments)
)
success_prob = (success_prob - success_prob.min()) / (success_prob.max() - success_prob.min())
deployment_success = (success_prob > 0.5).astype(int)

deploy_data = pd.DataFrame({
    'code_coverage': code_coverage,
    'test_pass_rate': test_pass_rate,
    'build_time_min': build_time_minutes,
    'num_commits': num_commits,
    'success': deployment_success
})

print("📊 Deployment Dataset (first 10 rows):")
print(deploy_data.head(10).to_string(index=False))

# Train classification model
X_deploy = deploy_data[['code_coverage', 'test_pass_rate', 'build_time_min', 'num_commits']]
y_deploy = deploy_data['success']

X_train_d, X_test_d, y_train_d, y_test_d = train_test_split(
    X_deploy, y_deploy, test_size=0.3, random_state=42
)

model_deploy = LogisticRegression(random_state=42)
model_deploy.fit(X_train_d, y_train_d)

# Get probabilities for cross-entropy calculation
y_prob_d = model_deploy.predict_proba(X_test_d)[:, 1]

# Calculate Cross-Entropy Loss
cross_entropy = log_loss(y_test_d, y_prob_d)

print("\n📈 DEPLOYMENT PREDICTION METRICS:")
print(f"   Cross-Entropy Loss: {cross_entropy:.4f}")
print(f"   Accuracy: {model_deploy.score(X_test_d, y_test_d) * 100:.1f}%")

print("\n💡 INTERPRETATION:")
print(f"   Lower cross-entropy = Better classification model")
print(f"   Current loss: {cross_entropy:.4f} (lower is better)")

# ============================================================
# STEP 9: COMPARING COST FUNCTIONS
# ============================================================
print("\n" + "=" * 60)
print("📊 STEP 9: COMPARING COST FUNCTIONS")
print("=" * 60)

# Create comparison data
actual = np.array([100, 200, 300, 400, 500])
predictions = {
    'Good Model': np.array([105, 195, 305, 395, 505]),
    'Average Model': np.array([120, 180, 330, 370, 530]),
    'Bad Model': np.array([150, 150, 350, 350, 550])
}

print("\n📋 Model Comparison (Predicting AWS Costs):")
print(f"   Actual values: {actual}")

comparison_results = []
for name, pred in predictions.items():
    mse = mean_squared_error(actual, pred)
    rmse = np.sqrt(mse)
    mae = mean_absolute_error(actual, pred)
    comparison_results.append({
        'Model': name,
        'Predictions': str(pred.tolist()),
        'MSE': mse,
        'RMSE': round(rmse, 2),
        'MAE': mae
    })

comparison_df = pd.DataFrame(comparison_results)
print("\n" + comparison_df.to_string(index=False))

print("\n✅ KEY INSIGHT:")
print("   Lower MSE/RMSE/MAE = Better Model!")
print("   Good Model has the lowest cost → It's the best!")

# ============================================================
# STEP 10: VISUALIZE COST COMPARISON
# ============================================================
print("\n" + "=" * 60)
print("📊 STEP 10: VISUALIZING COST FUNCTIONS")
print("=" * 60)

try:
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    
    models = ['Good\nModel', 'Average\nModel', 'Bad\nModel']
    colors = ['#2ecc71', '#f39c12', '#e74c3c']  # green, orange, red
    
    # MSE Comparison
    mse_values = [r['MSE'] for r in comparison_results]
    axes[0].bar(models, mse_values, color=colors, edgecolor='black', linewidth=1.5)
    axes[0].set_title('MSE Comparison\n(Lower is Better)', fontsize=12, fontweight='bold')
    axes[0].set_ylabel('Mean Squared Error')
    for i, v in enumerate(mse_values):
        axes[0].text(i, v + 50, f'{v:,.0f}', ha='center', fontweight='bold')
    
    # RMSE Comparison
    rmse_values = [r['RMSE'] for r in comparison_results]
    axes[1].bar(models, rmse_values, color=colors, edgecolor='black', linewidth=1.5)
    axes[1].set_title('RMSE Comparison\n(Average Error in $)', fontsize=12, fontweight='bold')
    axes[1].set_ylabel('Root Mean Squared Error ($)')
    for i, v in enumerate(rmse_values):
        axes[1].text(i, v + 2, f'${v:.0f}', ha='center', fontweight='bold')
    
    # MAE Comparison
    mae_values = [r['MAE'] for r in comparison_results]
    axes[2].bar(models, mae_values, color=colors, edgecolor='black', linewidth=1.5)
    axes[2].set_title('MAE Comparison\n(Average Absolute Error)', fontsize=12, fontweight='bold')
    axes[2].set_ylabel('Mean Absolute Error ($)')
    for i, v in enumerate(mae_values):
        axes[2].text(i, v + 1, f'${v:.0f}', ha='center', fontweight='bold')
    
    plt.suptitle('Cost Function Comparison: AWS Cost Prediction Models', 
                 fontsize=14, fontweight='bold', y=1.02)
    plt.tight_layout()
    plt.savefig('cost_function_comparison.png', dpi=150, bbox_inches='tight')
    plt.show()
    print("   ✅ Visualization saved as 'cost_function_comparison.png'")
except Exception as e:
    print(f"   ⚠️ Could not display plot: {e}")
    print("   (This is normal if running without a display)")

# ============================================================
# STEP 11: WHEN TO USE WHICH COST FUNCTION
# ============================================================
print("\n" + "=" * 60)
print("📋 STEP 11: WHEN TO USE WHICH COST FUNCTION")
print("=" * 60)

print("""
┌─────────────────────────────────────────────────────────────┐
│                COST FUNCTION CHEAT SHEET                     │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│   PROBLEM TYPE          COST FUNCTION       AWS/DEVOPS USE   │
│   ────────────          ─────────────       ──────────────   │
│   Regression            MSE                 EC2 cost predict │
│   Regression            RMSE                Lambda time      │
│   Regression (outliers) MAE                 Build time       │
│   Binary Classification Cross-Entropy       Deploy success   │
│   Multi-class           Cat. Cross-Entropy  Incident type    │
│                                                              │
│   RULES OF THUMB:                                            │
│   ─────────────────                                          │
│   • MSE:  Default for regression, penalizes big errors       │
│   • RMSE: Same as MSE but interpretable units                │
│   • MAE:  When outliers shouldn't dominate                   │
│   • Cross-Entropy: For classification problems               │
│                                                              │
└─────────────────────────────────────────────────────────────┘
""")

# ============================================================
# STEP 12: MLFLOW LOGGING (OPTIONAL)
# ============================================================
print("\n" + "=" * 60)
print("📊 STEP 12: LOGGING TO MLFLOW (MLOps Ready!)")
print("=" * 60)

print("""
In a real MLOps pipeline, you would log these metrics to MLflow:

┌─────────────────────────────────────────────────────────────┐
│  import mlflow                                               │
│                                                              │
│  mlflow.set_experiment("aws-ec2-cost-prediction")            │
│                                                              │
│  with mlflow.start_run(run_name="linear-regression-v1"):     │
│      # Log parameters                                        │
│      mlflow.log_param("model_type", "LinearRegression")      │
│      mlflow.log_param("features", "instances,hours,vcpu")    │
│                                                              │
│      # Log COST FUNCTION METRICS                             │
│      mlflow.log_metric("train_mse", 15000)                   │
│      mlflow.log_metric("train_rmse", 122.47)                 │
│      mlflow.log_metric("test_mse", 18000)                    │
│      mlflow.log_metric("test_rmse", 134.16)                  │
│                                                              │
│      # Log model                                             │
│      mlflow.sklearn.log_model(model, "model")                │
│                                                              │
│  # Now compare runs in MLflow UI!                            │
└─────────────────────────────────────────────────────────────┘

This enables:
✅ Experiment comparison
✅ Model versioning
✅ Automated model selection
✅ Production deployment decisions
""")

# ============================================================
# FINAL SUMMARY
# ============================================================
print("\n" + "=" * 60)
print("📝 DAY 38 SUMMARY: COST FUNCTION")
print("=" * 60)

print("""
┌─────────────────────────────────────────────────────────────┐
│                    KEY TAKEAWAYS                             │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  1. WHAT: Cost function measures "how wrong" the model is    │
│                                                              │
│  2. WHY: Without it, model can't learn or improve            │
│                                                              │
│  3. TYPES:                                                   │
│     • MSE:  Mean Squared Error (regression)                  │
│     • RMSE: Root MSE (interpretable units)                   │
│     • MAE:  Mean Absolute Error (robust to outliers)         │
│     • Cross-Entropy: For classification                      │
│                                                              │
│  4. AWS/DEVOPS USES:                                         │
│     • EC2 cost prediction → MSE/RMSE                         │
│     • Lambda time prediction → MSE/MAE                       │
│     • Deployment success → Cross-Entropy                     │
│     • CloudWatch metric prediction → RMSE                    │
│                                                              │
│  5. MLOPS CONNECTION:                                        │
│     • Log metrics to MLflow                                  │
│     • Compare models objectively                             │
│     • Automate model selection                               │
│                                                              │
│  FORMULA TO REMEMBER:                                        │
│  ─────────────────────                                       │
│  MSE = (1/n) × Σ(actual - predicted)²                        │
│  LOWER MSE = BETTER MODEL                                    │
│                                                              │
└─────────────────────────────────────────────────────────────┘
""")

print("\n🎉 CONGRATULATIONS!")
print("   You now understand cost functions - the heart of ML!")
print("   Next: Day 39 - Gradient Descent (How to MINIMIZE cost)")
print("\n" + "=" * 60)


