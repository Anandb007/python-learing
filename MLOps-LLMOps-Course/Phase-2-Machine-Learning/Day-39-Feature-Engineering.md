# 📘 Day 39: Feature Engineering (Beginner → Intermediate)

## 🎯 Learning Objectives
By the end of today, you will understand:
- What features are and why they matter
- How to create new features from existing data
- Feature transformation techniques
- Encoding categorical variables
- Handling missing data and outliers
- AWS/DevOps feature engineering examples

---

## 📚 Section 1: What is Feature Engineering?

### 🤔 The Simple Explanation

**Feature Engineering** = "Improving your data so the model can learn better"

```
┌─────────────────────────────────────────────────────────────────┐
│              FEATURE ENGINEERING = COOKING                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│   🥬 Raw vegetables    =  Raw data                               │
│   🔪 Cutting, cleaning =  Feature engineering                    │
│   🍽️ Tasty dish        =  ML model output                        │
│                                                                  │
│   If you skip preparation → your dish (model) becomes BAD!       │
│                                                                  │
│   ┌────────────────────────────────────────────────────────┐    │
│   │  RAW DATA  →  FEATURE ENGINEERING  →  BETTER MODEL     │    │
│   └────────────────────────────────────────────────────────┘    │
│                                                                  │
│   Feature Engineering is 70% of a real ML job!                   │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### 🔧 AWS DevOps Analogy

```
┌─────────────────────────────────────────────────────────────────┐
│          FEATURE ENGINEERING ≈ DATA PIPELINE (ETL)               │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│   In AWS Data Pipelines:                                         │
│                                                                  │
│   ┌──────────┐    ┌─────────────┐    ┌──────────────┐           │
│   │  Raw S3  │ →  │  AWS Glue   │ →  │ Clean Data   │           │
│   │  Data    │    │  Transform  │    │  for ML      │           │
│   └──────────┘    └─────────────┘    └──────────────┘           │
│                                                                  │
│   AWS Glue does:                                                 │
│   • Clean messy data                                             │
│   • Transform formats                                            │
│   • Create new columns                                           │
│   • Handle missing values                                        │
│                                                                  │
│   That's exactly what Feature Engineering does!                  │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 📚 Section 2: What is a Feature?

### 📋 Definition

A **feature** is information the model uses to make predictions.

```
┌─────────────────────────────────────────────────────────────────┐
│                      WHAT IS A FEATURE?                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│   PREDICTION TASK              FEATURES USED                     │
│   ────────────────             ─────────────                     │
│   House price                  Area, bedrooms, location          │
│   Salary                       Experience, skills, education     │
│   Weather                      Humidity, temperature, pressure   │
│                                                                  │
│   AWS/DEVOPS EXAMPLES:                                           │
│   ─────────────────────────────────────────                      │
│   EC2 Cost prediction          Instance type, hours, region      │
│   Lambda execution time        Memory, payload size, runtime     │
│   Deployment success           Test coverage, commits, build time│
│   S3 storage cost              Object count, size, storage class │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### 🔧 AWS Example: EC2 Cost Prediction Features

```
┌─────────────────────────────────────────────────────────────────┐
│              EC2 COST PREDICTION - FEATURES                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│   To predict EC2 monthly cost, we need FEATURES:                 │
│                                                                  │
│   BASIC FEATURES:                                                │
│   ───────────────                                                │
│   • instance_type     (t2.micro, m5.large, etc.)                 │
│   • hours_running     (how many hours per month)                 │
│   • region            (us-east-1, ap-south-1, etc.)              │
│   • num_instances     (how many EC2 instances)                   │
│                                                                  │
│   ENGINEERED FEATURES (we create these!):                        │
│   ────────────────────────────────────────                       │
│   • cost_per_hour     = total_cost / hours_running               │
│   • utilization_ratio = actual_hours / max_hours                 │
│   • is_spot_instance  = 1 if spot, 0 if on-demand                │
│   • vcpu_memory_ratio = vcpu_count / memory_gb                   │
│                                                                  │
│   More features → Better predictions!                            │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 📚 Section 3: Types of Feature Engineering

