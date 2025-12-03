"""
Data Generator - Creates synthetic training data
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
