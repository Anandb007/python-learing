"""
ML Model Training
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
