# ============================================================
# 📘 DAY 39 PRACTICE: Feature Engineering
# ============================================================
# 
# 🎯 LEARNING GOALS:
# - Understand what features are
# - Create new features from existing data
# - Transform features (log, scaling, binning)
# - Encode categorical variables
# - Handle missing data and outliers
#
# 🔧 AWS/DEVOPS EXAMPLES USED:
# - EC2 Instance Cost Prediction
# - Lambda Execution Analysis
# - CI/CD Pipeline Success Prediction
# - CloudWatch Metrics Processing
#
# ⏱️ TIME: 60-75 minutes
# ============================================================

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler, MinMaxScaler, LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.metrics import mean_squared_error, accuracy_score, r2_score
from datetime import datetime, timedelta

print("=" * 60)
print("📘 DAY 39: FEATURE ENGINEERING")
print("    Improving Your Data for Better Models")
print("=" * 60)

# ============================================================
# STEP 1: WHAT IS A FEATURE?
# ============================================================
print("\n" + "=" * 60)
print("🎓 STEP 1: WHAT IS A FEATURE?")
print("=" * 60)

print("""
┌─────────────────────────────────────────────────────────────┐
│                    WHAT IS A FEATURE?                        │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  A FEATURE is information the model uses to make predictions │
│                                                              │
│  AWS/DEVOPS EXAMPLES:                                        │
│  ─────────────────────                                       │
│  EC2 Cost Prediction:                                        │
│  • instance_type, hours_running, region, num_instances       │
│                                                              │
│  Lambda Execution Time:                                      │
│  • memory_mb, payload_size, cold_start, runtime              │
│                                                              │
│  Deployment Success:                                         │
│  • code_coverage, test_pass_rate, build_time, commits        │
│                                                              │
│  FEATURE ENGINEERING = Making features BETTER                │
│  → 70% of a real ML engineer's job!                          │
│                                                              │
└─────────────────────────────────────────────────────────────┘
""")

# ============================================================
# STEP 2: FEATURE CREATION - EC2 EXAMPLE
# ============================================================
print("\n" + "=" * 60)
print("🆕 STEP 2: FEATURE CREATION")
print("    Creating New Features from Existing Data")
print("=" * 60)

# Create EC2 instance data
ec2_data = pd.DataFrame({
    'instance_id': ['i-001', 'i-002', 'i-003', 'i-004', 'i-005'],
    'instance_type': ['t2.micro', 't2.small', 't2.medium', 't2.large', 't2.xlarge'],
    'vcpu_count': [1, 1, 2, 2, 4],
    'memory_gb': [1, 2, 4, 8, 16],
    'hours_running': [720, 500, 720, 360, 720],
    'monthly_cost': [8.50, 17.00, 33.28, 33.28, 133.12],
    'launch_date': ['2024-01-15', '2024-06-01', '2023-12-01', '2024-09-01', '2024-03-15']
})

print("\n📊 Original EC2 Data:")
print(ec2_data.to_string(index=False))

print("\n" + "-" * 50)
print("🔧 Creating New Features...")
print("-" * 50)

# Feature 1: Cost per hour
ec2_data['cost_per_hour'] = ec2_data['monthly_cost'] / ec2_data['hours_running']
print(f"\n1️⃣ cost_per_hour = monthly_cost / hours_running")

# Feature 2: Compute power
ec2_data['compute_power'] = ec2_data['vcpu_count'] * ec2_data['memory_gb']
print(f"2️⃣ compute_power = vcpu_count × memory_gb")

# Feature 3: Cost per compute unit
ec2_data['cost_efficiency'] = ec2_data['monthly_cost'] / ec2_data['compute_power']
print(f"3️⃣ cost_efficiency = monthly_cost / compute_power")

# Feature 4: Instance age in days
ec2_data['launch_date'] = pd.to_datetime(ec2_data['launch_date'])
ec2_data['instance_age_days'] = (datetime.now() - ec2_data['launch_date']).dt.days
print(f"4️⃣ instance_age_days = today - launch_date")

# Feature 5: Full month usage indicator
ec2_data['full_month'] = (ec2_data['hours_running'] >= 700).astype(int)
print(f"5️⃣ full_month = 1 if hours >= 700, else 0")