### 📋 Overview

```
┌─────────────────────────────────────────────────────────────────┐
│              TYPES OF FEATURE ENGINEERING                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│   (A) Feature Creation     → Create NEW features                 │
│   (B) Feature Transformation → Change form of data               │
│   (C) Encoding             → Convert text to numbers             │
│   (D) Handling Missing Data → Fix NaN/NULL values                │
│   (E) Outlier Handling     → Remove extreme values               │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 📚 Section 4: (A) Feature Creation

### 🆕 Creating New Features from Existing Ones

This is the **MOST IMPORTANT** part of feature engineering!

```
┌─────────────────────────────────────────────────────────────────┐
│                    FEATURE CREATION                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│   WHAT: Create new columns from existing data                    │
│   WHY:  Give the model NEW knowledge it couldn't see before      │
│                                                                  │
│   AWS EC2 EXAMPLES:                                              │
│   ─────────────────                                              │
│                                                                  │
│   1. Cost per hour:                                              │
│      cost_per_hour = monthly_cost / hours_running                │
│                                                                  │
│   2. Instance age (days since launch):                           │
│      instance_age = current_date - launch_date                   │
│                                                                  │
│   3. Total compute units:                                        │
│      compute_units = vcpu_count × memory_gb                      │
│                                                                  │
│   4. Utilization efficiency:                                     │
│      efficiency = actual_usage / provisioned_capacity            │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### 💻 Code Example: Feature Creation for EC2 Data

```python
import pandas as pd
from datetime import datetime

# EC2 Instance Data
ec2_data = pd.DataFrame({
    'instance_id': ['i-001', 'i-002', 'i-003', 'i-004'],
    'vcpu_count': [2, 4, 8, 16],
    'memory_gb': [4, 8, 32, 64],
    'hours_running': [720, 500, 720, 360],
    'monthly_cost': [50, 120, 400, 600],
    'launch_date': ['2024-01-15', '2024-06-01', '2023-12-01', '2024-09-01']
})

# FEATURE CREATION
# 1. Cost per hour
ec2_data['cost_per_hour'] = ec2_data['monthly_cost'] / ec2_data['hours_running']

# 2. Compute power (vCPU × Memory)
ec2_data['compute_power'] = ec2_data['vcpu_count'] * ec2_data['memory_gb']

# 3. Cost efficiency (cost per compute unit)
ec2_data['cost_efficiency'] = ec2_data['monthly_cost'] / ec2_data['compute_power']

# 4. Instance age in days
ec2_data['launch_date'] = pd.to_datetime(ec2_data['launch_date'])
ec2_data['instance_age_days'] = (datetime.now() - ec2_data['launch_date']).dt.days

# 5. Is running full month?
ec2_data['full_month_usage'] = (ec2_data['hours_running'] >= 700).astype(int)

print("EC2 Data with Engineered Features:")
print(ec2_data.to_string(index=False))
```

---

## 📚 Section 5: (B) Feature Transformation

### 🔄 Changing Data Form for Better Learning

```
┌─────────────────────────────────────────────────────────────────┐
│                  FEATURE TRANSFORMATION                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│   1. LOG TRANSFORMATION (for skewed data)                        │
│   ─────────────────────────────────────────                      │
│   When values vary a lot (1, 10, 100, 10000)                     │
│   → Apply log to stabilize                                       │
│                                                                  │
│   Example: S3 object sizes vary from 1KB to 5TB                  │
│   log_size = log(object_size)                                    │
│                                                                  │
│   2. NORMALIZATION / SCALING                                     │
│   ──────────────────────────                                     │
│   When features have different ranges:                           │
│   • hours_running: 1-720                                         │
│   • monthly_cost: 10-10000                                       │
│   → Scale to same range (0-1)                                    │
│                                                                  │
│   3. BINNING (numbers → categories)                              │
│   ─────────────────────────────────                              │
│   Convert continuous values to categories:                       │
│   • 0-100 hours → "low_usage"                                    │
│   • 100-500 hours → "medium_usage"                               │
│   • 500-720 hours → "high_usage"                                 │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### 💻 Code Example: Feature Transformation

```python
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler, StandardScaler

