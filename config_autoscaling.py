"""
Configuration for Auto Scaling ML Monitoring
Enhanced Predictive Alerting for All Resources
"""

# UPDATE THIS WITH YOUR ASG NAME!
AUTOSCALING_CONFIG = {
    'asg_name': 'ML-Auto-scaling-Group',
    'region': 'us-east-1'
}

# Current thresholds (when resource is ALREADY high)
THRESHOLDS = {
    # CPU thresholds
    'cpu_warning': 70,
    'cpu_critical': 80,
    
    # Disk thresholds
    'disk_warning': 75,
    'disk_critical': 85,
    
    # Memory thresholds
    'memory_warning': 80,
    'memory_critical': 95,
    
    # Network thresholds (bytes per second)
    'network_in_warning': 50000000,      # 50 MB/s
    'network_in_critical': 100000000,    # 100 MB/s
    'network_out_warning': 50000000,
    'network_out_critical': 100000000,
    
    # ASG aggregate
    'asg_avg_cpu_warning': 60,
    'asg_avg_cpu_critical': 75
}

# PREDICTION THRESHOLDS - Send alert BEFORE reaching these levels
PREDICTION_THRESHOLDS = {
    # Alert if CPU predicted to reach these (lower = earlier warning)
    'cpu_prediction_warning': 50,        # Alert if CPU will reach 50%
    'cpu_prediction_critical': 65,       # Alert if CPU will reach 65%

    # Disk predictions
    'disk_prediction_warning': 60,
    'disk_prediction_critical': 75,

    # Memory predictions
    'memory_prediction_warning': 65,
    'memory_prediction_critical': 80,

    # Alert if ANY resource increases by this much
    'significant_increase': 15,          # Alert if resource will increase by 15%+
}
# Spike detection thresholds (sudden jumps)
SPIKE_CONFIG = {
    'cpu_spike_threshold': 25,
    'disk_spike_threshold': 15,
    'memory_spike_threshold': 20,
    'network_spike_threshold': 50,       # percentage
}

# Prediction settings
PREDICTION_CONFIG = {
    'enabled': True,
    'hours_ahead': 1,
    'send_prediction_alerts': True,
    'alert_on_any_increase': True,       # NEW: Alert on any predicted increase
    'min_increase_for_alert': 10,        # NEW: Minimum increase to trigger alert
    'trend_detection_enabled': True,
    'trend_alert_threshold': 10,         # Lower threshold
}

# Cause analysis settings
CAUSE_ANALYSIS_CONFIG = {
    'enabled': True,
    'analyze_patterns': True,
    'check_time_correlation': True,
    'common_causes': {
        'high_cpu': [
            'High application load/traffic',
            'Background processes or cron jobs',
            'Memory swapping due to low memory',
            'Inefficient code or queries',
            'Software updates running'
        ],
        'high_disk': [
            'Log files growing rapidly',
            'Database growth',
            'Temp files accumulation',
            'Large file uploads/downloads',
            'Backup processes running'
        ],
        'high_network': [
            'DDoS attack or traffic spike',
            'Large data transfer/backup',
            'API rate limiting issues',
            'High user traffic'
        ],
        'high_memory': [
            'Memory leak in application',
            'Cache not being cleared',
            'Too many connections/sessions',
            'Large dataset processing'
        ]
    }
}

# ML settings
ML_CONFIG = {
    'prediction_hours_ahead': 1,
    'training_window_days': 30,
    'model_type': 'random_forest'
}

# UPDATE THIS WITH YOUR SNS ARN!
SNS_CONFIG = {
    'enabled': True,
    'topic_arn': 'arn:aws:sns:us-east-1:486408064722:ml-auto-scaling',
    'region': 'us-east-1'
}

ALERT_CONFIG = {
    'console_alerts': True,
    'log_alerts': True,
    'sns_alerts': True,
    'log_file': 'logs/asg_alerts.log',
    'aggregate_alerts': True,
    'include_cause_analysis': True,
    'send_prediction_emails': True,      # Send emails for predictions
    'prediction_email_cooldown': 1800,   # Don't send same prediction alert within 30 minutes
}

AWS_REGION = 'us-east-1'

MONITORING_CONFIG = {
    'check_interval_seconds': 30,
    'instance_discovery_interval_seconds': 300,
    'collect_network_metrics': True,
    'collect_memory_metrics': True
}