# Feature 6: Utilization ratio
ec2_data['utilization_ratio'] = ec2_data['hours_running'] / 720
print(f"6️⃣ utilization_ratio = hours_running / 720")

print("\n📊 EC2 Data with NEW Features:")
display_cols = ['instance_id', 'cost_per_hour', 'compute_power', 
                'cost_efficiency', 'instance_age_days', 'full_month', 'utilization_ratio']
print(ec2_data[display_cols].to_string(index=False))

print("\n💡 KEY INSIGHT:")
print("   These new features give the model MORE information to learn from!")

# ============================================================
# STEP 3: FEATURE TRANSFORMATION
# ============================================================
print("\n" + "=" * 60)
print("🔄 STEP 3: FEATURE TRANSFORMATION")
print("    Changing Data Form for Better Learning")
print("=" * 60)

# Create Lambda data with varying scales
np.random.seed(42)
lambda_data = pd.DataFrame({
    'function_name': [f'func_{i}' for i in range(10)],
    'memory_mb': [128, 256, 512, 1024, 2048, 128, 256, 512, 1024, 2048],
    'invocations': [100, 5000, 150, 100000, 500, 10000, 300, 50000, 200, 1000000],
    'execution_time_ms': [50, 80, 120, 40, 200, 60, 100, 70, 150, 30],
    'payload_size_kb': [1, 50, 10, 500, 5, 100, 20, 200, 15, 1000]
})

print("\n📊 Lambda Data (Original):")
print(lambda_data.to_string(index=False))

print(f"\n📈 Value Ranges (before transformation):")
print(f"   memory_mb: {lambda_data['memory_mb'].min()} - {lambda_data['memory_mb'].max()}")
print(f"   invocations: {lambda_data['invocations'].min()} - {lambda_data['invocations'].max()}")
print(f"   Huge difference! This confuses the model.")

# (A) LOG TRANSFORMATION
print("\n" + "-" * 50)
print("(A) LOG TRANSFORMATION - For Skewed Data")
print("-" * 50)

lambda_data['log_invocations'] = np.log1p(lambda_data['invocations'])
print(f"\n   Original invocations: {list(lambda_data['invocations'][:5])}...")
print(f"   Log invocations:      {list(lambda_data['log_invocations'][:5].round(2))}...")
print(f"\n   ✅ Log transformation makes values more uniform!")

# (B) MIN-MAX SCALING
print("\n" + "-" * 50)
print("(B) MIN-MAX SCALING - Scale to 0-1 Range")
print("-" * 50)

scaler = MinMaxScaler()
lambda_data['memory_scaled'] = scaler.fit_transform(lambda_data[['memory_mb']])

print(f"\n   Original memory: {list(lambda_data['memory_mb'][:5])}")
print(f"   Scaled memory:   {list(lambda_data['memory_scaled'][:5].round(3))}")
print(f"\n   ✅ Now all values are between 0 and 1!")

# (C) STANDARD SCALING
print("\n" + "-" * 50)
print("(C) STANDARD SCALING - Mean=0, Std=1")
print("-" * 50)

std_scaler = StandardScaler()
lambda_data['execution_standardized'] = std_scaler.fit_transform(
    lambda_data[['execution_time_ms']]
)

print(f"\n   Original execution: {list(lambda_data['execution_time_ms'][:5])}")
print(f"   Standardized:       {list(lambda_data['execution_standardized'][:5].round(3))}")
print(f"\n   Mean: {lambda_data['execution_standardized'].mean():.6f} (≈ 0)")
print(f"   Std:  {lambda_data['execution_standardized'].std():.6f} (≈ 1)")

# (D) BINNING
print("\n" + "-" * 50)
print("(D) BINNING - Convert Numbers to Categories")
print("-" * 50)

lambda_data['usage_tier'] = pd.cut(
    lambda_data['invocations'],
    bins=[0, 1000, 10000, 100000, float('inf')],
    labels=['low', 'medium', 'high', 'very_high']
)

print(f"\n   Binning rules:")
print(f"   0-1000 invocations     → 'low'")
print(f"   1000-10000 invocations → 'medium'")
print(f"   10000-100000           → 'high'")
print(f"   100000+                → 'very_high'")

