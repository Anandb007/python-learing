"""
Configuration for ML Monitoring
"""

THRESHOLDS = {
    'cpu_warning': 70,
    'cpu_critical': 80,
    'disk_warning': 75,
    'disk_critical': 85,
    'memory_warning': 80,
    'memory_critical': 95
}

SPIKE_CONFIG = {
    'cpu_spike_threshold': 25,
    'disk_spike_threshold': 15
}

ML_CONFIG = {
    'prediction_hours_ahead': 1,
    'training_window_days': 30,
    'model_type': 'random_forest'
}

EC2_PRICING = {
    't2.micro': 0.0116,
    't2.small': 0.0232,
    't2.medium': 0.0464,
}

EBS_PRICING = {
    'gp2': 0.10,
    'gp3': 0.08,
}

SNS_CONFIG = {
    'enabled': True,
    'topic_arn': 'arn:aws:sns:us-east-1:486408064722:ml-auto-scaling',
    'region': 'us-east-1'
}

ALERT_CONFIG = {
    'console_alerts': True,
    'log_alerts': True,
    'sns_alerts': True,
    'log_file': 'logs/alerts.log'
}

AWS_REGION = 'us-east-1'
