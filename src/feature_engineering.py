"""
Feature Engineering - Creates ML features
"""

import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings('ignore')

class FeatureEngineer:
    def __init__(self):
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