print(f"\n   Sample results:")
for i in range(5):
    print(f"   {lambda_data['invocations'][i]:>7} invocations → {lambda_data['usage_tier'][i]}")

# ============================================================
# STEP 4: ENCODING CATEGORICAL FEATURES
# ============================================================
print("\n" + "=" * 60)
print("🔢 STEP 4: ENCODING CATEGORICAL FEATURES")
print("    Converting Text to Numbers")
print("=" * 60)

print("""
┌─────────────────────────────────────────────────────────────┐
│                    WHY ENCODE?                               │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ML models only understand NUMBERS, not text!                │
│                                                              │
│  region = "us-east-1"  ❌ Model doesn't understand           │
│  region = 1            ✅ Model understands numbers          │
│                                                              │
│  ENCODING TYPES:                                             │
│  1. LABEL ENCODING - For ordinal data (has order)            │
│  2. ONE-HOT ENCODING - For nominal data (no order)           │
│                                                              │
└─────────────────────────────────────────────────────────────┘
""")

# Create EC2 data with categorical features
ec2_categorical = pd.DataFrame({
    'instance_id': ['i-001', 'i-002', 'i-003', 'i-004', 'i-005', 'i-006'],
    'region': ['us-east-1', 'us-west-2', 'ap-south-1', 'us-east-1', 'eu-west-1', 'us-west-2'],
    'instance_size': ['small', 'small', 'medium', 'large', 'small', 'xlarge'],
    'pricing_model': ['on-demand', 'spot', 'reserved', 'on-demand', 'spot', 'reserved'],
    'monthly_cost': [10, 5, 30, 80, 8, 60]
})

print("📊 EC2 Data with Categorical Features:")
print(ec2_categorical.to_string(index=False))

# (A) LABEL ENCODING - For ordinal data
print("\n" + "-" * 50)
print("(A) LABEL ENCODING - For Ordinal Data (has order)")
print("-" * 50)

# Instance size has an order: small < medium < large < xlarge
size_order = {'small': 0, 'medium': 1, 'large': 2, 'xlarge': 3}
ec2_categorical['size_encoded'] = ec2_categorical['instance_size'].map(size_order)

print(f"\n   Size order: small(0) < medium(1) < large(2) < xlarge(3)")
print(f"\n   Original → Encoded:")
for i in range(len(ec2_categorical)):
    orig = ec2_categorical['instance_size'][i]
    enc = ec2_categorical['size_encoded'][i]
    print(f"   {orig:>8} → {enc}")

# (B) ONE-HOT ENCODING - For nominal data
print("\n" + "-" * 50)
print("(B) ONE-HOT ENCODING - For Nominal Data (no order)")
print("-" * 50)

# Region has no inherent order
region_dummies = pd.get_dummies(ec2_categorical['region'], prefix='region')
ec2_encoded = pd.concat([ec2_categorical, region_dummies], axis=1)

print(f"\n   Regions: us-east-1, us-west-2, ap-south-1, eu-west-1")
print(f"   No inherent order → Use one-hot encoding")
print(f"\n   One-hot encoded columns:")
print(region_dummies.to_string(index=False))

# (C) Using sklearn LabelEncoder
print("\n" + "-" * 50)
print("(C) SKLEARN LabelEncoder")
print("-" * 50)

le = LabelEncoder()
ec2_categorical['pricing_encoded'] = le.fit_transform(ec2_categorical['pricing_model'])

print(f"\n   Pricing model encoding:")
for idx, label in enumerate(le.classes_):
    print(f"   {label:>10} → {idx}")

# ============================================================
# STEP 5: HANDLING MISSING DATA
# ============================================================
print("\n" + "=" * 60)
print("❓ STEP 5: HANDLING MISSING DATA")
print("    Fixing NULL/NaN Values")
print("=" * 60)

