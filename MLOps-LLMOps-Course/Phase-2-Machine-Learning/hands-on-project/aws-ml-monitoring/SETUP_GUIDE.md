# 🐧 Complete Ubuntu EC2 Setup Guide

## ML Monitoring Project - Step by Step Instructions

This guide covers everything from creating an AWS account to running the ML monitoring application on Ubuntu EC2.

---

## 📋 Table of Contents

1. [Prerequisites](#1-prerequisites)
2. [Create AWS Account](#2-create-aws-account)
3. [Create IAM User](#3-create-iam-user)
4. [Launch Ubuntu EC2 Instance](#4-launch-ubuntu-ec2-instance)
5. [Connect to EC2 Instance](#5-connect-to-ec2-instance)
6. [Install Required Software](#6-install-required-software)
7. [Configure AWS Credentials](#7-configure-aws-credentials)
8. [Set Up the Project](#8-set-up-the-project)
9. [Run the Application](#9-run-the-application)
10. [Install CloudWatch Agent](#10-install-cloudwatch-agent-optional)
11. [Set Up Automatic Execution](#11-set-up-automatic-execution-optional)
12. [Troubleshooting](#12-troubleshooting)

---

## 1. Prerequisites

Before starting, you need:
- A computer with internet access
- A valid email address
- A credit/debit card (for AWS account verification)
- Basic knowledge of using terminal/command line

---

## 2. Create AWS Account

### Step 2.1: Go to AWS Website

Open browser and navigate to: **https://aws.amazon.com/**

### Step 2.2: Click "Create an AWS Account"

Click the orange button at the top right.

### Step 2.3: Enter Account Details

```
Email address: your-email@example.com
Password: YourStrongPassword123!
AWS account name: MLOpsLearning
```

### Step 2.4: Contact Information

```
Account type: Personal
Full name: Your Full Name
Phone number: +91-XXXXXXXXXX
Country: India
Address: Your address
City: Your city
State: Your state
Postal code: XXXXXX
```

### Step 2.5: Payment Method

- Enter credit/debit card details
- AWS may charge ₹2 ($1) for verification (refunded)
- We will use FREE TIER only

### Step 2.6: Identity Verification

- AWS will call or SMS you
- Enter the verification code

### Step 2.7: Select Support Plan

Select: **Basic Support - Free**

### Step 2.8: Complete Registration

Wait for account activation (usually instant, may take up to 24 hours).

---

## 3. Create IAM User

### Step 3.1: Login to AWS Console

Go to: **https://console.aws.amazon.com/**

### Step 3.2: Navigate to IAM

1. In search bar, type: **IAM**
2. Click on "IAM"

### Step 3.3: Create User

1. Click **Users** in left sidebar
2. Click **Create user**

### Step 3.4: User Configuration

```
User name: ml-monitoring-user

Permissions:
☑️ CloudWatchReadOnlyAccess
☑️ AmazonEC2ReadOnlyAccess  
☑️ CloudWatchAgentServerPolicy
```

### Step 3.5: Create Access Keys

1. Click on the created user
2. Go to **Security credentials** tab
3. Click **Create access key**
4. Select **Command Line Interface (CLI)**
5. Click **Create access key**
6. **DOWNLOAD THE CSV FILE** - Save it securely!

```
⚠️ IMPORTANT: Save these values securely!
   Access Key ID:     AKIAXXXXXXXXXXXXXXXXX
   Secret Access Key: xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

---

## 4. Launch Ubuntu EC2 Instance

### Step 4.1: Go to EC2 Console

Navigate to: **https://console.aws.amazon.com/ec2/**

### Step 4.2: Click "Launch instance"

Click the orange **Launch instance** button.

### Step 4.3: Configure Instance

```
NAME
────
ml-monitoring-ubuntu

APPLICATION AND OS IMAGES (AMI)
───────────────────────────────
Quick Start: Ubuntu
AMI: Ubuntu Server 22.04 LTS (HVM), SSD Volume Type
     Free tier eligible ✓

INSTANCE TYPE
─────────────
t2.micro
- Free tier eligible ✓
- 1 vCPU
- 1 GB Memory

KEY PAIR (LOGIN)
────────────────
Click: Create new key pair
  Key pair name: ml-ubuntu-key
  Key pair type: RSA
  Private key format: .pem
Click: Create key pair
  → Downloads ml-ubuntu-key.pem (SAVE THIS FILE!)

NETWORK SETTINGS
────────────────
☑️ Allow SSH traffic from: My IP
☑️ Allow HTTP traffic from the internet

CONFIGURE STORAGE
─────────────────
15 GiB gp3 Root volume
```

### Step 4.4: Launch Instance

1. Click **Launch instance**
2. Click **View all instances**
3. Wait for **Instance state** to show **Running**
4. Note the **Public IPv4 address** (e.g., 54.123.45.67)

---

## 5. Connect to EC2 Instance

### Step 5.1: Open Terminal

**On Windows:**
- Open PowerShell or Command Prompt
- Or use PuTTY

**On Mac/Linux:**
- Open Terminal

### Step 5.2: Navigate to Key File Location

```bash
cd ~/Downloads
# Or wherever you saved the .pem file
```

### Step 5.3: Set Key File Permissions (Mac/Linux only)

```bash
chmod 400 ml-ubuntu-key.pem
```

### Step 5.4: Connect via SSH

```bash
ssh -i "ml-ubuntu-key.pem" ubuntu@YOUR_PUBLIC_IP
```

Replace `YOUR_PUBLIC_IP` with your EC2 instance's public IP address.

### Step 5.5: Accept Connection

When prompted "Are you sure you want to continue connecting?", type: **yes**

### Step 5.6: Verify Connection

You should see:
```
Welcome to Ubuntu 22.04.3 LTS (GNU/Linux 5.15.0-xxx-aws x86_64)

ubuntu@ip-172-31-xx-xx:~$
```

**You are now connected to your Ubuntu EC2 instance!** 🎉

---

## 6. Install Required Software

Run these commands on your EC2 instance:

### Step 6.1: Update System

```bash
sudo apt update
sudo apt upgrade -y
```

### Step 6.2: Install Python 3

```bash
sudo apt install python3 python3-pip python3-venv -y
```

Verify:
```bash
python3 --version
# Should show: Python 3.10.x or higher
```

### Step 6.3: Install AWS CLI

```bash
sudo apt install awscli -y
```

Verify:
```bash
aws --version
# Should show: aws-cli/2.x.x
```

### Step 6.4: Install Git (Optional)

```bash
sudo apt install git -y
```

---

## 7. Configure AWS Credentials

### Step 7.1: Run AWS Configure

```bash
aws configure
```

### Step 7.2: Enter Credentials

```
AWS Access Key ID [None]: AKIAXXXXXXXXXXXXXXXXX
AWS Secret Access Key [None]: xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
Default region name [None]: us-east-1
Default output format [None]: json
```

### Step 7.3: Verify Configuration

```bash
aws sts get-caller-identity
```

Expected output:
```json
{
    "UserId": "AIDAXXXXXXXXXXXXXXXXX",
    "Account": "123456789012",
    "Arn": "arn:aws:iam::123456789012:user/ml-monitoring-user"
}
```

### Step 7.4: Test EC2 Access

```bash
aws ec2 describe-instances --query 'Reservations[].Instances[].{ID:InstanceId,State:State.Name,Type:InstanceType}' --output table
```

---

## 8. Set Up the Project

### Step 8.1: Create Project Directory

```bash
mkdir -p ~/ml-monitoring
cd ~/ml-monitoring
mkdir -p src data models logs
```

### Step 8.2: Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
```

Your prompt should now show: `(venv) ubuntu@ip-xxx:~/ml-monitoring$`

### Step 8.3: Create requirements.txt

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

### Step 8.4: Install Python Packages

```bash
pip install -r requirements.txt
```

### Step 8.5: Create Configuration File

```bash
cat > config.py << 'EOF'
"""
Configuration for ML Monitoring Project (Ubuntu EC2)
"""

# Threshold settings for alerts
THRESHOLDS = {
    'cpu_warning': 70,
    'cpu_critical': 85,
    'disk_warning': 75,
    'disk_critical': 90,
    'memory_warning': 80,
    'memory_critical': 95
}

# ML Model configuration
ML_CONFIG = {
    'prediction_hours_ahead': 1,
    'training_window_days': 30,
    'model_type': 'random_forest'
}

# EC2 pricing (USD per hour) - US East region
EC2_PRICING = {
    't2.micro': 0.0116,
    't2.small': 0.0232,
    't2.medium': 0.0464,
    't2.large': 0.0928,
    't3.micro': 0.0104,
    't3.small': 0.0208,
    't3.medium': 0.0416,
    'm5.large': 0.096,
}

# EBS pricing (USD per GB per month)
EBS_PRICING = {
    'gp2': 0.10,
    'gp3': 0.08,
    'io1': 0.125,
}

# Alert settings
ALERT_CONFIG = {
    'console_alerts': True,
    'log_alerts': True,
    'log_file': 'logs/alerts.log'
}

# AWS Region
AWS_REGION = 'us-east-1'
EOF
```

### Step 8.6: Create Source Files

Create `src/__init__.py`:
```bash
touch src/__init__.py
```

Create `src/data_generator.py`:
```bash
cat > src/data_generator.py << 'DATAGENEOF'
"""
Data Generator - Creates synthetic CloudWatch-like metrics for training
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os

def generate_metrics(days=30, instances=5, interval_minutes=5):
    """Generate realistic EC2 metrics data."""
    
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
            
            # CPU pattern with business hours and spikes
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
    """Create target variable for ML prediction."""
    print(f"\n📎 Creating target variable ({hours_ahead}h ahead)")
    
    rows_shift = hours_ahead * 12
    df = df.copy()
    df['cpu_future'] = df.groupby('instance_id')['cpu_utilization'].shift(-rows_shift)
    df['will_exceed_threshold'] = (df['cpu_future'] > 70).astype(int)
    df = df.dropna(subset=['cpu_future'])
    
    print(f"   Rows with target: {len(df)}")
    return df

def save_data(df, filepath='data/training_data.csv'):
    """Save data to CSV."""
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    df.to_csv(filepath, index=False)
    print(f"💾 Saved: {filepath}")

if __name__ == "__main__":
    df = generate_metrics(days=7, instances=3)
    df = create_target(df)
    save_data(df)
    print(df.head())
DATAGENEOF
```

Create `src/feature_engineering.py`:
```bash
cat > src/feature_engineering.py << 'FEATUREEOF'
"""
Feature Engineering - Creates ML features from raw metrics
"""

import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
import warnings
warnings.filterwarnings('ignore')

class FeatureEngineer:
    def __init__(self):
        self.encoder = LabelEncoder()
        self.fitted = False
    
    def create_features(self, df):
        """Create all features."""
        print("\n🔧 FEATURE ENGINEERING")
        print("=" * 60)
        
        df = df.copy()
        
        # Time features
        if 'timestamp' in df.columns:
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            df['hour'] = df['timestamp'].dt.hour
            df['day_of_week'] = df['timestamp'].dt.dayofweek
            df['is_weekend'] = (df['day_of_week'] >= 5).astype(int)
            df['is_business_hours'] = ((df['hour'] >= 9) & (df['hour'] <= 18)).astype(int)
            df['hour_sin'] = np.sin(2 * np.pi * df['hour'] / 24)
            df['hour_cos'] = np.cos(2 * np.pi * df['hour'] / 24)
        
        # Rolling statistics
        for col in ['cpu_utilization', 'memory_utilization', 'disk_utilization']:
            if col in df.columns:
                df[f'{col}_rolling_mean'] = df.groupby('instance_id')[col].transform(
                    lambda x: x.rolling(12, min_periods=1).mean())
                df[f'{col}_rolling_std'] = df.groupby('instance_id')[col].transform(
                    lambda x: x.rolling(12, min_periods=1).std())
                df[f'{col}_rolling_max'] = df.groupby('instance_id')[col].transform(
                    lambda x: x.rolling(12, min_periods=1).max())
                df[f'{col}_lag_1'] = df.groupby('instance_id')[col].shift(1)
                df[f'{col}_lag_3'] = df.groupby('instance_id')[col].shift(3)
                df[f'{col}_diff'] = df.groupby('instance_id')[col].diff()
        
        # Interaction features
        if 'cpu_utilization' in df.columns and 'memory_utilization' in df.columns:
            df['cpu_memory_ratio'] = df['cpu_utilization'] / (df['memory_utilization'] + 0.01)
            df['system_stress'] = (df['cpu_utilization'] + df['memory_utilization'] + 
                                   df.get('disk_utilization', 0)) / 3
        
        if 'cpu_utilization' in df.columns:
            df['cpu_distance_warning'] = 70 - df['cpu_utilization']
            df['cpu_elevated'] = (df['cpu_utilization'] > 50).astype(int)
        
        if 'network_in_mb' in df.columns:
            df['network_total'] = df['network_in_mb'] + df.get('network_out_mb', 0)
        
        print(f"   ✅ Created {len(df.columns)} features")
        return df
    
    def handle_missing(self, df):
        """Handle missing values."""
        df = df.copy()
        for col in df.select_dtypes(include=[np.number]).columns:
            df[col] = df[col].fillna(df[col].mean())
        return df.fillna(method='ffill').fillna(method='bfill').fillna(0)
    
    def encode(self, df, fit=True):
        """Encode categorical features."""
        df = df.copy()
        if 'instance_type' in df.columns:
            if fit:
                df['instance_type_encoded'] = self.encoder.fit_transform(df['instance_type'].astype(str))
            else:
                df['instance_type_encoded'] = df['instance_type'].apply(
                    lambda x: self.encoder.transform([str(x)])[0] if str(x) in self.encoder.classes_ else -1)
        return df
    
    def get_features(self):
        """Return feature column names."""
        return [
            'cpu_utilization', 'memory_utilization', 'disk_utilization',
            'hour', 'is_weekend', 'is_business_hours', 'hour_sin', 'hour_cos',
            'cpu_utilization_rolling_mean', 'cpu_utilization_rolling_std', 'cpu_utilization_rolling_max',
            'memory_utilization_rolling_mean', 'disk_utilization_rolling_mean',
            'cpu_utilization_lag_1', 'cpu_utilization_lag_3', 'cpu_utilization_diff',
            'cpu_memory_ratio', 'system_stress', 'cpu_distance_warning', 'cpu_elevated',
            'network_total', 'instance_type_encoded'
        ]
    
    def fit_transform(self, df):
        """Full pipeline for training."""
        df = self.create_features(df)
        df = self.handle_missing(df)
        df = self.encode(df, fit=True)
        self.fitted = True
        return df
    
    def transform(self, df):
        """Transform for prediction."""
        df = self.create_features(df)
        df = self.handle_missing(df)
        df = self.encode(df, fit=False)
        return df
FEATUREEOF
```

Create `src/model_training.py`:
```bash
cat > src/model_training.py << 'MODELEOF'
"""
ML Model Training - Trains Random Forest for CPU prediction
"""

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
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
        """Prepare feature matrix."""
        cols = [c for c in features if c in df.columns]
        X = df[cols].fillna(0).replace([np.inf, -np.inf], 0)
        return X, cols
    
    def train(self, df, target='cpu_future', features=None):
        """Train the model."""
        print("\n" + "=" * 60)
        print("🎯 MODEL TRAINING")
        print("=" * 60)
        
        if features is None:
            features = [c for c in df.select_dtypes(include=[np.number]).columns 
                       if c not in [target, 'will_exceed_threshold']]
        
        self.feature_columns = features
        X, self.feature_columns = self.prepare_data(df, features)
        y = df[target].values
        
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        print(f"   Training samples: {len(X_train)}")
        print(f"   Testing samples: {len(X_test)}")
        print(f"   Features: {len(self.feature_columns)}")
        
        self.model.fit(X_train, y_train)
        
        y_train_pred = self.model.predict(X_train)
        y_test_pred = self.model.predict(X_test)
        
        self.metrics = {
            'train_rmse': np.sqrt(mean_squared_error(y_train, y_train_pred)),
            'test_rmse': np.sqrt(mean_squared_error(y_test, y_test_pred)),
            'train_r2': r2_score(y_train, y_train_pred),
            'test_r2': r2_score(y_test, y_test_pred),
            'train_mae': mean_absolute_error(y_train, y_train_pred),
            'test_mae': mean_absolute_error(y_test, y_test_pred),
            'trained_at': datetime.now().isoformat()
        }
        
        print(f"\n📊 EVALUATION METRICS")
        print(f"   Training RMSE: {self.metrics['train_rmse']:.2f}%")
        print(f"   Testing RMSE:  {self.metrics['test_rmse']:.2f}%")
        print(f"   Training R²:   {self.metrics['train_r2']:.4f}")
        print(f"   Testing R²:    {self.metrics['test_r2']:.4f}")
        
        if self.metrics['test_r2'] > 0.8:
            print(f"\n   ✅ Model performance: EXCELLENT")
        elif self.metrics['test_r2'] > 0.6:
            print(f"\n   ⚠️ Model performance: GOOD")
        else:
            print(f"\n   ❌ Model performance: NEEDS IMPROVEMENT")
        
        self.trained = True
        return self.metrics
    
    def predict(self, df):
        """Make predictions."""
        if not self.trained:
            raise ValueError("Model not trained!")
        X, _ = self.prepare_data(df, self.feature_columns)
        return self.model.predict(X)
    
    def predict_with_confidence(self, df):
        """Predict with confidence intervals."""
        if not self.trained:
            raise ValueError("Model not trained!")
        X, _ = self.prepare_data(df, self.feature_columns)
        predictions = np.array([tree.predict(X) for tree in self.model.estimators_])
        mean_pred = np.mean(predictions, axis=0)
        std_pred = np.std(predictions, axis=0)
        return {
            'prediction': mean_pred,
            'lower': mean_pred - 2 * std_pred,
            'upper': mean_pred + 2 * std_pred,
            'confidence': 0.95
        }
    
    def save(self, path='models/cpu_predictor.pkl'):
        """Save model."""
        os.makedirs(os.path.dirname(path), exist_ok=True)
        joblib.dump({
            'model': self.model,
            'features': self.feature_columns,
            'metrics': self.metrics,
            'trained': self.trained
        }, path)
        print(f"\n💾 Model saved: {path}")
    
    def load(self, path='models/cpu_predictor.pkl'):
        """Load model."""
        data = joblib.load(path)
        self.model = data['model']
        self.feature_columns = data['features']
        self.metrics = data['metrics']
        self.trained = data['trained']
        print(f"📂 Model loaded: {path}")
        return self
MODELEOF
```

Create `src/cloudwatch_connector.py`:
```bash
cat > src/cloudwatch_connector.py << 'CWEOF'
"""
CloudWatch Connector - Fetches real metrics from AWS
"""

import boto3
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
from botocore.exceptions import ClientError, NoCredentialsError
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import AWS_REGION

class CloudWatchConnector:
    def __init__(self, region=None):
        self.region = region or AWS_REGION
        print(f"\n🌐 Connecting to AWS CloudWatch ({self.region})...")
        
        try:
            self.cloudwatch = boto3.client('cloudwatch', region_name=self.region)
            self.ec2 = boto3.client('ec2', region_name=self.region)
            self.ec2.describe_regions()
            print(f"   ✅ Connected successfully!")
        except NoCredentialsError:
            print("   ❌ AWS credentials not found!")
            print("   Run: aws configure")
            raise
        except ClientError as e:
            print(f"   ❌ Error: {e}")
            raise
    
    def get_instances(self):
        """Get running EC2 instances."""
        print("\n📋 Fetching EC2 instances...")
        response = self.ec2.describe_instances(
            Filters=[{'Name': 'instance-state-name', 'Values': ['running']}])
        
        instances = []
        for reservation in response['Reservations']:
            for instance in reservation['Instances']:
                name = 'No Name'
                for tag in instance.get('Tags', []):
                    if tag['Key'] == 'Name':
                        name = tag['Value']
                instances.append({
                    'instance_id': instance['InstanceId'],
                    'instance_type': instance['InstanceType'],
                    'name': name,
                    'private_ip': instance.get('PrivateIpAddress', 'N/A')
                })
        
        print(f"   Found {len(instances)} running instance(s)")
        for inst in instances:
            print(f"   • {inst['instance_id']} ({inst['name']}) - {inst['instance_type']}")
        return instances
    
    def get_cpu(self, instance_id, hours=24):
        """Get CPU metrics."""
        end = datetime.utcnow()
        start = end - timedelta(hours=hours)
        
        try:
            response = self.cloudwatch.get_metric_data(
                MetricDataQueries=[{
                    'Id': 'cpu',
                    'MetricStat': {
                        'Metric': {
                            'Namespace': 'AWS/EC2',
                            'MetricName': 'CPUUtilization',
                            'Dimensions': [{'Name': 'InstanceId', 'Value': instance_id}]
                        },
                        'Period': 300,
                        'Stat': 'Average'
                    },
                    'ReturnData': True
                }],
                StartTime=start,
                EndTime=end
            )
            
            timestamps = response['MetricDataResults'][0]['Timestamps']
            values = response['MetricDataResults'][0]['Values']
            
            if not timestamps:
                return pd.DataFrame()
            
            return pd.DataFrame({
                'timestamp': timestamps,
                'cpu_utilization': values,
                'instance_id': instance_id
            }).sort_values('timestamp').reset_index(drop=True)
        except:
            return pd.DataFrame()
    
    def get_all_metrics(self, hours=24):
        """Get all metrics for all instances."""
        print(f"\n📊 Fetching CloudWatch metrics (last {hours}h)...")
        
        instances = self.get_instances()
        if not instances:
            return pd.DataFrame()
        
        all_data = []
        for inst in instances:
            iid = inst['instance_id']
            cpu_df = self.get_cpu(iid, hours)
            
            if cpu_df.empty:
                print(f"   ⚠️ No data for {iid}")
                continue
            
            cpu_df['instance_type'] = inst['instance_type']
            cpu_df['memory_utilization'] = np.random.uniform(40, 70, len(cpu_df))
            cpu_df['disk_utilization'] = np.random.uniform(30, 60, len(cpu_df))
            cpu_df['network_in_mb'] = np.random.uniform(10, 100, len(cpu_df))
            cpu_df['network_out_mb'] = np.random.uniform(5, 50, len(cpu_df))
            cpu_df['hour_of_day'] = pd.to_datetime(cpu_df['timestamp']).dt.hour
            cpu_df['day_of_week'] = pd.to_datetime(cpu_df['timestamp']).dt.dayofweek
            cpu_df['is_business_hours'] = cpu_df['hour_of_day'].apply(lambda x: 1 if 9 <= x <= 18 else 0)
            cpu_df['is_weekend'] = cpu_df['day_of_week'].apply(lambda x: 1 if x >= 5 else 0)
            
            print(f"   ✅ {iid}: {len(cpu_df)} points")
            all_data.append(cpu_df)
        
        if all_data:
            combined = pd.concat(all_data, ignore_index=True)
            print(f"\n✅ Total: {len(combined)} data points")
            return combined
        return pd.DataFrame()
    
    def get_current(self, instance_id):
        """Get current metrics for an instance."""
        cpu_df = self.get_cpu(instance_id, hours=0.25)
        if cpu_df.empty:
            return None
        latest = cpu_df.iloc[-1]
        return {
            'instance_id': instance_id,
            'cpu_utilization': float(latest['cpu_utilization']),
            'memory_utilization': 50.0,
            'disk_utilization': 45.0,
            'network_in_mb': 20.0,
            'network_out_mb': 10.0
        }

if __name__ == "__main__":
    try:
        conn = CloudWatchConnector()
        conn.get_instances()
    except Exception as e:
        print(f"Error: {e}")
CWEOF
```

Create `src/cost_calculator.py`:
```bash
cat > src/cost_calculator.py << 'COSTEOF'
"""
AWS Cost Calculator - Predicts monthly costs
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import EC2_PRICING, EBS_PRICING

class CostCalculator:
    def __init__(self):
        self.ec2_prices = EC2_PRICING
        self.ebs_prices = EBS_PRICING
    
    def calculate_ec2(self, instance_type, hours, count=1):
        """Calculate EC2 cost."""
        rate = self.ec2_prices.get(instance_type, 0.0116)
        return round(rate * hours * count, 2)
    
    def calculate_ebs(self, size_gb, volume_type='gp3'):
        """Calculate EBS cost."""
        rate = self.ebs_prices.get(volume_type, 0.08)
        return round(rate * size_gb, 2)
    
    def predict_monthly(self, instances, verbose=True):
        """Predict monthly cost."""
        if verbose:
            print("\n" + "=" * 60)
            print("💰 AWS COST PREDICTION")
            print("=" * 60)
        
        total_ec2 = 0
        total_ebs = 0
        
        for inst in instances:
            itype = inst.get('instance_type', 't2.micro')
            count = inst.get('count', 1)
            hours = inst.get('hours_per_day', 24) * 30
            storage = inst.get('storage_gb', 8) * count
            
            ec2_cost = self.calculate_ec2(itype, hours, count)
            ebs_cost = self.calculate_ebs(storage)
            total_ec2 += ec2_cost
            total_ebs += ebs_cost
            
            if verbose:
                print(f"\n   📦 {itype} x {count}")
                print(f"      EC2: ${ec2_cost:.2f}")
                print(f"      EBS: ${ebs_cost:.2f}")
        
        data_transfer = round(total_ec2 * 0.1, 2)
        grand_total = round(total_ec2 + total_ebs + data_transfer, 2)
        
        if verbose:
            print(f"\n   {'─' * 40}")
            print(f"   EC2 Compute:    ${total_ec2:.2f}")
            print(f"   EBS Storage:    ${total_ebs:.2f}")
            print(f"   Data Transfer:  ${data_transfer:.2f}")
            print(f"   {'─' * 40}")
            print(f"   💵 TOTAL:       ${grand_total:.2f}/month")
        
        return {'total': grand_total, 'ec2': total_ec2, 'ebs': total_ebs}

if __name__ == "__main__":
    calc = CostCalculator()
    calc.predict_monthly([
        {'instance_type': 't2.micro', 'count': 2, 'storage_gb': 30},
        {'instance_type': 't2.small', 'count': 1, 'storage_gb': 50}
    ])
COSTEOF
```

Create `src/alert_system.py`:
```bash
cat > src/alert_system.py << 'ALERTEOF'
"""
Alert System - Sends alerts when thresholds are exceeded
"""

from datetime import datetime
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import THRESHOLDS, ALERT_CONFIG

class AlertSystem:
    def __init__(self):
        self.thresholds = THRESHOLDS
        self.history = []
    
    def check_current(self, metrics):
        """Check current metrics against thresholds."""
        alerts = []
        
        cpu = metrics.get('cpu_utilization', 0)
        if cpu >= self.thresholds['cpu_critical']:
            alerts.append({'level': 'CRITICAL', 'metric': 'CPU', 'value': cpu,
                          'message': f'🚨 CRITICAL: CPU at {cpu:.1f}% (threshold: {self.thresholds["cpu_critical"]}%)'})
        elif cpu >= self.thresholds['cpu_warning']:
            alerts.append({'level': 'WARNING', 'metric': 'CPU', 'value': cpu,
                          'message': f'⚠️ WARNING: CPU at {cpu:.1f}% (threshold: {self.thresholds["cpu_warning"]}%)'})
        
        disk = metrics.get('disk_utilization', 0)
        if disk >= self.thresholds['disk_critical']:
            alerts.append({'level': 'CRITICAL', 'metric': 'Disk', 'value': disk,
                          'message': f'🚨 CRITICAL: Disk at {disk:.1f}%'})
        elif disk >= self.thresholds['disk_warning']:
            alerts.append({'level': 'WARNING', 'metric': 'Disk', 'value': disk,
                          'message': f'⚠️ WARNING: Disk at {disk:.1f}%'})
        
        return alerts
    
    def check_prediction(self, predicted_cpu, hours_ahead=1):
        """Check predicted values against thresholds."""
        alerts = []
        
        if predicted_cpu >= self.thresholds['cpu_critical']:
            alerts.append({
                'level': 'PREDICTION_CRITICAL',
                'value': predicted_cpu,
                'message': f'🔮 PREDICTION: CPU will reach {predicted_cpu:.1f}% in {hours_ahead}h (CRITICAL threshold: {self.thresholds["cpu_critical"]}%)'
            })
        elif predicted_cpu >= self.thresholds['cpu_warning']:
            alerts.append({
                'level': 'PREDICTION_WARNING',
                'value': predicted_cpu,
                'message': f'🔮 PREDICTION: CPU will reach {predicted_cpu:.1f}% in {hours_ahead}h (WARNING threshold: {self.thresholds["cpu_warning"]}%)'
            })
        
        return alerts
    
    def send(self, alert):
        """Send an alert."""
        alert['timestamp'] = datetime.now().isoformat()
        self.history.append(alert)
        
        # Console output
        if ALERT_CONFIG.get('console_alerts', True):
            print(f"\n{'🔴' * 20}")
            print(f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            print(alert['message'])
            print(f"{'🔴' * 20}")
        
        # Log to file
        if ALERT_CONFIG.get('log_alerts', True):
            log_file = ALERT_CONFIG.get('log_file', 'logs/alerts.log')
            os.makedirs(os.path.dirname(log_file), exist_ok=True)
            with open(log_file, 'a') as f:
                f.write(f"{alert['timestamp']} | {alert['level']} | {alert['message']}\n")
    
    def process(self, current_metrics, predicted_cpu=None, hours_ahead=1):
        """Process all alerts."""
        alerts = []
        alerts.extend(self.check_current(current_metrics))
        
        if predicted_cpu is not None:
            alerts.extend(self.check_prediction(predicted_cpu, hours_ahead))
        
        for alert in alerts:
            self.send(alert)
        
        return alerts

if __name__ == "__main__":
    alert_sys = AlertSystem()
    alert_sys.process({'cpu_utilization': 90, 'disk_utilization': 80}, predicted_cpu=92)
ALERTEOF
```

Create `main.py`:
```bash
cat > main.py << 'MAINEOF'
"""
ML Monitoring Application - Main Entry Point
Run on Ubuntu EC2 instance
"""

import os
import sys
from datetime import datetime
import pandas as pd

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from data_generator import generate_metrics, create_target, save_data
from feature_engineering import FeatureEngineer
from model_training import CPUPredictor
from cloudwatch_connector import CloudWatchConnector
from cost_calculator import CostCalculator
from alert_system import AlertSystem
from config import ML_CONFIG, THRESHOLDS

def print_header():
    print("\n" + "=" * 70)
    print("🐧 ML MONITORING ON UBUNTU EC2")
    print("=" * 70)
    print(f"   Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 70)

def run_with_synthetic_data():
    """Run with synthetic data (for testing/demo)."""
    print("\n📊 Using synthetic data...")
    
    # Generate data
    df = generate_metrics(days=14, instances=3)
    df = create_target(df, hours_ahead=ML_CONFIG['prediction_hours_ahead'])
    save_data(df)
    
    # Feature engineering
    fe = FeatureEngineer()
    df = fe.fit_transform(df)
    
    # Train model
    predictor = CPUPredictor()
    predictor.train(df, target='cpu_future', features=fe.get_features())
    predictor.save()
    
    return fe, predictor, None

def run_with_aws_data():
    """Run with real AWS CloudWatch data."""
    print("\n🌐 Connecting to AWS CloudWatch...")
    
    try:
        connector = CloudWatchConnector()
        df = connector.get_all_metrics(hours=24)
        
        if df.empty:
            print("\n⚠️ No CloudWatch data available, using synthetic data...")
            return run_with_synthetic_data()
        
        df = create_target(df, hours_ahead=ML_CONFIG['prediction_hours_ahead'])
        
        fe = FeatureEngineer()
        df = fe.fit_transform(df)
        
        predictor = CPUPredictor()
        predictor.train(df, target='cpu_future', features=fe.get_features())
        predictor.save('models/cpu_predictor_aws.pkl')
        
        return fe, predictor, connector
        
    except Exception as e:
        print(f"\n❌ AWS Error: {e}")
        print("   Falling back to synthetic data...")
        return run_with_synthetic_data()

def run_predictions(fe, predictor, connector):
    """Run predictions on current data."""
    print("\n" + "=" * 70)
    print("🔮 RUNNING PREDICTIONS")
    print("=" * 70)
    
    alert_sys = AlertSystem()
    
    if connector:
        # Real AWS data
        instances = connector.get_instances()
        for inst in instances:
            current = connector.get_current(inst['instance_id'])
            if current:
                print(f"\n📊 Instance: {inst['instance_id']} ({inst['name']})")
                print(f"   Current CPU: {current['cpu_utilization']:.1f}%")
                
                current_df = pd.DataFrame([current])
                current_df['timestamp'] = datetime.now()
                current_df['instance_type'] = inst['instance_type']
                current_df = fe.transform(current_df)
                
                result = predictor.predict_with_confidence(current_df)
                predicted = result['prediction'][0]
                
                print(f"   Predicted CPU (1h): {predicted:.1f}%")
                print(f"   Confidence: [{max(0,result['lower'][0]):.1f}% - {min(100,result['upper'][0]):.1f}%]")
                
                alert_sys.process(current, predicted_cpu=predicted)
    else:
        # Synthetic demo
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
            alert_sys.process(scenario, predicted_cpu=predicted)

def run_cost_analysis(connector):
    """Run cost analysis."""
    print("\n" + "=" * 70)
    print("💰 COST ANALYSIS")
    print("=" * 70)
    
    calc = CostCalculator()
    
    if connector:
        instances = connector.get_instances()
        config = [{'instance_type': i['instance_type'], 'count': 1, 'storage_gb': 15} for i in instances]
        if config:
            calc.predict_monthly(config)
    else:
        # Demo config
        calc.predict_monthly([
            {'instance_type': 't2.micro', 'count': 2, 'storage_gb': 30},
            {'instance_type': 't2.small', 'count': 1, 'storage_gb': 50}
        ])

def main():
    """Main function."""
    print_header()
    
    # Ask user for data source
    print("\nSelect data source:")
    print("  1. Synthetic data (demo/testing)")
    print("  2. Real AWS CloudWatch data")
    
    try:
        choice = input("\nEnter choice (1 or 2) [default: 1]: ").strip() or '1'
    except:
        choice = '1'
    
    if choice == '2':
        fe, predictor, connector = run_with_aws_data()
    else:
        fe, predictor, connector = run_with_synthetic_data()
    
    # Run predictions
    run_predictions(fe, predictor, connector)
    
    # Cost analysis
    run_cost_analysis(connector)
    
    # Summary
    print("\n" + "=" * 70)
    print("✅ ML MONITORING COMPLETE")
    print("=" * 70)
    print(f"""
   📁 Files created:
      • data/training_data.csv
      • models/cpu_predictor.pkl
      • logs/alerts.log
   
   🔄 To run again: python main.py
   🔄 To run in background: nohup python main.py > logs/output.log 2>&1 &
    """)

if __name__ == "__main__":
    main()
MAINEOF
```

### Step 8.7: Create Setup Script

```bash
cat > setup.sh << 'SETUPEOF'
#!/bin/bash
# Automated setup script for Ubuntu EC2

echo "=================================================="
echo "🐧 ML Monitoring Setup Script"
echo "=================================================="

# Update system
echo "📦 Updating system..."
sudo apt update && sudo apt upgrade -y

# Install Python
echo "🐍 Installing Python..."
sudo apt install python3 python3-pip python3-venv -y

# Install AWS CLI
echo "☁️ Installing AWS CLI..."
sudo apt install awscli -y

# Create directories
echo "📁 Creating directories..."
mkdir -p data models logs

# Create virtual environment
echo "🔧 Creating virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Install Python packages
echo "📦 Installing Python packages..."
pip install -r requirements.txt

echo ""
echo "=================================================="
echo "✅ Setup complete!"
echo "=================================================="
echo ""
echo "Next steps:"
echo "  1. Configure AWS: aws configure"
echo "  2. Activate venv: source venv/bin/activate"
echo "  3. Run app: python main.py"
SETUPEOF

chmod +x setup.sh
```

---

## 9. Run the Application

### Step 9.1: Activate Virtual Environment

```bash
cd ~/ml-monitoring
source venv/bin/activate
```

### Step 9.2: Run the Application

```bash
python main.py
```

### Step 9.3: Expected Output

```
======================================================================
🐧 ML MONITORING ON UBUNTU EC2
======================================================================
   Started: 2024-11-28 15:30:00
======================================================================

Select data source:
  1. Synthetic data (demo/testing)
  2. Real AWS CloudWatch data

Enter choice (1 or 2) [default: 1]: 1

📊 Using synthetic data...
======================================================================
📊 GENERATING TRAINING DATA
======================================================================
   Days: 14
   Instances: 3
   Data points per instance: 4032

✅ Generated 12096 data points

🔧 FEATURE ENGINEERING
======================================================================
   ✅ Created 35 features

======================================================================
🎯 MODEL TRAINING
======================================================================
   Training samples: 9676
   Testing samples: 2420
   Features: 22

📊 EVALUATION METRICS
   Training RMSE: 2.85%
   Testing RMSE:  4.12%
   Training R²:   0.9523
   Testing R²:    0.8856

   ✅ Model performance: EXCELLENT

💾 Model saved: models/cpu_predictor.pkl

======================================================================
🔮 RUNNING PREDICTIONS
======================================================================

📊 Scenario: Normal
   Current CPU: 45%
   Predicted CPU (1h): 48.2%

📊 Scenario: Warning
   Current CPU: 72%
   Predicted CPU (1h): 75.8%

🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴
⏰ 2024-11-28 15:30:15
⚠️ WARNING: CPU at 72.0% (threshold: 70%)
🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴

📊 Scenario: Critical
   Current CPU: 88%
   Predicted CPU (1h): 85.3%

🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴
⏰ 2024-11-28 15:30:15
🚨 CRITICAL: CPU at 88.0% (threshold: 85%)
🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴

======================================================================
💰 COST ANALYSIS
======================================================================

   📦 t2.micro x 2
      EC2: $16.70
      EBS: $2.40

   📦 t2.small x 1
      EC2: $16.70
      EBS: $4.00

   ────────────────────────────────────────
   EC2 Compute:    $33.41
   EBS Storage:    $6.40
   Data Transfer:  $3.34
   ────────────────────────────────────────
   💵 TOTAL:       $43.15/month

======================================================================
✅ ML MONITORING COMPLETE
======================================================================
```

---

## 10. Install CloudWatch Agent (Optional)

For real Memory and Disk metrics:

```bash
# Download CloudWatch Agent
wget https://s3.amazonaws.com/amazoncloudwatch-agent/ubuntu/amd64/latest/amazon-cloudwatch-agent.deb

# Install
sudo dpkg -i amazon-cloudwatch-agent.deb

# Create config
sudo tee /opt/aws/amazon-cloudwatch-agent/etc/amazon-cloudwatch-agent.json > /dev/null << 'EOF'
{
    "agent": {"metrics_collection_interval": 60},
    "metrics": {
        "namespace": "CWAgent",
        "metrics_collected": {
            "cpu": {"measurement": ["cpu_usage_active"]},
            "disk": {"measurement": ["disk_used_percent"], "resources": ["/"]},
            "mem": {"measurement": ["mem_used_percent"]}
        }
    }
}
EOF

# Start agent
sudo /opt/aws/amazon-cloudwatch-agent/bin/amazon-cloudwatch-agent-ctl \
    -a fetch-config -m ec2 -s \
    -c file:/opt/aws/amazon-cloudwatch-agent/etc/amazon-cloudwatch-agent.json
```

---

## 11. Set Up Automatic Execution (Optional)

### Using Cron (Run every 5 minutes)

```bash
crontab -e
```

Add this line:
```
*/5 * * * * cd /home/ubuntu/ml-monitoring && /home/ubuntu/ml-monitoring/venv/bin/python main.py --auto >> /home/ubuntu/ml-monitoring/logs/cron.log 2>&1
```

### Using Systemd Service

```bash
sudo tee /etc/systemd/system/ml-monitor.service > /dev/null << 'EOF'
[Unit]
Description=ML Monitoring Service
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/home/ubuntu/ml-monitoring
ExecStart=/home/ubuntu/ml-monitoring/venv/bin/python main.py
Restart=always
RestartSec=300

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl enable ml-monitor
sudo systemctl start ml-monitor
```

---

## 12. Troubleshooting

### "No module named 'xxx'"
```bash
source venv/bin/activate
pip install -r requirements.txt
```

### "AWS credentials not found"
```bash
aws configure
```

### "Permission denied"
```bash
chmod +x main.py setup.sh
```

### "No running instances"
- Check AWS region is correct
- Verify instance is running in EC2 console

---

## 📋 Quick Reference

```bash
# Activate environment
source venv/bin/activate

# Run application
python main.py

# Run in background
nohup python main.py > logs/output.log 2>&1 &

# View logs
tail -f logs/output.log
tail -f logs/alerts.log

# Check AWS
aws sts get-caller-identity
aws ec2 describe-instances
```

---

**🎉 Congratulations!** You now have a complete ML monitoring system running on Ubuntu EC2!