# Lambda execution data
lambda_data = pd.DataFrame({
    'function_name': ['func_a', 'func_b', 'func_c', 'func_d', 'func_e'],
    'memory_mb': [128, 256, 512, 1024, 2048],
    'execution_time_ms': [50, 100, 200, 80, 150],
    'invocations': [1000, 50000, 100, 500000, 10000],
    'payload_size_kb': [1, 50, 500, 10, 100]
})

print("Original Data:")
print(lambda_data.to_string(index=False))

# 1. LOG TRANSFORMATION (for skewed invocations)
lambda_data['log_invocations'] = np.log1p(lambda_data['invocations'])

# 2. MIN-MAX SCALING (0 to 1)
scaler = MinMaxScaler()
lambda_data['memory_scaled'] = scaler.fit_transform(lambda_data[['memory_mb']])

# 3. STANDARD SCALING (mean=0, std=1)
std_scaler = StandardScaler()
lambda_data['execution_standardized'] = std_scaler.fit_transform(
    lambda_data[['execution_time_ms']]
)

# 4. BINNING (convert to categories)
lambda_data['usage_tier'] = pd.cut(
    lambda_data['invocations'],
    bins=[0, 1000, 10000, 100000, float('inf')],
    labels=['low', 'medium', 'high', 'very_high']
)

print("\nTransformed Data:")
print(lambda_data.to_string(index=False))
```

---

## 📚 Section 6: (C) Encoding Categorical Features

### 🔢 Converting Text to Numbers

ML models require **numbers**, not text!

```
┌─────────────────────────────────────────────────────────────────┐
│                   CATEGORICAL ENCODING                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│   PROBLEM: Model can't understand text                           │
│   ─────────                                                      │
│   region = "us-east-1"  ❌ Model doesn't understand              │
│   region = 1            ✅ Model understands numbers             │
│                                                                  │
│   ENCODING TYPES:                                                │
│   ───────────────                                                │
│                                                                  │
│   1. LABEL ENCODING (for ordinal data)                           │
│      small → 0, medium → 1, large → 2                            │
│      (Order matters!)                                            │
│                                                                  │
│   2. ONE-HOT ENCODING (for nominal data)                         │
│      us-east-1 → [1, 0, 0]                                       │
│      us-west-2 → [0, 1, 0]                                       │
│      eu-west-1 → [0, 0, 1]                                       │
│      (No order, just categories)                                 │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### 💻 Code Example: Encoding AWS Regions and Instance Types

```python
import pandas as pd
from sklearn.preprocessing import LabelEncoder

# EC2 data with categorical features
ec2_data = pd.DataFrame({
    'instance_id': ['i-001', 'i-002', 'i-003', 'i-004', 'i-005'],
    'region': ['us-east-1', 'us-west-2', 'ap-south-1', 'us-east-1', 'eu-west-1'],
    'instance_type': ['t2.micro', 't2.small', 't2.medium', 't2.large', 't2.micro'],
    'instance_size': ['small', 'small', 'medium', 'large', 'small'],
    'monthly_cost': [10, 20, 40, 80, 10]
})

print("Original Data:")
print(ec2_data.to_string(index=False))

# 1. LABEL ENCODING (for ordinal: size has order)
size_order = {'small': 0, 'medium': 1, 'large': 2}
ec2_data['size_encoded'] = ec2_data['instance_size'].map(size_order)

# 2. ONE-HOT ENCODING (for nominal: region has no order)
region_dummies = pd.get_dummies(ec2_data['region'], prefix='region')
ec2_encoded = pd.concat([ec2_data, region_dummies], axis=1)

print("\nEncoded Data:")
print(ec2_encoded.to_string(index=False))

# 3. Using sklearn LabelEncoder
le = LabelEncoder()
ec2_data['instance_type_encoded'] = le.fit_transform(ec2_data['instance_type'])

print("\nInstance Type Mapping:")
for idx, label in enumerate(le.classes_):
    print(f"   {label} → {idx}")
```