# Create CloudWatch data with missing values
np.random.seed(123)
cloudwatch_data = pd.DataFrame({
    'timestamp': pd.date_range('2024-01-01 00:00', periods=12, freq='H'),
    'cpu_utilization': [45, np.nan, 55, 60, np.nan, 70, 65, np.nan, 50, 45, 55, 60],
    'memory_utilization': [60, 65, np.nan, 70, 75, 80, np.nan, 85, 80, 75, np.nan, 70],
    'network_in_mb': [100, 150, 200, np.nan, 180, 160, 170, 190, np.nan, 140, 155, 165],
    'instance_type': ['t2.micro', np.nan, 't2.micro', 't2.micro', np.nan, 
                      't2.micro', 't2.micro', 't2.micro', np.nan, 
                      't2.micro', 't2.micro', 't2.micro']
})

print("\n📊 CloudWatch Data with Missing Values:")
print(cloudwatch_data.to_string(index=False))

print(f"\n❓ Missing Values Count:")
print(cloudwatch_data.isnull().sum())

# Create a copy for handling
cw_cleaned = cloudwatch_data.copy()

# (A) Fill with MEAN
print("\n" + "-" * 50)
print("(A) Fill with MEAN - For normal distributions")
print("-" * 50)

mean_value = cw_cleaned['cpu_utilization'].mean()
cw_cleaned['cpu_utilization'] = cw_cleaned['cpu_utilization'].fillna(mean_value)
print(f"   CPU mean: {mean_value:.2f}")
print(f"   ✅ Filled missing CPU values with {mean_value:.2f}")

# (B) Fill with MEDIAN
print("\n" + "-" * 50)
print("(B) Fill with MEDIAN - For skewed distributions")
print("-" * 50)

median_value = cw_cleaned['memory_utilization'].median()
cw_cleaned['memory_utilization'] = cw_cleaned['memory_utilization'].fillna(median_value)
print(f"   Memory median: {median_value:.2f}")
print(f"   ✅ Filled missing memory values with {median_value:.2f}")

# (C) Forward Fill - For time series
print("\n" + "-" * 50)
print("(C) Forward Fill (ffill) - For time series")
print("-" * 50)

cw_cleaned['network_in_mb'] = cw_cleaned['network_in_mb'].fillna(method='ffill')
print(f"   ✅ Used previous value for missing network data")

# (D) Fill with MODE - For categorical
print("\n" + "-" * 50)
print("(D) Fill with MODE - For categorical data")
print("-" * 50)

mode_value = cw_cleaned['instance_type'].mode()[0]
cw_cleaned['instance_type'] = cw_cleaned['instance_type'].fillna(mode_value)
print(f"   Instance type mode: {mode_value}")
print(f"   ✅ Filled missing instance_type with '{mode_value}'")

print(f"\n📊 Cleaned Data:")
print(cw_cleaned.to_string(index=False))
print(f"\n✅ Missing Values After Cleaning: {cw_cleaned.isnull().sum().sum()}")

# ============================================================
# STEP 6: OUTLIER HANDLING
# ============================================================
print("\n" + "=" * 60)
print("🚨 STEP 6: OUTLIER HANDLING")
print("    Detecting and Handling Extreme Values")
print("=" * 60)

# Create Lambda data with outliers
lambda_outliers = pd.DataFrame({
    'function_name': [f'func_{i}' for i in range(15)],
    'execution_time_ms': [50, 80, 100, 120, 90, 110, 95, 85, 
                          5000,  # ← Cold start outlier
                          105, 115, 88, 92, 
                          30000,  # ← Timeout outlier
                          102]
})

print("\n📊 Lambda Execution Data (with outliers):")
print(lambda_outliers.to_string(index=False))

print(f"\n📈 Statistics:")
print(f"   Mean:   {lambda_outliers['execution_time_ms'].mean():.2f} ms")
print(f"   Median: {lambda_outliers['execution_time_ms'].median():.2f} ms")
print(f"   (Mean is much higher due to outliers!)")

# IQR Method for outlier detection
print("\n" + "-" * 50)
print("IQR METHOD: Detecting Outliers")
print("-" * 50)

Q1 = lambda_outliers['execution_time_ms'].quantile(0.25)
Q3 = lambda_outliers['execution_time_ms'].quantile(0.75)
IQR = Q3 - Q1
lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR

print(f"\n   Q1 (25th percentile): {Q1}")
print(f"   Q3 (75th percentile): {Q3}")
print(f"   IQR = Q3 - Q1 = {IQR}")
print(f"\n   Outlier bounds:")
print(f"   Lower: Q1 - 1.5×IQR = {lower_bound}")
print(f"   Upper: Q3 + 1.5×IQR = {upper_bound}")

# Find outliers
outliers_mask = (
    (lambda_outliers['execution_time_ms'] < lower_bound) | 
    (lambda_outliers['execution_time_ms'] > upper_bound)
)
outliers = lambda_outliers[outliers_mask]

print(f"\n🚨 OUTLIERS DETECTED ({len(outliers)}):")
print(outliers.to_string(index=False))

# Solution 1: Remove outliers
print("\n" + "-" * 50)
print("SOLUTION 1: Remove Outliers")
print("-" * 50)

clean_data = lambda_outliers[~outliers_mask].copy()
print(f"   Original rows: {len(lambda_outliers)}")
print(f"   After removal: {len(clean_data)}")
print(f"   New mean: {clean_data['execution_time_ms'].mean():.2f} ms")

# Solution 2: Cap outliers (Winsorization)
print("\n" + "-" * 50)
print("SOLUTION 2: Cap Outliers (Winsorization)")
print("-" * 50)

lambda_outliers['execution_capped'] = lambda_outliers['execution_time_ms'].clip(
    lower=lower_bound, upper=upper_bound
)
print(f"   Capped to range: [{lower_bound:.0f}, {upper_bound:.0f}]")
print(f"   Max after capping: {lambda_outliers['execution_capped'].max():.0f} ms")

# ============================================================
# STEP 7: COMPLETE FEATURE ENGINEERING PIPELINE
# ============================================================
print("\n" + "=" * 60)
print("🔧 STEP 7: COMPLETE FEATURE ENGINEERING PIPELINE")
print("    CI/CD Pipeline Success Prediction")
print("=" * 60)

# Create CI/CD pipeline data
np.random.seed(42)
n_samples = 80

raw_cicd = pd.DataFrame({
    'pipeline_id': [f'pipe_{i}' for i in range(n_samples)],
    'repo': np.random.choice(['backend', 'frontend', 'api', 'infra'], n_samples),
    'branch': np.random.choice(['main', 'develop', 'feature'], n_samples),
    'num_commits': np.random.randint(1, 30, n_samples),
    'code_coverage': np.random.uniform(50, 100, n_samples),
    'test_count': np.random.randint(20, 300, n_samples),
    'build_time_sec': np.random.randint(30, 400, n_samples),
    'previous_failures': np.random.randint(0, 8, n_samples),
    'hour_of_day': np.random.randint(0, 24, n_samples)
})

# Add missing values
raw_cicd.loc[np.random.choice(n_samples, 4), 'code_coverage'] = np.nan
raw_cicd.loc[np.random.choice(n_samples, 3), 'test_count'] = np.nan

# Add outliers
raw_cicd.loc[0, 'build_time_sec'] = 3000

# Create target
success_prob = (
    raw_cicd['code_coverage'].fillna(70) * 0.4 +
    (100 - raw_cicd['previous_failures'] * 12) * 0.3 +
    (raw_cicd['test_count'].fillna(100) / 3) * 0.2 +
    np.random.normal(0, 15, n_samples)
)
raw_cicd['success'] = (success_prob > 55).astype(int)

print("\n📋 RAW CI/CD DATA (first 8 rows):")
print(raw_cicd.head(8).to_string(index=False))
print(f"\n❓ Missing values: {raw_cicd.isnull().sum().sum()}")

# PIPELINE STEP 1: Handle Missing Data
print("\n" + "─" * 50)
print("PIPELINE STEP 1: Handle Missing Data")
print("─" * 50)
data = raw_cicd.copy()
data['code_coverage'] = data['code_coverage'].fillna(data['code_coverage'].median())
data['test_count'] = data['test_count'].fillna(data['test_count'].median())
print(f"   ✅ Filled missing values with median")

