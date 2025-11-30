# 🔴 AWS ML Monitoring Project

## CPU + Disk Monitoring with ML Prediction & SNS Alerts

---

## 📋 Overview

This project implements a production-ready ML-powered monitoring system that:

| Feature | Description |
|---------|-------------|
| **CPU Monitoring** | Real-time CPU metrics from AWS CloudWatch |
| **Disk Monitoring** | Disk usage via CloudWatch Agent |
| **ML Prediction** | Predicts CPU usage 1 hour ahead |
| **Spike Detection** | Detects sudden CPU (+25%) / Disk (+15%) spikes |
| **Threshold Alerts** | CPU ≥80%, Disk ≥85% |
| **SNS Notifications** | Email alerts via AWS SNS |
| **Continuous Monitoring** | Every 30 seconds |

---

## 🚀 Quick Start

```bash
# 1. Activate virtual environment
cd ~/ml-monitoring
source venv/bin/activate

# 2. Train ML model (run once)
python main.py

# 3. Start monitoring
python monitor_continuous.py

# 4. Run in background
nohup python monitor_continuous.py > logs/monitor.log 2>&1 &
```

---

## 📁 Project Structure

```
ml-monitoring/
├── main.py                    # Train ML model
├── monitor_continuous.py      # Main monitoring script
├── config.py                  # Configuration
├── requirements.txt           # Dependencies
├── src/
│   ├── data_generator.py      # Synthetic data generation
│   ├── feature_engineering.py # ML feature creation
│   ├── model_training.py      # Random Forest training
│   ├── alert_system.py        # SNS integration
│   └── cost_calculator.py     # AWS cost prediction
├── data/                      # Training data
├── models/                    # Trained models
└── logs/                      # Logs & alerts
```

---

## 📚 Documentation

| Document | Description |
|----------|-------------|
| [COMPLETE_SETUP_GUIDE.md](COMPLETE_SETUP_GUIDE.md) | Full step-by-step setup guide |
| [config.py](config.py) | Configuration settings |

---

## 🔔 Alert Types

| Alert | Trigger | Action |
|-------|---------|--------|
| ⚡ CPU_SPIKE | +25% jump | Immediate SNS email |
| ⚡ DISK_SPIKE | +15% jump | Immediate SNS email |
| 🚨 CPU_CRITICAL | CPU ≥ 80% | SNS email |
| 🚨 DISK_CRITICAL | Disk ≥ 85% | SNS email |
| 🔮 CPU_PREDICTION | Predicted ≥ 80% | SNS email |
| 🔮 DISK_PREDICTION | Predicted ≥ 85% | SNS email |

---

## 📊 ML Concepts Used (Day 31-39)

| Day | Concept | Implementation |
|-----|---------|----------------|
| 31 | ML Basics | Prediction system |
| 32 | Supervised Learning | Historical data training |
| 35-36 | Model Evaluation | RMSE, R² metrics |
| 38 | Cost Function | Optimization |
| 39 | Feature Engineering | 38+ features |

---

## 🛠️ Commands Reference

```bash
# Start monitoring
python monitor_continuous.py

# Background mode
nohup python monitor_continuous.py > logs/monitor.log 2>&1 &

# Stop monitoring
pkill -f monitor_continuous

# View logs
tail -f logs/monitor.log

# Check alerts
cat logs/alerts.log

# Test CPU load
stress --cpu 2 --timeout 60

# CloudWatch Agent status
sudo /opt/aws/amazon-cloudwatch-agent/bin/amazon-cloudwatch-agent-ctl -a status
```

---

## ⚙️ Configuration

Edit `config.py` to customize:

```python
# Thresholds
THRESHOLDS = {
    'cpu_warning': 70,
    'cpu_critical': 80,
    'disk_warning': 75,
    'disk_critical': 85,
}

# Spike detection
SPIKE_CONFIG = {
    'cpu_spike_threshold': 25,
    'disk_spike_threshold': 15,
}

# SNS
SNS_CONFIG = {
    'enabled': True,
    'topic_arn': 'arn:aws:sns:...',
    'region': 'us-east-1'
}
```

Edit `monitor_continuous.py` to set:

```python
INSTANCE_ID = "i-your-instance-id"
REGION = "us-east-1"
CHECK_INTERVAL_SECONDS = 30
```

---

## 📧 SNS Setup

1. Create SNS Topic in AWS Console
2. Subscribe your email
3. Confirm email subscription
4. Update `config.py` with topic ARN
5. Add `AmazonSNSFullAccess` to IAM user

---

## 🔍 Troubleshooting

| Issue | Solution |
|-------|----------|
| No CPU data | Wait 5-10 min for CloudWatch |
| Disk N/A | Install CloudWatch Agent |
| SNS Access Denied | Add SNS policy to IAM |
| Model not found | Run `python main.py` first |
| No email | Check spam folder |

---

## ✅ Setup Checklist

- [ ] AWS Account created
- [ ] IAM User with permissions
- [ ] EC2 Instance launched (Ubuntu)
- [ ] SSH connected
- [ ] Python & AWS CLI installed
- [ ] AWS credentials configured
- [ ] Virtual environment setup
- [ ] Packages installed
- [ ] SNS Topic created
- [ ] Email subscription confirmed
- [ ] CloudWatch Agent installed
- [ ] ML Model trained
- [ ] Monitoring running

---

## 📝 License

This project is for educational purposes as part of the MLOps/LLMOps course.

---

**Created:** November 2025