---

## 📚 Section 7: (D) Handling Missing Data

### ❓ Fixing NULL/NaN Values

```
┌─────────────────────────────────────────────────────────────────┐
│                  HANDLING MISSING DATA                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│   PROBLEM: Dataset has empty values (NaN, NULL)                  │
│   ─────────                                                      │
│   CloudWatch metrics sometimes have gaps                         │
│   S3 access logs might be incomplete                             │
│   EC2 utilization data can be missing                            │
│                                                                  │
│   SOLUTIONS:                                                     │
│   ──────────                                                     │
│                                                                  │
│   1. REMOVE rows with missing values                             │
│      df.dropna()                                                 │
│      → Use when few rows have missing data                       │
│                                                                  │
│   2. FILL with mean/median/mode                                  │
│      df['col'].fillna(df['col'].mean())                          │
│      → Mean for normal data                                      │
│      → Median for skewed data                                    │
│      → Mode for categorical data                                 │
│                                                                  │
│   3. FILL with specific value                                    │
│      df['col'].fillna(0)                                         │
│      → When missing = zero makes sense                           │
│                                                                  │
│   4. FORWARD/BACKWARD FILL (for time series)                     │
│      df['col'].fillna(method='ffill')                            │
│      → Use previous value                                        │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### 💻 Code Example: Handling Missing CloudWatch Metrics

```python
import pandas as pd
import numpy as np

# CloudWatch metrics with missing values
cloudwatch_data = pd.DataFrame({
    'timestamp': pd.date_range('2024-01-01', periods=10, freq='H'),
    'cpu_utilization': [45, np.nan, 55, 60, np.nan, 70, 65, np.nan, 50, 45],
    'memory_utilization': [60, 65, np.nan, 70, 75, 80, np.nan, 85, 80, 75],
    'network_in_mb': [100, 150, 200, np.nan, 180, 160, 170, 190, np.nan, 140],
    'region': ['us-east-1', np.nan, 'us-east-1', 'us-east-1', np.nan, 
               'us-east-1', 'us-east-1', 'us-east-1', np.nan, 'us-east-1']
})

print("Original Data with Missing Values:")
print(cloudwatch_data.to_string(index=False))
print(f"\nMissing values per column:")
print(cloudwatch_data.isnull().sum())

# SOLUTION 1: Fill numeric with mean
cloudwatch_data['cpu_utilization'] = cloudwatch_data['cpu_utilization'].fillna(
    cloudwatch_data['cpu_utilization'].mean()
)

# SOLUTION 2: Fill numeric with median (better for skewed data)
cloudwatch_data['memory_utilization'] = cloudwatch_data['memory_utilization'].fillna(
    cloudwatch_data['memory_utilization'].median()
)

# SOLUTION 3: Forward fill for time series (use previous value)
cloudwatch_data['network_in_mb'] = cloudwatch_data['network_in_mb'].fillna(
    method='ffill'
)

# SOLUTION 4: Fill categorical with mode (most frequent value)
cloudwatch_data['region'] = cloudwatch_data['region'].fillna(
    cloudwatch_data['region'].mode()[0]
)