# PIPELINE STEP 2: Handle Outliers
print("\n" + "─" * 50)
print("PIPELINE STEP 2: Handle Outliers")
print("─" * 50)
Q3_build = data['build_time_sec'].quantile(0.75)
IQR_build = data['build_time_sec'].quantile(0.75) - data['build_time_sec'].quantile(0.25)
upper_limit = Q3_build + 1.5 * IQR_build
data['build_time_sec'] = data['build_time_sec'].clip(upper=upper_limit)
print(f"   ✅ Capped build_time to max {upper_limit:.0f} sec")

# PIPELINE STEP 3: Feature Creation
print("\n" + "─" * 50)
print("PIPELINE STEP 3: Feature Creation")
print("─" * 50)
data['tests_per_commit'] = data['test_count'] / data['num_commits']
data['coverage_ratio'] = data['code_coverage'] / 100
data['build_efficiency'] = data['test_count'] / data['build_time_sec']
data['is_main_branch'] = (data['branch'] == 'main').astype(int)
data['is_working_hours'] = ((data['hour_of_day'] >= 9) & (data['hour_of_day'] <= 18)).astype(int)
data['failure_risk'] = data['previous_failures'] / 8
print("   ✅ Created 6 new features")

# PIPELINE STEP 4: Feature Transformation
print("\n" + "─" * 50)
print("PIPELINE STEP 4: Feature Transformation")
print("─" * 50)
data['log_build_time'] = np.log1p(data['build_time_sec'])
scaler = StandardScaler()
data[['commits_scaled', 'tests_scaled']] = scaler.fit_transform(
    data[['num_commits', 'test_count']]
)
print("   ✅ Applied log transform and standard scaling")

# PIPELINE STEP 5: Encoding
print("\n" + "─" * 50)
print("PIPELINE STEP 5: Encoding Categorical Features")
print("─" * 50)
repo_dummies = pd.get_dummies(data['repo'], prefix='repo')
data = pd.concat([data, repo_dummies], axis=1)
le = LabelEncoder()
data['branch_encoded'] = le.fit_transform(data['branch'])
print("   ✅ One-hot encoded 'repo', label encoded 'branch'")

# PIPELINE STEP 6: Select Features and Train
print("\n" + "─" * 50)
print("PIPELINE STEP 6: Train Model with Engineered Features")
print("─" * 50)

feature_cols = [
    'coverage_ratio', 'tests_per_commit', 'build_efficiency',
    'is_main_branch', 'is_working_hours', 'failure_risk',
    'log_build_time', 'commits_scaled', 'tests_scaled',
    'branch_encoded', 'repo_api', 'repo_backend', 'repo_frontend', 'repo_infra'
]

X = data[feature_cols]
y = data['success']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)

model = LogisticRegression(random_state=42, max_iter=500)
model.fit(X_train, y_train)

y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)

print(f"\n   📊 RESULTS:")
print(f"   Training samples: {len(X_train)}")
print(f"   Testing samples:  {len(X_test)}")
print(f"   Features used:    {len(feature_cols)}")
print(f"   Accuracy:         {accuracy * 100:.1f}%")

# Show feature importance
importance = pd.DataFrame({
    'feature': feature_cols,
    'importance': np.abs(model.coef_[0])
}).sort_values('importance', ascending=False)

print(f"\n   📈 Top 5 Important Features:")
for idx, row in importance.head(5).iterrows():
    print(f"      {row['feature']}: {row['importance']:.4f}")

# ============================================================
# STEP 8: BEFORE vs AFTER COMPARISON
# ============================================================
print("\n" + "=" * 60)
print("📊 STEP 8: BEFORE vs AFTER COMPARISON")
print("=" * 60)

# Train model WITHOUT feature engineering
X_basic = raw_cicd[['num_commits', 'test_count', 'build_time_sec', 'previous_failures']].copy()
X_basic = X_basic.fillna(X_basic.median())
y_basic = raw_cicd['success']

X_train_b, X_test_b, y_train_b, y_test_b = train_test_split(
    X_basic, y_basic, test_size=0.25, random_state=42
)

model_basic = LogisticRegression(random_state=42, max_iter=500)
model_basic.fit(X_train_b, y_train_b)
accuracy_basic = accuracy_score(y_test_b, model_basic.predict(X_test_b))

