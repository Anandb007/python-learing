"""
Main Application - Train ML Model
"""

import os
import sys
from datetime import datetime
import pandas as pd

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from data_generator import generate_metrics, create_target, save_data
from feature_engineering import FeatureEngineer
from model_training import CPUPredictor
from config import ML_CONFIG

def main():
    print("\n" + "=" * 70)
    print("🐧 ML MONITORING - MODEL TRAINING")
    print("=" * 70)
    print(f"   Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    print("\n📊 Generating training data...")
    df = generate_metrics(days=14, instances=3)
    df = create_target(df, hours_ahead=ML_CONFIG['prediction_hours_ahead'])
    save_data(df)
    
    fe = FeatureEngineer()
    df = fe.fit_transform(df)
    
    predictor = CPUPredictor()
    predictor.train(df, target='cpu_future', features=fe.get_features())
    predictor.save()
    
    print("\n" + "=" * 70)
    print("✅ TRAINING COMPLETE!")
    print("=" * 70)
    print(f"""
   📁 Files created:
      • data/training_data.csv
      • models/cpu_predictor.pkl
   
   Next step: Run 'python monitor_autoscaling.py'
    """)


if __name__ == "__main__":
    main()