print("\nData After Handling Missing Values:")
print(cloudwatch_data.to_string(index=False))
print(f"\nMissing values after handling:")
print(cloudwatch_data.isnull().sum())
```

---

## 📚 Section 8: (E) Outlier Handling

### 🚨 Dealing with Extreme Values

```
┌─────────────────────────────────────────────────────────────────┐
│                    OUTLIER HANDLING                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│   WHAT: Values that are too different from others                │
│   ─────                                                          │
│   Normal Lambda execution: 50-500 ms                             │
│   Suddenly: 50000 ms (timeout!) ← OUTLIER                        │
│                                                                  │
│   WHY IT'S A PROBLEM:                                            │
│   ───────────────────                                            │
│   • Outliers confuse models                                      │
│   • Skew the mean                                                │
│   • Cause overfitting                                            │
│                                                                  │
│   SOLUTIONS:                                                     │
│   ──────────                                                     │
│   1. REMOVE outlier rows                                         │
│   2. CAP values (winsorization)                                  │
│   3. Apply LOG transformation                                    │
│   4. Use IQR method to detect                                    │
│                                                                  │
│   IQR METHOD:                                                    │
│   ────────────                                                   │
│   Q1 = 25th percentile                                           │
│   Q3 = 75th percentile                                           │
│   IQR = Q3 - Q1                                                  │
│   Outliers = values < Q1-1.5×IQR or > Q3+1.5×IQR                 │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### 💻 Code Example: Outlier Detection in Lambda Execution Times

```python
import pandas as pd
import numpy as np

# Lambda execution data with outliers
lambda_data = pd.DataFrame({
    'function_name': ['func_' + str(i) for i in range(15)],
    'execution_time_ms': [50, 80, 100, 120, 90, 110, 95, 85, 
                          5000,  # ← Outlier (cold start)
                          105, 115, 88, 92, 
                          30000,  # ← Outlier (timeout)
                          102]
})

print("Original Data:")
print(lambda_data.to_string(index=False))
print(f"\nStatistics:")
print(f"   Mean: {lambda_data['execution_time_ms'].mean():.2f} ms")
print(f"   Median: {lambda_data['execution_time_ms'].median():.2f} ms")

# DETECTING OUTLIERS using IQR method
Q1 = lambda_data['execution_time_ms'].quantile(0.25)
Q3 = lambda_data['execution_time_ms'].quantile(0.75)
IQR = Q3 - Q1

lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR

print(f"\n📊 IQR Analysis:")
print(f"   Q1 (25%): {Q1}")
print(f"   Q3 (75%): {Q3}")
print(f"   IQR: {IQR}")
print(f"   Lower bound: {lower_bound}")
print(f"   Upper bound: {upper_bound}")

# Find outliers
outliers = lambda_data[
    (lambda_data['execution_time_ms'] < lower_bound) | 
    (lambda_data['execution_time_ms'] > upper_bound)
]
print(f"\n🚨 Outliers Found:")
print(outliers.to_string(index=False))

# SOLUTION 1: Remove outliers
clean_data = lambda_data[
    (lambda_data['execution_time_ms'] >= lower_bound) & 
    (lambda_data['execution_time_ms'] <= upper_bound)
]

print(f"\n✅ Clean Data (outliers removed):")
print(f"   Original rows: {len(lambda_data)}")
print(f"   Clean rows: {len(clean_data)}")
print(f"   New Mean: {clean_data['execution_time_ms'].mean():.2f} ms")

# SOLUTION 2: Cap outliers (winsorization)
lambda_data['execution_capped'] = lambda_data['execution_time_ms'].clip(
    lower=lower_bound, upper=upper_bound
)
print(f"\n✅ Capped Data (outliers limited):")
print(f"   Max value after capping: {lambda_data['execution_capped'].max():.2f} ms")
```

---

## 📚 Section 9: Complete AWS Feature Engineering Pipeline

### 💻 Full Example: CI/CD Pipeline Success Prediction