print(f"""
┌─────────────────────────────────────────────────────────────┐
│              FEATURE ENGINEERING IMPACT                      │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│   WITHOUT Feature Engineering:                               │
│   ─────────────────────────────                              │
│   Features used: 4 (basic columns only)                      │
│   Accuracy: {accuracy_basic * 100:.1f}%                                          │
│                                                              │
│   WITH Feature Engineering:                                  │
│   ──────────────────────────                                 │
│   Features used: {len(feature_cols)} (engineered features)                      │
│   Accuracy: {accuracy * 100:.1f}%                                          │
│                                                              │
│   IMPROVEMENT: +{(accuracy - accuracy_basic) * 100:.1f}% accuracy!                        │
│                                                              │
│   🎯 Feature Engineering makes models BETTER!                │
│                                                              │
└─────────────────────────────────────────────────────────────┘
""")

# ============================================================
# STEP 9: FEATURE ENGINEERING CHEAT SHEET
# ============================================================
print("\n" + "=" * 60)
print("📋 STEP 9: FEATURE ENGINEERING CHEAT SHEET")
print("=" * 60)

print("""
┌─────────────────────────────────────────────────────────────┐
│              FEATURE ENGINEERING TECHNIQUES                  │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│   TECHNIQUE           WHEN TO USE           EXAMPLE          │
│   ─────────           ───────────           ───────          │
│   Feature Creation    Always!               cost/hour        │
│   Log Transform       Skewed data           log(invocations) │
│   Min-Max Scaling     Neural networks       scale to 0-1     │
│   Standard Scaling    Linear models         mean=0, std=1    │
│   Binning             Continuous→Category   usage_tier       │
│   Label Encoding      Ordinal categories    small<medium     │
│   One-Hot Encoding    Nominal categories    region           │
│   Mean/Median Fill    Missing numerics      CPU utilization  │
│   Mode Fill           Missing categories    instance_type    │
│   Forward Fill        Time series           CloudWatch       │
│   IQR Outlier         Detect extremes       timeout values   │
│   Capping             Handle outliers       limit max value  │
│                                                              │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│              AWS/DEVOPS FEATURE IDEAS                        │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│   EC2 PREDICTIONS:                                           │
│   • cost_per_hour, compute_power, utilization_ratio          │
│   • instance_age, is_spot, region_encoded                    │
│                                                              │
│   LAMBDA ANALYSIS:                                           │
│   • log_invocations, memory_efficiency, cold_start_flag      │
│   • payload_per_invocation, runtime_encoded                  │
│                                                              │
│   CI/CD SUCCESS:                                             │
│   • tests_per_commit, coverage_ratio, failure_risk           │
│   • is_main_branch, is_working_hours, build_efficiency       │
│                                                              │
└─────────────────────────────────────────────────────────────┘
""")

# ============================================================
# FINAL SUMMARY
# ============================================================
print("\n" + "=" * 60)
print("📝 DAY 39 SUMMARY: FEATURE ENGINEERING")
print("=" * 60)

print("""
┌─────────────────────────────────────────────────────────────┐
│                    KEY TAKEAWAYS                             │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│   1. WHAT: Improving data so models learn better             │
│                                                              │
│   2. TYPES:                                                  │
│      • Feature Creation - Make new columns                   │
│      • Transformation - Log, scaling, binning                │
│      • Encoding - Text → Numbers                             │
│      • Missing Data - Fill NaN values                        │
│      • Outliers - Remove or cap extremes                     │
│                                                              │
│   3. WHY IT MATTERS:                                         │
│      • 70% of ML engineer's job                              │
│      • Directly impacts model accuracy                       │
│      • Bad features = bad model                              │
│                                                              │
│   4. AWS/DEVOPS CONNECTION:                                  │
│      • ETL pipelines (AWS Glue)                              │
│      • Feature stores (SageMaker)                            │
│      • Airflow for automation                                │
│      • MLflow for versioning                                 │
│                                                              │
│   🎯 REMEMBER: Good Features > Complex Models!               │
│                                                              │
└─────────────────────────────────────────────────────────────┘
""")

print("\n🎉 CONGRATULATIONS!")
print("   You've mastered Feature Engineering!")
print("   Next: Day 40 - Gradient Descent (How Models Learn)")
print("\n" + "=" * 60)

