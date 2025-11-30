# 🎯 Complete ML Monitoring Setup Guide
## AWS EC2 CPU + Disk Monitoring with ML Prediction & SNS Alerts

---

# Table of Contents

1. [Project Overview](#1-project-overview)
2. [Prerequisites](#2-prerequisites)
3. [Phase 1: AWS Account Setup](#3-phase-1-aws-account-setup)
4. [Phase 2: IAM User Creation](#4-phase-2-iam-user-creation)
5. [Phase 3: Launch EC2 Instance (Ubuntu)](#5-phase-3-launch-ec2-instance-ubuntu)
6. [Phase 4: Connect to EC2 via SSH](#6-phase-4-connect-to-ec2-via-ssh)
7. [Phase 5: Install Required Software](#7-phase-5-install-required-software)
8. [Phase 6: Configure AWS Credentials](#8-phase-6-configure-aws-credentials)
9. [Phase 7: Create Project Structure](#9-phase-7-create-project-structure)
10. [Phase 8: Setup Virtual Environment](#10-phase-8-setup-virtual-environment)
11. [Phase 9: Create All Project Files](#11-phase-9-create-all-project-files)
12. [Phase 10: Create SNS Topic for Alerts](#12-phase-10-create-sns-topic-for-alerts)
13. [Phase 11: Install CloudWatch Agent (For Disk Metrics)](#13-phase-11-install-cloudwatch-agent-for-disk-metrics)
14. [Phase 12: Train the ML Model](#14-phase-12-train-the-ml-model)
15. [Phase 13: Run Continuous Monitoring](#15-phase-13-run-continuous-monitoring)
16. [Phase 14: Testing the System](#16-phase-14-testing-the-system)
17. [Troubleshooting](#17-troubleshooting)
18. [Project Architecture](#18-project-architecture)
19. [All Code Files Reference](#19-all-code-files-reference)

---

# 1. Project Overview

## What This Project Does

This project creates an ML-powered monitoring system that:

| Feature | Description |
|---------|-------------|
| **CPU Monitoring** | Fetches real CPU metrics from AWS CloudWatch |
| **Disk Monitoring** | Fetches disk usage via CloudWatch Agent |
| **ML Prediction** | Predicts CPU usage 1 hour ahead using Random Forest |
| **Spike Detection** | Detects sudden CPU/Disk spikes (+25%/+15%) |
| **Threshold Alerts** | Alerts when CPU ≥80% or Disk ≥85% |
| **SNS Notifications** | Sends email alerts via AWS SNS |
| **Continuous Monitoring** | Runs every 30 seconds |

## ML Concepts Used (Day 31-39)

| Day | Concept | How It's Used |
|-----|---------|---------------|
| 31 | ML Basics | Building prediction system |
| 32 | Supervised Learning | Training model on historical data |
| 35-36 | Model Evaluation | RMSE, R² metrics |
| 38 | Cost Function | Optimizing predictions |
| 39 | Feature Engineering | Creating 38+ features from raw data |

---

# 2. Prerequisites

## Required Accounts
- [ ] AWS Account (Free Tier eligible)
- [ ] Email address for SNS notifications

## Required Knowledge
- Basic terminal/command line usage
- Basic Python understanding (helpful but not required)

## Tools Used
- AWS Services: EC2, CloudWatch, SNS, IAM
- Python 3.10+
- SSH Client (built into Windows PowerShell/Mac Terminal)

---

# 3. Phase 1: AWS Account Setup

## Step 3.1: Create AWS Account

1. **Go to AWS website**
   ```
   https://aws.amazon.com/
   ```

2. **Click "Create an AWS Account"**

3. **Enter account details:**
   - Email address
   - Password
   - Account name (e.g., "my-learning-account")

4. **Enter contact information:**
   - Full name
   - Phone number
   - Country
   - Address

5. **Add payment method:**
   - Credit/Debit card required
   - You won't be charged if staying within Free Tier

6. **Verify phone number:**
   - Enter verification code sent via SMS

7. **Select support plan:**
   - Choose "Basic Support - Free"

8. **Wait for activation:**
   - Usually takes 1-5 minutes
   - You'll receive confirmation email

---

# 4. Phase 2: IAM User Creation

## Why IAM User?
- Never use root account for daily operations
- IAM users have limited, specific permissions
- Better security practice

## Step 4.1: Access IAM Console

1. **Login to AWS Console:**
   ```
   https://console.aws.amazon.com/
   ```

2. **Search for "IAM" in the search bar**

3. **Click on "IAM" service**

## Step 4.2: Create New User

1. **Click "Users" in left sidebar**

2. **Click "Create user" button**

3. **Enter user details:**
   ```
   User name: ml-monitoring-user
   ```

4. **Click "Next"**

## Step 4.3: Set Permissions

1. **Select "Attach policies directly"**

2. **Search and check these policies:**
   - [ ] `CloudWatchReadOnlyAccess`
   - [ ] `AmazonEC2ReadOnlyAccess`
   - [ ] `CloudWatchAgentServerPolicy`
   - [ ] `AmazonSNSFullAccess`

3. **Click "Next"**

4. **Click "Create user"**

## Step 4.4: Create Access Keys

1. **Click on the user name you just created**

2. **Go to "Security credentials" tab**

3. **Scroll down to "Access keys"**

4. **Click "Create access key"**

5. **Select "Command Line Interface (CLI)"**

6. **Check the confirmation checkbox**

7. **Click "Next"**

8. **Click "Create access key"**

9. **⚠️ IMPORTANT: Download the CSV file or copy both keys:**
   ```
   Access Key ID: AKIA...............
   Secret Access Key: xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
   ```
   
   **Save these securely - you won't see the secret key again!**

---

# 5. Phase 3: Launch EC2 Instance (Ubuntu)

## Step 5.1: Navigate to EC2

1. **Go to AWS Console**

2. **Search "EC2" and click on it**

3. **Click "Launch instance"**

## Step 5.2: Configure Instance

### Name and Tags
```
Name: ml-monitoring-ubuntu
```

### Application and OS Images (AMI)
```
Select: Ubuntu Server 22.04 LTS (Free tier eligible)
Architecture: 64-bit (x86)
```

### Instance Type
```
Select: t2.micro (Free tier eligible)
         OR
         t2.medium (if you need more power)
```

### Key Pair (Login)
1. **Click "Create new key pair"**
2. **Enter details:**
   ```
   Key pair name: ml-ubuntu-key
   Key pair type: RSA
   Private key file format: .pem
   ```
3. **Click "Create key pair"**
4. **⚠️ Download the .pem file and save it securely**

### Network Settings
1. **Click "Edit"**
2. **Configure:**
   ```
   VPC: Default
   Subnet: No preference
   Auto-assign public IP: Enable
   
   Security group: Create security group
   Security group name: ml-monitoring-sg
   
   Inbound rules:
   - Type: SSH, Source: My IP
   ```

### Configure Storage
```
Size: 15 GiB (or more)
Volume type: gp3
```

### Advanced Details
```
Leave default settings
```

## Step 5.3: Launch Instance

1. **Review all settings**

2. **Click "Launch instance"**

3. **Wait for instance to show "Running" status**

4. **Note down the Public IP address:**
   ```
   Example: 54.123.45.67
   ```

---

# 6. Phase 4: Connect to EC2 via SSH

## Step 6.1: Prepare Key File

### On Windows (PowerShell):
```powershell
# Navigate to Downloads folder
cd C:\Users\YourUsername\Downloads

# No chmod needed on Windows
```

### On Mac/Linux:
```bash
# Navigate to Downloads folder
cd ~/Downloads

# Set correct permissions
chmod 400 ml-ubuntu-key.pem
```

## Step 6.2: Connect via SSH

### Command Format:
```bash
ssh -i "ml-ubuntu-key.pem" ubuntu@YOUR_PUBLIC_IP
```

### Example:
```bash
ssh -i "ml-ubuntu-key.pem" ubuntu@54.123.45.67
```

## Step 6.3: First Connection

1. **When prompted "Are you sure you want to continue connecting?"**
   ```
   Type: yes
   Press: Enter
   ```

2. **You should see:**
   ```
   Welcome to Ubuntu 22.04.3 LTS
   ubuntu@ip-172-31-xx-xx:~$
   ```

**🎉 You are now connected to your EC2 instance!**

---

# 7. Phase 5: Install Required Software

## Step 7.1: Update System Packages

```bash
sudo apt update
```

```bash
sudo apt upgrade -y
```

## Step 7.2: Install Python

```bash
sudo apt install python3 python3-pip python3-venv -y
```

## Step 7.3: Verify Python Installation

```bash
python3 --version
```

**Expected output:**
```
Python 3.10.x (or higher)
```

## Step 7.4: Install AWS CLI

```bash
sudo apt install awscli -y
```

## Step 7.5: Verify AWS CLI Installation

```bash
aws --version
```

**Expected output:**
```
aws-cli/2.x.x Python/3.x.x Linux/...
```

## Step 7.6: Install Additional Tools

```bash
sudo apt install stress -y
```

**This installs the stress tool for testing CPU load**

---

# 8. Phase 6: Configure AWS Credentials

## Step 8.1: Run AWS Configure

```bash
aws configure
```

## Step 8.2: Enter Your Credentials

When prompted, enter:

```
AWS Access Key ID [None]: YOUR_ACCESS_KEY_ID
AWS Secret Access Key [None]: YOUR_SECRET_ACCESS_KEY
Default region name [None]: us-east-1
Default output format [None]: json
```

**Replace with your actual keys from Phase 2**

## Step 8.3: Verify Configuration

```bash
aws sts get-caller-identity
```

**Expected output:**
```json
{
    "UserId": "AIDAXXXXXXXXXXXXXXXXX",
    "Account": "123456789012",
    "Arn": "arn:aws:iam::123456789012:user/ml-monitoring-user"
}
```

## Step 8.4: Test EC2 Access

```bash
aws ec2 describe-instances --query 'Reservations[*].Instances[*].[InstanceId,State.Name]' --output table
```

**Should show your instance ID and "running" status**

---

# 9. Phase 7: Create Project Structure

## Step 9.1: Create Main Project Directory

```bash
cd ~
mkdir ml-monitoring
cd ml-monitoring
```

## Step 9.2: Create Sub-Directories

```bash
mkdir -p src data models logs
```

## Step 9.3: Verify Structure

```bash
ls -la
```

**Expected output:**
```
drwxrwxr-x 2 ubuntu ubuntu 4096 data
drwxrwxr-x 2 ubuntu ubuntu 4096 logs
drwxrwxr-x 2 ubuntu ubuntu 4096 models
drwxrwxr-x 2 ubuntu ubuntu 4096 src
```

## Step 9.4: Check Current Location

```bash
pwd
```

**Expected output:**
```
/home/ubuntu/ml-monitoring
```

---

# 10. Phase 8: Setup Virtual Environment

## Step 10.1: Create Virtual Environment

```bash
python3 -m venv venv
```

## Step 10.2: Activate Virtual Environment

```bash
source venv/bin/activate
```

**Your prompt should change to:**
```
(venv) ubuntu@ip-172-31-xx-xx:~/ml-monitoring$
```

## Step 10.3: Upgrade pip

```bash
pip install --upgrade pip
```

## Step 10.4: Verify Virtual Environment

```bash
which python
```

**Expected output:**
```
/home/ubuntu/ml-monitoring/venv/bin/python
```

---

# 11. Phase 9: Create All Project Files

## Step 11.1: Create requirements.txt

```bash
cat > requirements.txt << 'EOF'
pandas==2.1.4
numpy==1.26.2
scikit-learn==1.3.2
joblib==1.3.2
boto3==1.34.0
matplotlib==3.8.2
seaborn==0.13.0
EOF
```

## Step 11.2: Install Python Packages

```bash
pip install -r requirements.txt
```

**Wait for installation to complete (may take 2-3 minutes)**

## Step 11.3: Create config.py

```bash
cat > config.py << 'EOF'
"""
Configuration for ML Monitoring Project
CPU + Disk Monitoring
"""

# Alert thresholds (percentage)
THRESHOLDS = {
    # CPU thresholds
    'cpu_warning': 70,
    'cpu_critical': 80,
    
    # Disk thresholds
    'disk_warning': 75,
    'disk_critical': 85,
    
    # Memory thresholds (if using)
    'memory_warning': 80,
    'memory_critical': 95
}

# Spike detection thresholds
SPIKE_CONFIG = {
    'cpu_spike_threshold': 25,    # Alert if CPU jumps +25%
    'disk_spike_threshold': 15    # Alert if Disk jumps +15%
}

# ML settings
ML_CONFIG = {
    'prediction_hours_ahead': 1,
    'training_window_days': 30,
    'model_type': 'random_forest'
}

# EC2 pricing (USD per hour)
EC2_PRICING = {
    't2.micro': 0.0116,
    't2.small': 0.0232,
    't2.medium': 0.0464,
    't2.large': 0.0928,
    't3.micro': 0.0104,
    't3.small': 0.0208,
}

# EBS pricing (USD per GB per month)
EBS_PRICING = {
    'gp2': 0.10,
    'gp3': 0.08,
}

# SNS Configuration - UPDATE THIS WITH YOUR ARN!
SNS_CONFIG = {
    'enabled': True,
    'topic_arn': 'arn:aws:sns:us-east-1:YOUR_ACCOUNT_ID:ml-cpu-alerts',  # <-- UPDATE THIS
    'region': 'us-east-1'
}

# Alert settings
ALERT_CONFIG = {
    'console_alerts': True,
    'log_alerts': True,
    'sns_alerts': True,
    'log_file': 'logs/alerts.log'
}

# AWS Region
AWS_REGION = 'us-east-1'
EOF
```

## Step 11.4: Create src/__init__.py

```bash
touch src/__init__.py
```

## Step 11.5: Create src/data_generator.py

```bash
cat > src/data_generator.py << 'EOF'
"""
Data Generator - Creates synthetic training data
Saves data to: data/training_data.csv
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os

def generate_metrics(days=30, instances=5, interval_minutes=5):
    print("=" * 60)
    print("📊 GENERATING TRAINING DATA")
    print("=" * 60)
    
    np.random.seed(42)
    total_minutes = days * 24 * 60
    n_points = total_minutes // interval_minutes
    
    print(f"   Days: {days}")
    print(f"   Instances: {instances}")
    print(f"   Data points per instance: {n_points}")
    
    data = []
    instance_types = ['t2.micro', 't2.small', 't2.medium', 't3.micro', 't3.small']
    start_date = datetime.now() - timedelta(days=days)
    
    for inst_idx in range(instances):
        instance_id = f'i-{np.random.randint(10000000, 99999999):08x}'
        instance_type = instance_types[inst_idx % len(instance_types)]
        base_cpu = np.random.uniform(20, 40)
        base_memory = np.random.uniform(30, 50)
        base_disk = np.random.uniform(40, 60)
        
        for i in range(n_points):
            timestamp = start_date + timedelta(minutes=i * interval_minutes)
            hour = timestamp.hour
            day_of_week = timestamp.weekday()
            
            hour_factor = 1.5 + 0.3 * np.sin((hour - 9) * np.pi / 9) if 9 <= hour <= 18 else 0.5
            weekend_factor = 0.4 if day_of_week >= 5 else 1.0
            spike_factor = np.random.uniform(1.5, 2.5) if np.random.random() < 0.05 else 1.0
            
            cpu = np.clip(base_cpu * hour_factor * weekend_factor * spike_factor + np.random.normal(0, 5), 0, 100)
            memory = np.clip(base_memory + (i / n_points) * 15 + np.random.normal(0, 3), 0, 100)
            disk = np.clip(base_disk + (i / n_points) * 10 + np.random.normal(0, 2), 0, 100)
            
            data.append({
                'timestamp': timestamp,
                'instance_id': instance_id,
                'instance_type': instance_type,
                'cpu_utilization': round(cpu, 2),
                'memory_utilization': round(memory, 2),
                'disk_utilization': round(disk, 2),
                'network_in_mb': round(max(0, base_cpu * 10 * hour_factor + np.random.normal(0, 50)), 2),
                'network_out_mb': round(max(0, base_cpu * 5 * hour_factor + np.random.normal(0, 30)), 2),
                'hour_of_day': hour,
                'day_of_week': day_of_week,
                'is_business_hours': 1 if 9 <= hour <= 18 else 0,
                'is_weekend': 1 if day_of_week >= 5 else 0
            })
    
    df = pd.DataFrame(data).sort_values(['instance_id', 'timestamp']).reset_index(drop=True)
    print(f"\n✅ Generated {len(df)} data points")
    return df

def create_target(df, hours_ahead=1):
    print(f"\n📎 Creating target variable ({hours_ahead}h ahead)")
    rows_shift = hours_ahead * 12
    df = df.copy()
    df['cpu_future'] = df.groupby('instance_id')['cpu_utilization'].shift(-rows_shift)
    df['will_exceed_threshold'] = (df['cpu_future'] > 70).astype(int)
    df = df.dropna(subset=['cpu_future'])
    print(f"   Rows with target: {len(df)}")
    return df

def save_data(df, filepath='data/training_data.csv'):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    df.to_csv(filepath, index=False)
    print(f"💾 Saved: {filepath}")

if __name__ == "__main__":
    df = generate_metrics(days=7, instances=3)
    df = create_target(df)
    save_data(df)
EOF
```

## Step 11.6: Create src/feature_engineering.py

```bash
cat > src/feature_engineering.py << 'EOF'
"""
Feature Engineering - Creates ML features
"""

import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings('ignore')

class FeatureEngineer:
    def __init__(self):
        # Simple mapping for instance types (no need for LabelEncoder)
        self.instance_type_map = {
            't2.micro': 0, 't2.small': 1, 't2.medium': 2, 't2.large': 3,
            't3.micro': 4, 't3.small': 5, 't3.medium': 6, 't3.large': 7,
            'm5.large': 8, 'm5.xlarge': 9, 'c5.large': 10, 'r5.large': 11
        }
    
    def create_features(self, df):
        print("\n🔧 FEATURE ENGINEERING")
        print("=" * 60)
        df = df.copy()
        
        if 'timestamp' in df.columns:
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            df['hour'] = df['timestamp'].dt.hour
            df['day_of_week'] = df['timestamp'].dt.dayofweek
            df['is_weekend'] = (df['day_of_week'] >= 5).astype(int)
            df['is_business_hours'] = ((df['hour'] >= 9) & (df['hour'] <= 18)).astype(int)
            df['hour_sin'] = np.sin(2 * np.pi * df['hour'] / 24)
            df['hour_cos'] = np.cos(2 * np.pi * df['hour'] / 24)
        
        for col in ['cpu_utilization', 'memory_utilization', 'disk_utilization']:
            if col in df.columns:
                if len(df) > 1:
                    df[f'{col}_rolling_mean'] = df.groupby('instance_id')[col].transform(lambda x: x.rolling(12, min_periods=1).mean())
                    df[f'{col}_rolling_std'] = df.groupby('instance_id')[col].transform(lambda x: x.rolling(12, min_periods=1).std())
                    df[f'{col}_rolling_max'] = df.groupby('instance_id')[col].transform(lambda x: x.rolling(12, min_periods=1).max())
                    df[f'{col}_lag_1'] = df.groupby('instance_id')[col].shift(1)
                    df[f'{col}_lag_3'] = df.groupby('instance_id')[col].shift(3)
                    df[f'{col}_diff'] = df.groupby('instance_id')[col].diff()
                else:
                    # For single row predictions
                    df[f'{col}_rolling_mean'] = df[col]
                    df[f'{col}_rolling_std'] = 0
                    df[f'{col}_rolling_max'] = df[col]
                    df[f'{col}_lag_1'] = df[col]
                    df[f'{col}_lag_3'] = df[col]
                    df[f'{col}_diff'] = 0
        
        if 'cpu_utilization' in df.columns and 'memory_utilization' in df.columns:
            df['cpu_memory_ratio'] = df['cpu_utilization'] / (df['memory_utilization'] + 0.01)
            df['system_stress'] = (df['cpu_utilization'] + df['memory_utilization'] + df.get('disk_utilization', 0)) / 3
        
        if 'cpu_utilization' in df.columns:
            df['cpu_distance_warning'] = 70 - df['cpu_utilization']
            df['cpu_elevated'] = (df['cpu_utilization'] > 50).astype(int)
        
        if 'network_in_mb' in df.columns:
            df['network_total'] = df['network_in_mb'] + df.get('network_out_mb', 0)
        
        print(f"   ✅ Created {len(df.columns)} features")
        return df
    
    def handle_missing(self, df):
        df = df.copy()
        for col in df.select_dtypes(include=[np.number]).columns:
            df[col] = df[col].fillna(df[col].mean() if len(df) > 1 else 0)
        return df.fillna(method='ffill').fillna(method='bfill').fillna(0)
    
    def encode(self, df):
        """Simple encoding without LabelEncoder"""
        df = df.copy()
        if 'instance_type' in df.columns:
            df['instance_type_encoded'] = df['instance_type'].map(self.instance_type_map).fillna(-1).astype(int)
        return df
    
    def get_features(self):
        return ['cpu_utilization', 'memory_utilization', 'disk_utilization', 'hour', 'is_weekend', 
                'is_business_hours', 'hour_sin', 'hour_cos', 'cpu_utilization_rolling_mean', 
                'cpu_utilization_rolling_std', 'cpu_utilization_rolling_max', 'memory_utilization_rolling_mean',
                'disk_utilization_rolling_mean', 'cpu_utilization_lag_1', 'cpu_utilization_lag_3',
                'cpu_utilization_diff', 'cpu_memory_ratio', 'system_stress', 'cpu_distance_warning',
                'cpu_elevated', 'network_total', 'instance_type_encoded']
    
    def fit_transform(self, df):
        df = self.create_features(df)
        df = self.handle_missing(df)
        df = self.encode(df)
        return df
    
    def transform(self, df):
        df = self.create_features(df)
        df = self.handle_missing(df)
        df = self.encode(df)
        return df
EOF
```

## Step 11.7: Create src/model_training.py

```bash
cat > src/model_training.py << 'EOF'
"""
ML Model Training
Saves model to: models/cpu_predictor.pkl
"""

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
import joblib
import os
from datetime import datetime

class CPUPredictor:
    def __init__(self):
        self.model = RandomForestRegressor(n_estimators=100, max_depth=10, random_state=42, n_jobs=-1)
        self.feature_columns = None
        self.metrics = {}
        self.trained = False
    
    def prepare_data(self, df, features):
        cols = [c for c in features if c in df.columns]
        X = df[cols].fillna(0).replace([np.inf, -np.inf], 0)
        return X, cols
    
    def train(self, df, target='cpu_future', features=None):
        print("\n" + "=" * 60)
        print("🎯 MODEL TRAINING")
        print("=" * 60)
        
        if features is None:
            features = [c for c in df.select_dtypes(include=[np.number]).columns if c not in [target, 'will_exceed_threshold']]
        
        self.feature_columns = features
        X, self.feature_columns = self.prepare_data(df, features)
        y = df[target].values
        
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        print(f"   Training samples: {len(X_train)}")
        print(f"   Testing samples: {len(X_test)}")
        
        self.model.fit(X_train, y_train)
        
        y_train_pred = self.model.predict(X_train)
        y_test_pred = self.model.predict(X_test)
        
        self.metrics = {
            'train_rmse': np.sqrt(mean_squared_error(y_train, y_train_pred)),
            'test_rmse': np.sqrt(mean_squared_error(y_test, y_test_pred)),
            'train_r2': r2_score(y_train, y_train_pred),
            'test_r2': r2_score(y_test, y_test_pred),
            'trained_at': datetime.now().isoformat()
        }
        
        print(f"\n📊 RESULTS")
        print(f"   Test RMSE: {self.metrics['test_rmse']:.2f}%")
        print(f"   Test R²: {self.metrics['test_r2']:.4f}")
        
        self.trained = True
        return self.metrics
    
    def predict(self, df):
        X, _ = self.prepare_data(df, self.feature_columns)
        return self.model.predict(X)
    
    def predict_with_confidence(self, df):
        X, _ = self.prepare_data(df, self.feature_columns)
        predictions = np.array([tree.predict(X) for tree in self.model.estimators_])
        mean_pred = np.mean(predictions, axis=0)
        std_pred = np.std(predictions, axis=0)
        return {'prediction': mean_pred, 'lower': mean_pred - 2*std_pred, 'upper': mean_pred + 2*std_pred}
    
    def save(self, path='models/cpu_predictor.pkl'):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        joblib.dump({'model': self.model, 'features': self.feature_columns, 'metrics': self.metrics}, path)
        print(f"\n💾 Model saved: {path}")
    
    def load(self, path='models/cpu_predictor.pkl'):
        data = joblib.load(path)
        self.model = data['model']
        self.feature_columns = data['features']
        self.metrics = data['metrics']
        self.trained = True
        return self
EOF
```

## Step 11.8: Create src/cost_calculator.py

```bash
cat > src/cost_calculator.py << 'EOF'
"""
AWS Cost Calculator
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import EC2_PRICING, EBS_PRICING

class CostCalculator:
    def __init__(self):
        self.ec2_prices = EC2_PRICING
        self.ebs_prices = EBS_PRICING
    
    def predict_monthly(self, instances, verbose=True):
        if verbose:
            print("\n" + "=" * 60)
            print("💰 AWS COST PREDICTION")
            print("=" * 60)
        
        total_ec2, total_ebs = 0, 0
        for inst in instances:
            itype = inst.get('instance_type', 't2.micro')
            count = inst.get('count', 1)
            hours = inst.get('hours_per_day', 24) * 30
            storage = inst.get('storage_gb', 8) * count
            
            ec2_cost = round(self.ec2_prices.get(itype, 0.0116) * hours * count, 2)
            ebs_cost = round(self.ebs_prices.get('gp3', 0.08) * storage, 2)
            total_ec2 += ec2_cost
            total_ebs += ebs_cost
            
            if verbose:
                print(f"\n   📦 {itype} x {count}")
                print(f"      EC2: ${ec2_cost:.2f}, EBS: ${ebs_cost:.2f}")
        
        total = round(total_ec2 + total_ebs + total_ec2 * 0.1, 2)
        if verbose:
            print(f"\n   💵 TOTAL: ${total:.2f}/month")
        return {'total': total}
EOF
```

## Step 11.9: Create src/alert_system.py

```bash
cat > src/alert_system.py << 'EOF'
"""
Alert System with CPU + Disk + SNS Integration
"""

import boto3
from datetime import datetime
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import THRESHOLDS, ALERT_CONFIG, SNS_CONFIG

class AlertSystem:
    def __init__(self):
        self.thresholds = THRESHOLDS
        self.sns_enabled = SNS_CONFIG.get('enabled', False) and ALERT_CONFIG.get('sns_alerts', False)
        
        if self.sns_enabled:
            try:
                self.sns_client = boto3.client('sns', region_name=SNS_CONFIG.get('region', 'us-east-1'))
                self.topic_arn = SNS_CONFIG.get('topic_arn', '')
                print(f"   ✅ SNS enabled: {self.topic_arn}")
            except Exception as e:
                print(f"   ⚠️ SNS init failed: {e}")
                self.sns_enabled = False
    
    def check(self, metrics, predicted_cpu=None, predicted_disk=None):
        """Check CPU and Disk against thresholds"""
        alerts = []
        
        # ===== CPU Checks =====
        cpu = metrics.get('cpu_utilization', 0)
        
        if cpu >= self.thresholds['cpu_critical']:
            alerts.append({
                'type': 'CPU_CRITICAL',
                'metric': 'CPU',
                'value': cpu,
                'threshold': self.thresholds['cpu_critical'],
                'message': f'🚨 CPU CRITICAL: {cpu:.1f}% (threshold: {self.thresholds["cpu_critical"]}%)'
            })
        elif cpu >= self.thresholds['cpu_warning']:
            alerts.append({
                'type': 'CPU_WARNING',
                'metric': 'CPU',
                'value': cpu,
                'threshold': self.thresholds['cpu_warning'],
                'message': f'⚠️ CPU WARNING: {cpu:.1f}% (threshold: {self.thresholds["cpu_warning"]}%)'
            })
        
        # CPU Prediction
        if predicted_cpu is not None and predicted_cpu >= self.thresholds['cpu_critical']:
            alerts.append({
                'type': 'CPU_PREDICTION',
                'metric': 'CPU_PREDICTED',
                'value': predicted_cpu,
                'threshold': self.thresholds['cpu_critical'],
                'message': f'🔮 CPU PREDICTION: Will reach {predicted_cpu:.1f}% in 1 hour!'
            })
        
        # ===== Disk Checks =====
        disk = metrics.get('disk_utilization', 0)
        
        if disk >= self.thresholds['disk_critical']:
            alerts.append({
                'type': 'DISK_CRITICAL',
                'metric': 'DISK',
                'value': disk,
                'threshold': self.thresholds['disk_critical'],
                'message': f'🚨 DISK CRITICAL: {disk:.1f}% (threshold: {self.thresholds["disk_critical"]}%)'
            })
        elif disk >= self.thresholds['disk_warning']:
            alerts.append({
                'type': 'DISK_WARNING',
                'metric': 'DISK',
                'value': disk,
                'threshold': self.thresholds['disk_warning'],
                'message': f'⚠️ DISK WARNING: {disk:.1f}% (threshold: {self.thresholds["disk_warning"]}%)'
            })
        
        # Disk Prediction
        if predicted_disk is not None and predicted_disk >= self.thresholds['disk_critical']:
            alerts.append({
                'type': 'DISK_PREDICTION',
                'metric': 'DISK_PREDICTED',
                'value': predicted_disk,
                'threshold': self.thresholds['disk_critical'],
                'message': f'🔮 DISK PREDICTION: Will reach {predicted_disk:.1f}% in 1 hour!'
            })
        
        return alerts
    
    def send_sns_alert(self, alert, instance_info=None):
        """Send alert via AWS SNS"""
        if not self.sns_enabled or not self.topic_arn:
            return False
        
        try:
            subject = f"[{alert['type']}] EC2 Alert - {alert['metric']}"
            
            message = f"""
══════════════════════════════════════════════════════════
🚨 ML MONITORING ALERT
══════════════════════════════════════════════════════════

⏰ Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
📍 Alert Type: {alert['type']}
📊 Metric: {alert['metric']}

{alert['message']}

"""
            if instance_info:
                message += f"""
══════════════════════════════════════════════════════════
📋 INSTANCE DETAILS
══════════════════════════════════════════════════════════

🖥️  Instance ID: {instance_info.get('instance_id', 'N/A')}
📛 Name: {instance_info.get('name', 'N/A')}
📍 Type: {instance_info.get('instance_type', 'N/A')}
🌐 Public IP: {instance_info.get('public_ip', 'N/A')}
💾 Storage: {instance_info.get('total_storage_gb', 'N/A')} GB

"""
            
            message += """
══════════════════════════════════════════════════════════
⚡ ACTION REQUIRED
══════════════════════════════════════════════════════════

Please check your EC2 instance and take appropriate action.

══════════════════════════════════════════════════════════
"""
            
            response = self.sns_client.publish(
                TopicArn=self.topic_arn,
                Subject=subject[:100],
                Message=message
            )
            
            print(f"   📧 SNS Alert sent! MessageId: {response['MessageId']}")
            return True
            
        except Exception as e:
            print(f"   ❌ SNS Error: {e}")
            return False
    
    def send(self, alerts, instance_info=None):
        """Send all alerts"""
        for alert in alerts:
            # Console
            print(f"\n{'🔴' * 15}")
            print(f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            print(alert['message'])
            print(f"{'🔴' * 15}")
            
            # Log file
            if ALERT_CONFIG.get('log_alerts', True):
                log_file = ALERT_CONFIG.get('log_file', 'logs/alerts.log')
                os.makedirs(os.path.dirname(log_file), exist_ok=True)
                with open(log_file, 'a') as f:
                    f.write(f"{datetime.now().isoformat()} | {alert['type']} | {alert['message']}\n")
            
            # SNS (for critical and prediction alerts)
            if self.sns_enabled and ('CRITICAL' in alert['type'] or 'PREDICTION' in alert['type']):
                self.send_sns_alert(alert, instance_info)
EOF
```

## Step 11.10: Create main.py (Training Script)

```bash
cat > main.py << 'EOF'
"""
Main Application - Train ML Model
Run this first to generate training data and train the model
"""

import os
import sys
from datetime import datetime
import pandas as pd

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from data_generator import generate_metrics, create_target, save_data
from feature_engineering import FeatureEngineer
from model_training import CPUPredictor
from cost_calculator import CostCalculator
from alert_system import AlertSystem
from config import ML_CONFIG, THRESHOLDS

def main():
    print("\n" + "=" * 70)
    print("🐧 ML MONITORING - MODEL TRAINING")
    print("=" * 70)
    print(f"   Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Generate training data
    print("\n📊 Generating training data...")
    df = generate_metrics(days=14, instances=3)
    df = create_target(df, hours_ahead=ML_CONFIG['prediction_hours_ahead'])
    save_data(df)  # Saves to data/training_data.csv
    
    # Feature engineering
    fe = FeatureEngineer()
    df = fe.fit_transform(df)
    
    # Train model
    predictor = CPUPredictor()
    predictor.train(df, target='cpu_future', features=fe.get_features())
    predictor.save()  # Saves to models/cpu_predictor.pkl
    
    # Run test predictions
    print("\n" + "=" * 70)
    print("🔮 RUNNING TEST PREDICTIONS")
    print("=" * 70)
    
    alert_sys = AlertSystem()
    
    scenarios = [
        {'name': 'Normal', 'cpu_utilization': 45, 'memory_utilization': 50, 'disk_utilization': 40},
        {'name': 'Warning', 'cpu_utilization': 72, 'memory_utilization': 75, 'disk_utilization': 70},
        {'name': 'Critical', 'cpu_utilization': 88, 'memory_utilization': 85, 'disk_utilization': 82}
    ]
    
    for scenario in scenarios:
        print(f"\n📊 Scenario: {scenario['name']}")
        print(f"   Current CPU: {scenario['cpu_utilization']}%")
        
        current_df = pd.DataFrame([scenario])
        current_df['timestamp'] = datetime.now()
        current_df['instance_type'] = 't2.micro'
        current_df['instance_id'] = 'i-demo'
        current_df['network_in_mb'] = 50
        current_df['network_out_mb'] = 25
        current_df = fe.transform(current_df)
        
        result = predictor.predict_with_confidence(current_df)
        predicted = result['prediction'][0]
        print(f"   Predicted CPU (1h): {predicted:.1f}%")
        
        alerts = alert_sys.check(scenario, predicted_cpu=predicted)
        alert_sys.send(alerts)
    
    # Cost calculation
    calc = CostCalculator()
    calc.predict_monthly([
        {'instance_type': 't2.micro', 'count': 2, 'storage_gb': 30},
        {'instance_type': 't2.small', 'count': 1, 'storage_gb': 50}
    ])
    
    print("\n" + "=" * 70)
    print("✅ TRAINING COMPLETE!")
    print("=" * 70)
    print(f"""
   📁 Files created:
      • data/training_data.csv
      • models/cpu_predictor.pkl
      • logs/alerts.log
   
   Next step: Run 'python monitor_continuous.py' to start monitoring
    """)


if __name__ == "__main__":
    main()
EOF
```

## Step 11.11: Create monitor_continuous.py (Main Monitoring Script)

```bash
cat > monitor_continuous.py << 'EOF'
"""
Continuous ML Monitoring - CPU + DISK
======================================
Features:
- Monitors CPU and Disk every 30 seconds
- ML predicts future usage
- Detects sudden spikes
- Sends SNS email alerts
"""

import boto3
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import time
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from feature_engineering import FeatureEngineer
from model_training import CPUPredictor
from alert_system import AlertSystem
from config import THRESHOLDS, SNS_CONFIG, SPIKE_CONFIG

# ============================================================
# CONFIGURATION - UPDATE THESE VALUES
# ============================================================
INSTANCE_ID = "i-0a0ce6a68dca68120"  # <-- UPDATE WITH YOUR INSTANCE ID
REGION = "us-east-1"
CHECK_INTERVAL_SECONDS = 30
# ============================================================


class SpikeDetector:
    """Detects sudden spikes in CPU and Disk"""
    
    def __init__(self):
        self.cpu_spike_threshold = SPIKE_CONFIG.get('cpu_spike_threshold', 25)
        self.disk_spike_threshold = SPIKE_CONFIG.get('disk_spike_threshold', 15)
        
        self.previous_cpu = None
        self.previous_disk = None
        self.cpu_history = []
        self.disk_history = []
    
    def check_cpu_spike(self, current_cpu):
        spike_detected = False
        spike_info = None
        
        if self.previous_cpu is not None:
            change = current_cpu - self.previous_cpu
            if change >= self.cpu_spike_threshold:
                spike_detected = True
                spike_info = {
                    'type': 'CPU_SPIKE',
                    'previous': self.previous_cpu,
                    'current': current_cpu,
                    'change': change,
                    'message': f'⚡ CPU SPIKE: {self.previous_cpu:.1f}% → {current_cpu:.1f}% (+{change:.1f}%)'
                }
        
        self.cpu_history.append(current_cpu)
        if len(self.cpu_history) > 5:
            self.cpu_history.pop(0)
        self.previous_cpu = current_cpu
        
        return spike_detected, spike_info
    
    def check_disk_spike(self, current_disk):
        spike_detected = False
        spike_info = None
        
        if self.previous_disk is not None:
            change = current_disk - self.previous_disk
            if change >= self.disk_spike_threshold:
                spike_detected = True
                spike_info = {
                    'type': 'DISK_SPIKE',
                    'previous': self.previous_disk,
                    'current': current_disk,
                    'change': change,
                    'message': f'⚡ DISK SPIKE: {self.previous_disk:.1f}% → {current_disk:.1f}% (+{change:.1f}%)'
                }
        
        self.disk_history.append(current_disk)
        if len(self.disk_history) > 5:
            self.disk_history.pop(0)
        self.previous_disk = current_disk
        
        return spike_detected, spike_info


class ContinuousMonitor:
    """Main monitoring class for CPU + Disk"""
    
    def __init__(self, instance_id, region):
        self.instance_id = instance_id
        self.region = region
        self.cloudwatch = boto3.client('cloudwatch', region_name=region)
        self.ec2 = boto3.client('ec2', region_name=region)
        
        # Spike detector
        self.spike_detector = SpikeDetector()
        
        # Load ML model
        print("\n🤖 Loading ML Model...")
        self.predictor = CPUPredictor()
        self.predictor.load('models/cpu_predictor.pkl')
        print("   ✅ Model loaded!")
        
        self.fe = FeatureEngineer()
        
        # Alert system
        print("\n📧 Initializing Alert System...")
        self.alert_sys = AlertSystem()
        
        # Instance info
        self.instance_info = self.get_instance_info()
    
    def get_instance_info(self):
        print(f"\n📋 Fetching instance info: {self.instance_id}")
        try:
            response = self.ec2.describe_instances(InstanceIds=[self.instance_id])
            instance = response['Reservations'][0]['Instances'][0]
            name = next((t['Value'] for t in instance.get('Tags', []) if t['Key'] == 'Name'), 'No Name')
            
            volumes = []
            for bdm in instance.get('BlockDeviceMappings', []):
                vol_id = bdm.get('Ebs', {}).get('VolumeId')
                if vol_id:
                    vol_info = self.ec2.describe_volumes(VolumeIds=[vol_id])['Volumes'][0]
                    volumes.append({'size_gb': vol_info['Size']})
            
            info = {
                'instance_id': self.instance_id,
                'instance_type': instance['InstanceType'],
                'name': name,
                'state': instance['State']['Name'],
                'public_ip': instance.get('PublicIpAddress', 'N/A'),
                'total_storage_gb': sum(v['size_gb'] for v in volumes)
            }
            print(f"   ✅ {info['name']} ({info['instance_type']})")
            return info
        except Exception as e:
            print(f"   ❌ Error: {e}")
            return None
    
    def get_cpu_metrics(self):
        """Fetch CPU from CloudWatch (AWS/EC2 namespace)"""
        end_time = datetime.utcnow()
        start_time = end_time - timedelta(minutes=5)
        
        try:
            response = self.cloudwatch.get_metric_data(
                MetricDataQueries=[{
                    'Id': 'cpu',
                    'MetricStat': {
                        'Metric': {
                            'Namespace': 'AWS/EC2',
                            'MetricName': 'CPUUtilization',
                            'Dimensions': [{'Name': 'InstanceId', 'Value': self.instance_id}]
                        },
                        'Period': 60,
                        'Stat': 'Average'
                    },
                    'ReturnData': True
                }],
                StartTime=start_time,
                EndTime=end_time
            )
            values = response['MetricDataResults'][0]['Values']
            return max(values) if values else None
        except:
            return None
    
    def get_disk_metrics(self):
        """Fetch Disk from CloudWatch (CWAgent namespace)"""
        end_time = datetime.utcnow()
        start_time = end_time - timedelta(minutes=5)
        
        try:
            response = self.cloudwatch.get_metric_data(
                MetricDataQueries=[{
                    'Id': 'disk',
                    'MetricStat': {
                        'Metric': {
                            'Namespace': 'CWAgent',
                            'MetricName': 'disk_used_percent',
                            'Dimensions': [
                                {'Name': 'InstanceId', 'Value': self.instance_id},
                                {'Name': 'path', 'Value': '/'},
                                {'Name': 'device', 'Value': 'xvda1'},
                                {'Name': 'fstype', 'Value': 'ext4'}
                            ]
                        },
                        'Period': 60,
                        'Stat': 'Average'
                    },
                    'ReturnData': True
                }],
                StartTime=start_time,
                EndTime=end_time
            )
            values = response['MetricDataResults'][0]['Values']
            return max(values) if values else None
        except Exception as e:
            # Try alternative dimension names
            try:
                response = self.cloudwatch.get_metric_data(
                    MetricDataQueries=[{
                        'Id': 'disk',
                        'MetricStat': {
                            'Metric': {
                                'Namespace': 'CWAgent',
                                'MetricName': 'disk_used_percent',
                                'Dimensions': [
                                    {'Name': 'InstanceId', 'Value': self.instance_id},
                                    {'Name': 'path', 'Value': '/'}
                                ]
                            },
                            'Period': 60,
                            'Stat': 'Average'
                        },
                        'ReturnData': True
                    }],
                    StartTime=start_time,
                    EndTime=end_time
                )
                values = response['MetricDataResults'][0]['Values']
                return max(values) if values else None
            except:
                return None
    
    def predict_future(self, current_cpu, current_disk):
        """Use ML to predict future usage"""
        now = datetime.now()
        
        df = pd.DataFrame([{
            'timestamp': now,
            'instance_id': self.instance_id,
            'instance_type': self.instance_info['instance_type'],
            'cpu_utilization': current_cpu,
            'memory_utilization': 50.0,
            'disk_utilization': current_disk or 50.0,
            'network_in_mb': 20.0,
            'network_out_mb': 10.0,
            'hour_of_day': now.hour,
            'day_of_week': now.weekday(),
            'is_business_hours': 1 if 9 <= now.hour <= 18 else 0,
            'is_weekend': 1 if now.weekday() >= 5 else 0
        }])
        
        df_features = self.fe.transform(df)
        result = self.predictor.predict_with_confidence(df_features)
        predicted_cpu = result['prediction'][0]
        
        # Simple disk prediction (linear trend)
        predicted_disk = None
        if current_disk and len(self.spike_detector.disk_history) >= 2:
            disk_trend = np.mean(np.diff(self.spike_detector.disk_history))
            predicted_disk = current_disk + (disk_trend * 12)  # 1 hour ahead
            predicted_disk = max(0, min(100, predicted_disk))
        
        return predicted_cpu, predicted_disk
    
    def send_spike_alert(self, spike_info):
        """Send immediate alert for spike"""
        try:
            sns = boto3.client('sns', region_name=self.region)
            
            message = f"""
══════════════════════════════════════════════════════════
⚡ IMMEDIATE ALERT: {spike_info['type']} DETECTED!
══════════════════════════════════════════════════════════

⏰ Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

{spike_info['message']}

📊 Details:
   • Previous: {spike_info['previous']:.1f}%
   • Current: {spike_info['current']:.1f}%
   • Change: +{spike_info['change']:.1f}%

🖥️ Instance: {self.instance_info['name']} ({self.instance_id})

⚠️ ACTION REQUIRED: Check your instance immediately!

══════════════════════════════════════════════════════════
"""
            
            response = sns.publish(
                TopicArn=SNS_CONFIG['topic_arn'],
                Subject=f"⚡ {spike_info['type']}: Jumped to {spike_info['current']:.1f}%",
                Message=message
            )
            print(f"   📧 SPIKE ALERT SENT! MessageId: {response['MessageId']}")
        except Exception as e:
            print(f"   ❌ Failed to send spike alert: {e}")
    
    def check_and_alert(self):
        print(f"\n{'='*60}")
        print(f"⏰ CHECK: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'='*60}")
        
        # Get current metrics
        current_cpu = self.get_cpu_metrics()
        current_disk = self.get_disk_metrics()
        
        if current_cpu is None:
            print("   ⚠️ Could not fetch CPU metrics")
            return
        
        print(f"\n📊 CURRENT METRICS:")
        print(f"   CPU:  {current_cpu:.2f}%")
        print(f"   Disk: {current_disk:.2f}%" if current_disk else "   Disk: N/A (CloudWatch Agent required)")
        
        # Check for spikes
        cpu_spike, cpu_spike_info = self.spike_detector.check_cpu_spike(current_cpu)
        if cpu_spike:
            print(f"\n⚡ {cpu_spike_info['message']}")
            self.send_spike_alert(cpu_spike_info)
        
        if current_disk:
            disk_spike, disk_spike_info = self.spike_detector.check_disk_spike(current_disk)
            if disk_spike:
                print(f"\n⚡ {disk_spike_info['message']}")
                self.send_spike_alert(disk_spike_info)
        
        # ML Predictions
        predicted_cpu, predicted_disk = self.predict_future(current_cpu, current_disk)
        
        print(f"\n🔮 PREDICTIONS (1 hour ahead):")
        print(f"   CPU:  {predicted_cpu:.2f}%")
        if predicted_disk:
            print(f"   Disk: {predicted_disk:.2f}%")
        
        print(f"\n🎯 THRESHOLDS:")
        print(f"   CPU Critical:  {THRESHOLDS['cpu_critical']}%")
        print(f"   Disk Critical: {THRESHOLDS['disk_critical']}%")
        
        # Check thresholds
        alerts = self.alert_sys.check(
            {'cpu_utilization': current_cpu, 'disk_utilization': current_disk or 0},
            predicted_cpu=predicted_cpu,
            predicted_disk=predicted_disk
        )
        
        if alerts:
            print(f"\n🚨 {len(alerts)} ALERT(S) TRIGGERED!")
            self.alert_sys.send(alerts, instance_info=self.instance_info)
        elif not cpu_spike and not (current_disk and disk_spike):
            print(f"\n✅ All normal. No alerts.")
        
        # History
        if len(self.spike_detector.cpu_history) > 1:
            print(f"\n📈 CPU History: {' → '.join([f'{c:.1f}%' for c in self.spike_detector.cpu_history[-5:]])}")
        if len(self.spike_detector.disk_history) > 1:
            print(f"💾 Disk History: {' → '.join([f'{d:.1f}%' for d in self.spike_detector.disk_history[-5:]])}")
    
    def run_forever(self, interval_seconds=30):
        print("\n" + "="*60)
        print("🔄 STARTING CONTINUOUS MONITORING (CPU + DISK)")
        print("="*60)
        print(f"   Instance: {self.instance_id}")
        print(f"   Check interval: {interval_seconds} seconds")
        print(f"   CPU Threshold: {THRESHOLDS['cpu_critical']}%")
        print(f"   Disk Threshold: {THRESHOLDS['disk_critical']}%")
        print(f"   CPU Spike: +{SPIKE_CONFIG['cpu_spike_threshold']}%")
        print(f"   Disk Spike: +{SPIKE_CONFIG['disk_spike_threshold']}%")
        print(f"   Press Ctrl+C to stop")
        print("="*60)
        
        try:
            while True:
                self.check_and_alert()
                print(f"\n⏳ Next check in {interval_seconds} seconds...")
                time.sleep(interval_seconds)
        except KeyboardInterrupt:
            print("\n\n🛑 Monitoring stopped")


def main():
    print("\n" + "="*70)
    print("🔴 CONTINUOUS ML MONITORING (CPU + DISK)")
    print("="*70)
    
    monitor = ContinuousMonitor(INSTANCE_ID, REGION)
    
    if not monitor.instance_info or monitor.instance_info['state'] != 'running':
        print("❌ Instance not available")
        return
    
    monitor.run_forever(interval_seconds=CHECK_INTERVAL_SECONDS)


if __name__ == "__main__":
    main()
EOF
```

## Step 11.12: Verify All Files Created

```bash
ls -la
ls -la src/
```

**Expected output:**
```
# Main directory
config.py
main.py
monitor_continuous.py
requirements.txt
data/
logs/
models/
src/
venv/

# src directory
__init__.py
alert_system.py
cost_calculator.py
data_generator.py
feature_engineering.py
model_training.py
```

---

# 12. Phase 10: Create SNS Topic for Alerts

## Step 12.1: Go to SNS Console

1. **Login to AWS Console**

2. **Search "SNS" and click on it**

3. **Click "Topics" in left sidebar**

4. **Click "Create topic"**

## Step 12.2: Configure Topic

```
Type: Standard
Name: ml-cpu-alerts
Display name: ML CPU Alerts
```

**Click "Create topic"**

## Step 12.3: Copy Topic ARN

After creation, you'll see the Topic ARN:
```
arn:aws:sns:us-east-1:123456789012:ml-cpu-alerts
```

**Copy this ARN - you'll need it!**

## Step 12.4: Create Email Subscription

1. **On the topic page, click "Create subscription"**

2. **Configure:**
   ```
   Protocol: Email
   Endpoint: your-email@example.com
   ```

3. **Click "Create subscription"**

## Step 12.5: Confirm Email Subscription

1. **Check your email inbox**

2. **Find email from "AWS Notifications"**

3. **Click "Confirm subscription" link**

4. **You should see "Subscription confirmed!"**

## Step 12.6: Update config.py with Your ARN

```bash
nano config.py
```

Find the `SNS_CONFIG` section and update:
```python
SNS_CONFIG = {
    'enabled': True,
    'topic_arn': 'arn:aws:sns:us-east-1:YOUR_ACCOUNT_ID:ml-cpu-alerts',  # <-- UPDATE THIS
    'region': 'us-east-1'
}
```

**Save: Ctrl+O, Enter, Ctrl+X**

## Step 12.7: Test SNS

```bash
python3 -c "
import boto3
sns = boto3.client('sns', region_name='us-east-1')
response = sns.publish(
    TopicArn='YOUR_TOPIC_ARN_HERE',
    Subject='TEST from ML Monitoring',
    Message='This is a test. If you receive this, SNS is working!'
)
print(f'✅ SUCCESS! MessageId: {response[\"MessageId\"]}')
"
```

**Check your email!**

---

# 13. Phase 11: Install CloudWatch Agent (For Disk Metrics)

## Why CloudWatch Agent?
- AWS CloudWatch basic monitoring does NOT include disk metrics
- CloudWatch Agent must be installed to collect disk and memory metrics

## Step 13.1: Download CloudWatch Agent

```bash
wget https://s3.amazonaws.com/amazoncloudwatch-agent/ubuntu/amd64/latest/amazon-cloudwatch-agent.deb
```

## Step 13.2: Install Agent

```bash
sudo dpkg -i amazon-cloudwatch-agent.deb
```

## Step 13.3: Create Agent Configuration

```bash
sudo tee /opt/aws/amazon-cloudwatch-agent/etc/amazon-cloudwatch-agent.json << 'EOF'
{
    "agent": {
        "metrics_collection_interval": 60,
        "run_as_user": "root"
    },
    "metrics": {
        "namespace": "CWAgent",
        "metrics_collected": {
            "disk": {
                "measurement": ["used_percent", "free", "used"],
                "metrics_collection_interval": 60,
                "resources": ["/"]
            },
            "mem": {
                "measurement": ["mem_used_percent"],
                "metrics_collection_interval": 60
            }
        },
        "append_dimensions": {
            "InstanceId": "${aws:InstanceId}"
        }
    }
}
EOF
```

## Step 13.4: Start CloudWatch Agent

```bash
sudo /opt/aws/amazon-cloudwatch-agent/bin/amazon-cloudwatch-agent-ctl \
    -a fetch-config \
    -m ec2 \
    -s \
    -c file:/opt/aws/amazon-cloudwatch-agent/etc/amazon-cloudwatch-agent.json
```

## Step 13.5: Verify Agent Status

```bash
sudo /opt/aws/amazon-cloudwatch-agent/bin/amazon-cloudwatch-agent-ctl -a status
```

**Expected output:**
```json
{
  "status": "running",
  "starttime": "2024-...",
  "configstatus": "configured"
}
```

## Step 13.6: Wait for Data

Wait 2-3 minutes for disk metrics to appear in CloudWatch.

---

# 14. Phase 12: Train the ML Model

## Step 14.1: Ensure Virtual Environment is Active

```bash
cd ~/ml-monitoring
source venv/bin/activate
```

## Step 14.2: Run Training Script

```bash
python main.py
```

## Step 14.3: Expected Output

```
======================================================================
🐧 ML MONITORING - MODEL TRAINING
======================================================================
   Time: 2025-11-28 10:00:00

📊 Generating training data...
============================================================
📊 GENERATING TRAINING DATA
============================================================
   Days: 14
   Instances: 3
   Data points per instance: 4032

✅ Generated 12096 data points

📎 Creating target variable (1h ahead)
   Rows with target: 12060
💾 Saved: data/training_data.csv

🔧 FEATURE ENGINEERING
============================================================
   ✅ Created 40 features

============================================================
🎯 MODEL TRAINING
============================================================
   Training samples: 9648
   Testing samples: 2412

📊 RESULTS
   Test RMSE: 7.71%
   Test R²: 0.8746

💾 Model saved: models/cpu_predictor.pkl

======================================================================
✅ TRAINING COMPLETE!
======================================================================
```

## Step 14.4: Verify Files Created

```bash
ls -la data/
ls -la models/
```

**Should show:**
```
data/training_data.csv
models/cpu_predictor.pkl
```

---

# 15. Phase 13: Run Continuous Monitoring

## Step 15.1: Update Instance ID

Edit `monitor_continuous.py`:
```bash
nano monitor_continuous.py
```

Find and update:
```python
INSTANCE_ID = "i-YOUR_INSTANCE_ID"  # <-- Replace with your instance ID
```

**Save: Ctrl+O, Enter, Ctrl+X**

## Step 15.2: Run Monitoring (Foreground)

```bash
python monitor_continuous.py
```

## Step 15.3: Run Monitoring (Background)

```bash
nohup python monitor_continuous.py > logs/monitor.log 2>&1 &
```

## Step 15.4: Check Background Process

```bash
ps aux | grep monitor_continuous
```

## Step 15.5: View Logs

```bash
tail -f logs/monitor.log
```

## Step 15.6: Stop Monitoring

```bash
pkill -f monitor_continuous
```

---

# 16. Phase 14: Testing the System

## Test 1: CPU Stress Test

### Terminal 1 - Run Monitoring:
```bash
cd ~/ml-monitoring
source venv/bin/activate
python monitor_continuous.py
```

### Terminal 2 - Generate CPU Load:
```bash
stress --cpu 2 --timeout 120
```

### Expected Result:
- CPU spike detected
- SNS email received

## Test 2: Disk Space Test

### Create Large File:
```bash
dd if=/dev/zero of=/tmp/testfile bs=1M count=1000
```

### Check Disk:
```bash
df -h /
```

### Delete Test File:
```bash
rm /tmp/testfile
```

## Test 3: Direct SNS Test

```bash
python3 -c "
import boto3
from config import SNS_CONFIG
sns = boto3.client('sns', region_name='us-east-1')
response = sns.publish(
    TopicArn=SNS_CONFIG['topic_arn'],
    Subject='🧪 TEST Alert',
    Message='Test message from ML Monitoring'
)
print(f'✅ Sent! MessageId: {response[\"MessageId\"]}')
"
```

---

# 17. Troubleshooting

## Issue 1: "No CPU data found"

**Cause:** Instance might be new or CloudWatch hasn't collected data yet.

**Fix:** Wait 5-10 minutes for CloudWatch to collect data.

## Issue 2: "Disk: N/A"

**Cause:** CloudWatch Agent not installed or not running.

**Fix:** 
```bash
# Check agent status
sudo /opt/aws/amazon-cloudwatch-agent/bin/amazon-cloudwatch-agent-ctl -a status

# Restart if needed
sudo /opt/aws/amazon-cloudwatch-agent/bin/amazon-cloudwatch-agent-ctl -a stop
sudo /opt/aws/amazon-cloudwatch-agent/bin/amazon-cloudwatch-agent-ctl -a start
```

## Issue 3: "SNS Error: Access Denied"

**Cause:** IAM user doesn't have SNS permissions.

**Fix:** Add `AmazonSNSFullAccess` policy to IAM user.

## Issue 4: "Model not found"

**Cause:** Training script wasn't run first.

**Fix:**
```bash
python main.py
```

## Issue 5: Email not received

**Checks:**
1. Check spam folder
2. Verify subscription is confirmed:
   ```bash
   aws sns list-subscriptions
   ```
3. Look for "PendingConfirmation" status

---

# 18. Project Architecture

## System Flow Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                    CONTINUOUS MONITORING LOOP                    │
│                     (runs every 30 seconds)                      │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│ STEP 1: Fetch Metrics from CloudWatch                           │
│         - CPU: AWS/EC2 namespace                                │
│         - Disk: CWAgent namespace                               │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│ STEP 2: Check for Spikes                                        │
│         - CPU spike: +25% jump                                  │
│         - Disk spike: +15% jump                                 │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│ STEP 3: ML Prediction                                           │
│         - Predict CPU 1 hour ahead                              │
│         - Predict Disk trend                                    │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│ STEP 4: Check Thresholds                                        │
│         - CPU Critical: ≥80%                                    │
│         - Disk Critical: ≥85%                                   │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│ STEP 5: Send Alerts (if triggered)                              │
│         - Console output                                        │
│         - Log file                                              │
│         - SNS Email                                             │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
                    ⏰ Wait 30 seconds
                              │
                              └──────────────────────────┐
                                                         │
                                              🔄 REPEAT ─┘
```

## File Structure

```
~/ml-monitoring/
│
├── main.py                    # Training script (run once)
├── monitor_continuous.py      # Main monitoring script
├── config.py                  # All configuration settings
├── requirements.txt           # Python dependencies
│
├── src/
│   ├── __init__.py
│   ├── data_generator.py      # Generates synthetic training data
│   ├── feature_engineering.py # Creates ML features
│   ├── model_training.py      # Trains Random Forest model
│   ├── cost_calculator.py     # AWS cost prediction
│   └── alert_system.py        # SNS alert integration
│
├── data/
│   └── training_data.csv      # Generated training data
│
├── models/
│   └── cpu_predictor.pkl      # Trained ML model
│
├── logs/
│   ├── alerts.log             # Alert history
│   └── monitor.log            # Monitoring logs
│
└── venv/                      # Python virtual environment
```

---

# 19. All Code Files Reference

## Quick Commands

```bash
# Activate environment
cd ~/ml-monitoring && source venv/bin/activate

# Train model
python main.py

# Start monitoring (foreground)
python monitor_continuous.py

# Start monitoring (background)
nohup python monitor_continuous.py > logs/monitor.log 2>&1 &

# Stop monitoring
pkill -f monitor_continuous

# View logs
tail -f logs/monitor.log

# Check alerts
cat logs/alerts.log

# Test CPU load
stress --cpu 2 --timeout 60

# Check CloudWatch Agent
sudo /opt/aws/amazon-cloudwatch-agent/bin/amazon-cloudwatch-agent-ctl -a status
```

## Alert Types

| Alert Type | Trigger | Email Subject |
|------------|---------|---------------|
| CPU_SPIKE | CPU jumps +25% | ⚡ CPU_SPIKE: Jumped to 92% |
| DISK_SPIKE | Disk jumps +15% | ⚡ DISK_SPIKE: Jumped to 88% |
| CPU_CRITICAL | CPU ≥ 80% | 🚨 CPU_CRITICAL: CPU at 85% |
| DISK_CRITICAL | Disk ≥ 85% | 🚨 DISK_CRITICAL: Disk at 90% |
| CPU_PREDICTION | Predicted CPU ≥ 80% | 🔮 CPU_PREDICTION: Will reach 85% |
| DISK_PREDICTION | Predicted Disk ≥ 85% | 🔮 DISK_PREDICTION: Will reach 88% |

---

# ✅ Congratulations!

You have successfully completed the ML Monitoring project setup!

## What You've Built:
- ✅ EC2 instance monitoring
- ✅ CloudWatch integration (CPU + Disk)
- ✅ ML-based prediction (Random Forest)
- ✅ Spike detection
- ✅ Threshold alerting
- ✅ SNS email notifications
- ✅ Continuous monitoring loop

## ML Concepts Applied:
- ✅ Supervised Learning (Regression)
- ✅ Feature Engineering (38+ features)
- ✅ Model Training (Train/Test Split)
- ✅ Model Evaluation (RMSE, R²)
- ✅ Real-time Prediction

---

**Document Created:** November 2025
**Last Updated:** November 2025
**Author:** ML Monitoring Project