```python
"""
Complete Feature Engineering Pipeline
=====================================
Predicting CI/CD Pipeline Success based on various features

This demonstrates all feature engineering techniques:
- Feature Creation
- Feature Transformation  
- Encoding
- Missing Data Handling
- Outlier Handling
"""

import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

print("=" * 60)
print("🔧 COMPLETE FEATURE ENGINEERING PIPELINE")
print("   CI/CD Pipeline Success Prediction")
print("=" * 60)

# Create raw CI/CD pipeline data
np.random.seed(42)
n_samples = 100

raw_data = pd.DataFrame({
    'pipeline_id': [f'pipe_{i}' for i in range(n_samples)],
    'repo_name': np.random.choice(['backend', 'frontend', 'api', 'infra'], n_samples),
    'branch': np.random.choice(['main', 'develop', 'feature'], n_samples),
    'num_commits': np.random.randint(1, 50, n_samples),
    'code_coverage': np.random.uniform(40, 100, n_samples),
    'test_count': np.random.randint(10, 500, n_samples),
    'build_time_sec': np.random.randint(30, 600, n_samples),
    'docker_image_size_mb': np.random.uniform(50, 2000, n_samples),
    'previous_failures': np.random.randint(0, 10, n_samples),
    'hour_of_day': np.random.randint(0, 24, n_samples),
    'day_of_week': np.random.choice(['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'], n_samples)
})

# Add some missing values (realistic scenario)
raw_data.loc[np.random.choice(n_samples, 5), 'code_coverage'] = np.nan
raw_data.loc[np.random.choice(n_samples, 3), 'test_count'] = np.nan

# Add outliers
raw_data.loc[0, 'build_time_sec'] = 5000  # Outlier
raw_data.loc[5, 'docker_image_size_mb'] = 10000  # Outlier

# Create target (success based on features)
success_score = (
    raw_data['code_coverage'].fillna(70) * 0.3 +
    (100 - raw_data['previous_failures'] * 10) * 0.3 +
    (raw_data['test_count'].fillna(100) / 5) * 0.2 +
    np.random.normal(0, 10, n_samples)
)
raw_data['success'] = (success_score > 50).astype(int)

print("\n📋 RAW DATA (first 10 rows):")
print(raw_data.head(10).to_string(index=False))

print(f"\n❓ Missing Values:")
print(raw_data.isnull().sum())

# ============================================================
# STEP 1: HANDLE MISSING DATA
# ============================================================
print("\n" + "=" * 60)
print("STEP 1: HANDLING MISSING DATA")
print("=" * 60)

data = raw_data.copy()

# Fill numeric missing values with median
data['code_coverage'] = data['code_coverage'].fillna(data['code_coverage'].median())
data['test_count'] = data['test_count'].fillna(data['test_count'].median())

print(f"✅ Missing values after handling: {data.isnull().sum().sum()}")

# ============================================================
# STEP 2: HANDLE OUTLIERS
# ============================================================
print("\n" + "=" * 60)
print("STEP 2: HANDLING OUTLIERS")
print("=" * 60)

# Cap build_time using IQR
Q1 = data['build_time_sec'].quantile(0.25)
Q3 = data['build_time_sec'].quantile(0.75)
IQR = Q3 - Q1
upper_limit = Q3 + 1.5 * IQR

data['build_time_sec'] = data['build_time_sec'].clip(upper=upper_limit)

# Cap docker image size
data['docker_image_size_mb'] = data['docker_image_size_mb'].clip(upper=2000)

print(f"✅ Outliers capped")
print(f"   Max build time: {data['build_time_sec'].max():.0f} sec")
print(f"   Max image size: {data['docker_image_size_mb'].max():.0f} MB")

# ============================================================
# STEP 3: FEATURE CREATION
# ============================================================
print("\n" + "=" * 60)
print("STEP 3: FEATURE CREATION")
print("=" * 60)

# Create new features
data['tests_per_commit'] = data['test_count'] / data['num_commits']
data['coverage_ratio'] = data['code_coverage'] / 100
data['build_efficiency'] = data['test_count'] / data['build_time_sec']
data['is_main_branch'] = (data['branch'] == 'main').astype(int)
data['is_weekend'] = data['day_of_week'].isin(['Sat', 'Sun']).astype(int)
data['is_working_hours'] = ((data['hour_of_day'] >= 9) & (data['hour_of_day'] <= 18)).astype(int)
data['failure_risk'] = data['previous_failures'] / 10  # Normalized

print("✅ New features created:")
print("   • tests_per_commit")
print("   • coverage_ratio")
print("   • build_efficiency")
print("   • is_main_branch")
print("   • is_weekend")
print("   • is_working_hours")
print("   • failure_risk")

# ============================================================
# STEP 4: FEATURE TRANSFORMATION
# ============================================================
print("\n" + "=" * 60)
print("STEP 4: FEATURE TRANSFORMATION")
print("=" * 60)

# Log transform skewed features
data['log_docker_size'] = np.log1p(data['docker_image_size_mb'])
data['log_build_time'] = np.log1p(data['build_time_sec'])

# Standard scaling for numerical features
scaler = StandardScaler()
numerical_cols = ['num_commits', 'test_count', 'build_time_sec']
data[['commits_scaled', 'tests_scaled', 'build_scaled']] = scaler.fit_transform(
    data[numerical_cols]
)

print("✅ Features transformed:")
print("   • Log transformation applied to docker_size, build_time")
print("   • Standard scaling applied to commits, tests, build_time")

# ============================================================
# STEP 5: ENCODING CATEGORICAL FEATURES
# ============================================================
print("\n" + "=" * 60)
print("STEP 5: ENCODING CATEGORICAL FEATURES")
print("=" * 60)

# One-hot encoding for repo_name
repo_dummies = pd.get_dummies(data['repo_name'], prefix='repo')
data = pd.concat([data, repo_dummies], axis=1)

# Label encoding for branch
le = LabelEncoder()
data['branch_encoded'] = le.fit_transform(data['branch'])

# Label encoding for day_of_week (ordinal)
day_order = {'Mon': 0, 'Tue': 1, 'Wed': 2, 'Thu': 3, 'Fri': 4, 'Sat': 5, 'Sun': 6}
data['day_encoded'] = data['day_of_week'].map(day_order)

print("✅ Categorical features encoded:")
print("   • repo_name: One-hot encoded")
print("   • branch: Label encoded")
print("   • day_of_week: Ordinal encoded")

# ============================================================
# STEP 6: FINAL FEATURE SET
# ============================================================
print("\n" + "=" * 60)
print("STEP 6: FINAL FEATURE SET")
print("=" * 60)

# Select features for model
feature_columns = [
    'coverage_ratio', 'tests_per_commit', 'build_efficiency',
    'is_main_branch', 'is_weekend', 'is_working_hours', 'failure_risk',
    'log_docker_size', 'log_build_time',
    'commits_scaled', 'tests_scaled', 'build_scaled',
    'branch_encoded', 'day_encoded',
    'repo_api', 'repo_backend', 'repo_frontend', 'repo_infra'
]

X = data[feature_columns]
y = data['success']

print(f"✅ Final feature set: {len(feature_columns)} features")
print(f"   Features: {feature_columns}")

# ============================================================
# STEP 7: TRAIN MODEL
# ============================================================
print("\n" + "=" * 60)
print("STEP 7: TRAIN MODEL WITH ENGINEERED FEATURES")
print("=" * 60)

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42
)

model = LogisticRegression(random_state=42, max_iter=1000)
model.fit(X_train, y_train)

y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)

print(f"✅ Model trained successfully!")
print(f"   Training samples: {len(X_train)}")
print(f"   Testing samples: {len(X_test)}")
print(f"   Accuracy: {accuracy * 100:.1f}%")

# Feature importance
feature_importance = pd.DataFrame({
    'feature': feature_columns,
    'importance': np.abs(model.coef_[0])
}).sort_values('importance', ascending=False)

print(f"\n📊 Top 5 Important Features:")
print(feature_importance.head().to_string(index=False))
```

---

## 📚 Section 10: Feature Engineering in MLOps

### 🔧 Where Feature Engineering Fits in DevOps Pipeline

```
┌─────────────────────────────────────────────────────────────────┐
│              FEATURE ENGINEERING IN MLOps                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│   DevOps Stage           How Feature Engineering is Used         │
│   ─────────────           ───────────────────────────────        │
│   Data Pipeline (ETL)    Cleaning data before training           │
│   AWS Glue / Lambda      Automating feature transformations      │
│   Airflow / Prefect      Orchestrating feature generation        │
│   Docker + CI/CD         Packaging preprocessing code            │
│   MLflow                 Tracking version of feature sets        │
│   Feature Store (Feast)  Storing reusable features               │
│   SageMaker              Built-in feature engineering tools      │
│                                                                  │
│   FEATURE STORE CONCEPT:                                         │
│   ──────────────────────                                         │
│   ┌─────────────────────────────────────────────────────────┐   │
│   │  Instead of recreating features for each model:          │   │
│   │                                                          │   │
│   │  Store them ONCE → Reuse EVERYWHERE                      │   │
│   │                                                          │   │
│   │  AWS Feast / SageMaker Feature Store:                    │   │
│   │  • Centralized feature storage                           │   │
│   │  • Feature versioning                                    │   │
│   │  • Online + offline serving                              │   │
│   │  • Feature sharing across teams                          │   │
│   └─────────────────────────────────────────────────────────┘   │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 📚 Section 11: Summary

### 📋 Key Takeaways

| Technique | What It Does | AWS/DevOps Example |
|-----------|--------------|-------------------|
| **Feature Creation** | Create new columns | cost_per_hour = cost / hours |
| **Transformation** | Change data form | log(invocations), scaling |
| **Encoding** | Text → Numbers | region → one-hot encoded |
| **Missing Data** | Fix NaN values | Fill CloudWatch gaps with mean |
| **Outlier Handling** | Remove extremes | Cap Lambda timeouts |

### 🎯 Why Feature Engineering Matters

```
┌─────────────────────────────────────────────────────────────────┐
│                  WITHOUT vs WITH                                 │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│   WITHOUT Feature Engineering:     WITH Feature Engineering:     │
│   ──────────────────────────       ─────────────────────────     │
│   ❌ Model gets confused           ✅ Model learns patterns      │
│   ❌ Accuracy reduces              ✅ Predictions improve        │
│   ❌ Loss increases                ✅ Training becomes stable    │
│   ❌ Model overfits                ✅ Better generalization      │
│                                                                  │
│   🎯 Feature Engineering is 70% of a real ML job!                │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 📚 Homework

1. **Create 3 new features** for EC2 cost prediction
2. **Apply log transformation** to skewed data
3. **Handle missing values** in a CloudWatch metrics dataset
4. **Encode categorical features** like region and instance_type
5. **Detect and remove outliers** from Lambda execution times

---

## 🔗 Connection to Other Days

```
┌─────────────────────────────────────────────────────────────────┐
│                    LEARNING PROGRESSION                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│   Day 38: Cost Function                                          │
│   ──────────────────────                                         │
│   Measure how wrong the model is                                 │
│                                                                  │
│   Day 39: Feature Engineering (TODAY)                            │
│   ────────────────────────────────────                           │
│   Improve data so model learns better                            │
│                                                                  │
│   Day 40: Gradient Descent (NEXT)                                │
│   ───────────────────────────────                                │
│   How model reduces the cost using features                      │
│                                                                  │
│   FLOW: Better Features → Lower Cost → Better Model              │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

**Next: Day 40 — Gradient Descent: How Models Learn** 🚀


