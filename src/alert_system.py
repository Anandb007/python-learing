"""
Enhanced Alert System with Predictive Alerting
Sends email BEFORE resources reach critical levels
"""

import boto3
from datetime import datetime
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from config_autoscaling import (
        THRESHOLDS, ALERT_CONFIG, SNS_CONFIG, 
        CAUSE_ANALYSIS_CONFIG, SPIKE_CONFIG, PREDICTION_CONFIG,
        PREDICTION_THRESHOLDS
    )
except ImportError:
    from config import THRESHOLDS, ALERT_CONFIG, SNS_CONFIG
    CAUSE_ANALYSIS_CONFIG = {'enabled': False}
    PREDICTION_CONFIG = {
        'enabled': True, 
        'send_prediction_alerts': True,
        'alert_on_any_increase': True,
        'min_increase_for_alert': 10
    }
    SPIKE_CONFIG = {'cpu_spike_threshold': 25, 'disk_spike_threshold': 15}
    PREDICTION_THRESHOLDS = {
        'cpu_prediction_warning': 50,
        'cpu_prediction_critical': 65,
        'disk_prediction_warning': 60,
        'disk_prediction_critical': 75,
        'memory_prediction_warning': 65,
        'memory_prediction_critical': 80,
        'significant_increase': 15
    }


class CauseAnalyzer:
    """Analyzes probable causes of resource spikes"""
    
    def __init__(self):
        self.config = CAUSE_ANALYSIS_CONFIG if CAUSE_ANALYSIS_CONFIG else {'enabled': False}
    
    def analyze(self, alert_type, metrics, instance_info=None, time_context=None):
        """Analyze and return probable causes for the alert"""
        if not self.config.get('enabled', False):
            return []
        
        causes = []
        current_hour = datetime.now().hour
        is_business_hours = 9 <= current_hour <= 18
        is_night = current_hour < 6 or current_hour > 22
        
        common_causes = self.config.get('common_causes', {})
        
        # CPU Analysis
        if 'CPU' in alert_type:
            base_causes = common_causes.get('high_cpu', [
                'High application load/traffic',
                'Background processes or cron jobs',
                'Memory swapping due to low memory'
            ])
            
            if is_business_hours:
                causes.append("📊 Business hours - likely high user traffic")
            if is_night:
                causes.append("🌙 Night time - possible backup/cron jobs running")
            
            if metrics:
                if metrics.get('memory_utilization') and metrics.get('memory_utilization', 0) > 70:
                    causes.append("💾 High memory - possible swapping causing CPU load")
                if metrics.get('disk_utilization') and metrics.get('disk_utilization', 0) > 80:
                    causes.append("💿 High disk I/O bottleneck")
            
            causes.extend(base_causes[:3])
        
        # Disk Analysis
        elif 'DISK' in alert_type:
            base_causes = common_causes.get('high_disk', [
                'Log files growing rapidly',
                'Database growth',
                'Temp files accumulation'
            ])
            
            if is_night:
                causes.append("🌙 Night time - possible backup running")
            
            causes.extend(base_causes[:3])
        
        # Memory Analysis
        elif 'MEMORY' in alert_type:
            base_causes = common_causes.get('high_memory', [
                'Memory leak in application',
                'Cache not being cleared',
                'Too many connections/sessions'
            ])
            causes.extend(base_causes[:3])
        
        # Network Analysis
        elif 'NETWORK' in alert_type:
            base_causes = common_causes.get('high_network', [
                'DDoS attack or traffic spike',
                'Large data transfer',
                'High user traffic'
            ])
            
            if is_business_hours:
                causes.append("📊 Business hours - high user traffic")
            
            causes.extend(base_causes[:3])
        
        # Prediction-specific
        if 'PREDICTION' in alert_type or 'TREND' in alert_type:
            causes.insert(0, "🔮 ML model predicts increase based on current trend")
        
        # Spike-specific
        if 'SPIKE' in alert_type:
            causes.insert(0, "⚡ Sudden change - immediate investigation needed")
        
        return causes[:5]


class AlertSystem:
    """Enhanced Alert System with Predictive Alerting"""
    
    def __init__(self):
        self.thresholds = THRESHOLDS
        self.prediction_thresholds = PREDICTION_THRESHOLDS
        self.sns_enabled = SNS_CONFIG.get('enabled', False) and ALERT_CONFIG.get('sns_alerts', False)
        self.cause_analyzer = CauseAnalyzer()
        self.last_prediction_alerts = {}
        
        if self.sns_enabled:
            try:
                self.sns_client = boto3.client('sns', region_name=SNS_CONFIG.get('region', 'us-east-1'))
                self.topic_arn = SNS_CONFIG.get('topic_arn', '')
                print(f"   ✅ SNS enabled: {self.topic_arn}")
            except Exception as e:
                print(f"   ⚠️ SNS init failed: {e}")
                self.sns_enabled = False
    
    def _should_send_prediction_alert(self, alert_key):
        """Check if we should send this prediction alert (cooldown)"""
        cooldown = ALERT_CONFIG.get('prediction_email_cooldown', 1800)
        now = datetime.now()
        
        if alert_key in self.last_prediction_alerts:
            last_sent = self.last_prediction_alerts[alert_key]
            if (now - last_sent).total_seconds() < cooldown:
                return False
        
        self.last_prediction_alerts[alert_key] = now
        return True
    
    def check(self, metrics, predicted_cpu=None, predicted_disk=None, 
              predicted_memory=None, trends=None):
        """Check all metrics and predictions against thresholds"""
        alerts = []
        trends = trends or {}
        
        cpu = metrics.get('cpu_utilization') or 0
        disk = metrics.get('disk_utilization')
        memory = metrics.get('memory_utilization')
        network_in = metrics.get('network_in') or 0
        
        # ============================================================
        # CURRENT VALUE ALERTS (Resource is ALREADY high)
        # ============================================================
        
        # CPU Current
        if cpu >= self.thresholds['cpu_critical']:
            alerts.append({
                'type': 'CPU_CRITICAL',
                'metric': 'CPU',
                'value': cpu,
                'threshold': self.thresholds['cpu_critical'],
                'severity': 'CRITICAL',
                'message': f'🚨 CPU CRITICAL: {cpu:.1f}% (threshold: {self.thresholds["cpu_critical"]}%)',
                'action_required': 'Immediate - Check processes, scale now',
                'send_email': True
            })
        elif cpu >= self.thresholds['cpu_warning']:
            alerts.append({
                'type': 'CPU_WARNING',
                'metric': 'CPU',
                'value': cpu,
                'threshold': self.thresholds['cpu_warning'],
                'severity': 'WARNING',
                'message': f'⚠️ CPU WARNING: {cpu:.1f}% (threshold: {self.thresholds["cpu_warning"]}%)',
                'action_required': 'Monitor closely',
                'send_email': True
            })
        
        # Disk Current
        if disk is not None:
            if disk >= self.thresholds['disk_critical']:
                alerts.append({
                    'type': 'DISK_CRITICAL',
                    'metric': 'DISK',
                    'value': disk,
                    'threshold': self.thresholds['disk_critical'],
                    'severity': 'CRITICAL',
                    'message': f'🚨 DISK CRITICAL: {disk:.1f}% (threshold: {self.thresholds["disk_critical"]}%)',
                    'action_required': 'Clear disk immediately',
                    'send_email': True
                })
            elif disk >= self.thresholds['disk_warning']:
                alerts.append({
                    'type': 'DISK_WARNING',
                    'metric': 'DISK',
                    'value': disk,
                    'threshold': self.thresholds['disk_warning'],
                    'severity': 'WARNING',
                    'message': f'⚠️ DISK WARNING: {disk:.1f}% (threshold: {self.thresholds["disk_warning"]}%)',
                    'action_required': 'Plan disk cleanup',
                    'send_email': True
                })
        
        # Memory Current
        if memory is not None:
            memory_critical = self.thresholds.get('memory_critical', 95)
            memory_warning = self.thresholds.get('memory_warning', 80)
            
            if memory >= memory_critical:
                alerts.append({
                    'type': 'MEMORY_CRITICAL',
                    'metric': 'MEMORY',
                    'value': memory,
                    'threshold': memory_critical,
                    'severity': 'CRITICAL',
                    'message': f'🚨 MEMORY CRITICAL: {memory:.1f}% (threshold: {memory_critical}%)',
                    'action_required': 'Check memory leaks immediately',
                    'send_email': True
                })
            elif memory >= memory_warning:
                alerts.append({
                    'type': 'MEMORY_WARNING',
                    'metric': 'MEMORY',
                    'value': memory,
                    'threshold': memory_warning,
                    'severity': 'WARNING',
                    'message': f'⚠️ MEMORY WARNING: {memory:.1f}% (threshold: {memory_warning}%)',
                    'action_required': 'Monitor memory usage',
                    'send_email': True
                })
        
        # Network Current
        network_in_critical = self.thresholds.get('network_in_critical', float('inf'))
        network_in_warning = self.thresholds.get('network_in_warning', float('inf'))
        
        if network_in >= network_in_critical:
            alerts.append({
                'type': 'NETWORK_IN_CRITICAL',
                'metric': 'NETWORK',
                'value': network_in,
                'threshold': network_in_critical,
                'severity': 'CRITICAL',
                'message': f'🚨 NETWORK IN CRITICAL: {network_in/1000000:.1f} MB/s',
                'action_required': 'Check for DDoS or unusual traffic',
                'send_email': True
            })
        elif network_in >= network_in_warning:
            alerts.append({
                'type': 'NETWORK_IN_WARNING',
                'metric': 'NETWORK',
                'value': network_in,
                'threshold': network_in_warning,
                'severity': 'WARNING',
                'message': f'⚠️ NETWORK IN WARNING: {network_in/1000000:.1f} MB/s',
                'action_required': 'Monitor network traffic',
                'send_email': True
            })
        
        # ============================================================
        # PREDICTION ALERTS - Send email BEFORE resource reaches high
        # ============================================================
        
        if PREDICTION_CONFIG.get('send_prediction_alerts', True):
            min_increase = PREDICTION_CONFIG.get('min_increase_for_alert', 10)
            
            # ===== CPU Prediction =====
            if predicted_cpu is not None:
                increase = predicted_cpu - cpu
                
                # CRITICAL: Will reach critical threshold
                if predicted_cpu >= self.prediction_thresholds.get('cpu_prediction_critical', 65):
                    alerts.append({
                        'type': 'CPU_PREDICTION_CRITICAL',
                        'metric': 'CPU_PREDICTED',
                        'value': predicted_cpu,
                        'current_value': cpu,
                        'increase': increase,
                        'severity': 'WARNING',
                        'is_prediction': True,
                        'send_email': True,
                        'message': f'🔮 CPU WILL REACH CRITICAL!\n   Current: {cpu:.1f}% → Predicted: {predicted_cpu:.1f}% in ~1 hour\n   Expected increase: +{increase:.1f}%',
                        'action_required': '⚡ ACT NOW: Scale up or optimize BEFORE CPU spikes!'
                    })
                
                # WARNING: Will reach warning threshold  
                elif predicted_cpu >= self.prediction_thresholds.get('cpu_prediction_warning', 50):
                    alerts.append({
                        'type': 'CPU_PREDICTION_WARNING',
                        'metric': 'CPU_PREDICTED',
                        'value': predicted_cpu,
                        'current_value': cpu,
                        'increase': increase,
                        'severity': 'INFO',
                        'is_prediction': True,
                        'send_email': True,
                        'message': f'🔮 CPU TRENDING UP!\n   Current: {cpu:.1f}% → Predicted: {predicted_cpu:.1f}% in ~1 hour\n   Expected increase: +{increase:.1f}%',
                        'action_required': 'Prepare to scale - CPU increasing'
                    })
                
                # SIGNIFICANT INCREASE: Any big jump predicted
                elif increase >= self.prediction_thresholds.get('significant_increase', 15):
                    alerts.append({
                        'type': 'CPU_INCREASE_PREDICTED',
                        'metric': 'CPU_TREND',
                        'value': predicted_cpu,
                        'current_value': cpu,
                        'increase': increase,
                        'severity': 'INFO',
                        'is_prediction': True,
                        'send_email': True,
                        'message': f'📈 CPU INCREASE EXPECTED!\n   Current: {cpu:.1f}% → Predicted: {predicted_cpu:.1f}%\n   Expected increase: +{increase:.1f}% in ~1 hour',
                        'action_required': 'Monitor - significant CPU increase coming'
                    })
                
                # ANY INCREASE: Alert on any predicted increase (if enabled)
                elif PREDICTION_CONFIG.get('alert_on_any_increase', False) and increase >= min_increase:
                    alerts.append({
                        'type': 'CPU_TRENDING_UP',
                        'metric': 'CPU_TREND',
                        'value': predicted_cpu,
                        'current_value': cpu,
                        'increase': increase,
                        'severity': 'INFO',
                        'is_prediction': True,
                        'send_email': True,
                        'message': f'📊 CPU Trend Alert\n   Current: {cpu:.1f}% → Predicted: {predicted_cpu:.1f}%\n   Increase: +{increase:.1f}%',
                        'action_required': 'Informational - CPU trending upward'
                    })
            
            # ===== Disk Prediction =====
            if predicted_disk is not None and disk is not None:
                disk_increase = predicted_disk - disk
                
                if predicted_disk >= self.prediction_thresholds.get('disk_prediction_critical', 75):
                    alerts.append({
                        'type': 'DISK_PREDICTION_CRITICAL',
                        'metric': 'DISK_PREDICTED',
                        'value': predicted_disk,
                        'current_value': disk,
                        'increase': disk_increase,
                        'severity': 'WARNING',
                        'is_prediction': True,
                        'send_email': True,
                        'message': f'🔮 DISK WILL REACH CRITICAL!\n   Current: {disk:.1f}% → Predicted: {predicted_disk:.1f}%\n   Expected increase: +{disk_increase:.1f}%',
                        'action_required': '⚡ ACT NOW: Start disk cleanup before it fills!'
                    })
                elif predicted_disk >= self.prediction_thresholds.get('disk_prediction_warning', 60):
                    alerts.append({
                        'type': 'DISK_PREDICTION_WARNING',
                        'metric': 'DISK_PREDICTED',
                        'value': predicted_disk,
                        'current_value': disk,
                        'increase': disk_increase,
                        'severity': 'INFO',
                        'is_prediction': True,
                        'send_email': True,
                        'message': f'🔮 DISK TRENDING UP!\n   Current: {disk:.1f}% → Predicted: {predicted_disk:.1f}%',
                        'action_required': 'Plan disk cleanup - usage increasing'
                    })
                elif disk_increase >= self.prediction_thresholds.get('significant_increase', 15):
                    alerts.append({
                        'type': 'DISK_INCREASE_PREDICTED',
                        'metric': 'DISK_TREND',
                        'value': predicted_disk,
                        'current_value': disk,
                        'increase': disk_increase,
                        'severity': 'INFO',
                        'is_prediction': True,
                        'send_email': True,
                        'message': f'📈 DISK INCREASE EXPECTED!\n   Current: {disk:.1f}% → Predicted: {predicted_disk:.1f}%',
                        'action_required': 'Monitor disk growth'
                    })
            
            # ===== Memory Prediction =====
            if predicted_memory is not None and memory is not None:
                mem_increase = predicted_memory - memory
                
                if predicted_memory >= self.prediction_thresholds.get('memory_prediction_critical', 80):
                    alerts.append({
                        'type': 'MEMORY_PREDICTION_CRITICAL',
                        'metric': 'MEMORY_PREDICTED',
                        'value': predicted_memory,
                        'current_value': memory,
                        'increase': mem_increase,
                        'severity': 'WARNING',
                        'is_prediction': True,
                        'send_email': True,
                        'message': f'🔮 MEMORY WILL REACH CRITICAL!\n   Current: {memory:.1f}% → Predicted: {predicted_memory:.1f}%\n   Expected increase: +{mem_increase:.1f}%',
                        'action_required': '⚡ ACT NOW: Check for memory leaks!'
                    })
                elif predicted_memory >= self.prediction_thresholds.get('memory_prediction_warning', 65):
                    alerts.append({
                        'type': 'MEMORY_PREDICTION_WARNING',
                        'metric': 'MEMORY_PREDICTED',
                        'value': predicted_memory,
                        'current_value': memory,
                        'increase': mem_increase,
                        'severity': 'INFO',
                        'is_prediction': True,
                        'send_email': True,
                        'message': f'🔮 MEMORY TRENDING UP!\n   Current: {memory:.1f}% → Predicted: {predicted_memory:.1f}%',
                        'action_required': 'Monitor memory usage'
                    })
                elif mem_increase >= self.prediction_thresholds.get('significant_increase', 15):
                    alerts.append({
                        'type': 'MEMORY_INCREASE_PREDICTED',
                        'metric': 'MEMORY_TREND',
                        'value': predicted_memory,
                        'current_value': memory,
                        'increase': mem_increase,
                        'severity': 'INFO',
                        'is_prediction': True,
                        'send_email': True,
                        'message': f'📈 MEMORY INCREASE EXPECTED!\n   Current: {memory:.1f}% → Predicted: {predicted_memory:.1f}%',
                        'action_required': 'Monitor memory growth'
                    })
        
        return alerts
    
    def add_cause_analysis(self, alert, metrics):
        """Add probable cause analysis to an alert"""
        causes = self.cause_analyzer.analyze(alert['type'], metrics)
        alert['probable_causes'] = causes
        return alert
    
    def format_scaling_event(self, event_type, instance_ids, instance_details, trigger_reason=None):
        """Format scaling event notification"""
        message = f"\n{'➕ NEW INSTANCES' if event_type == 'SCALE_OUT' else '➖ TERMINATED'}:\n"
        for inst_id in instance_ids:
            d = instance_details.get(inst_id, {})
            message += f"   • {inst_id}: {d.get('name', 'N/A')} ({d.get('instance_type', 'N/A')}) - {d.get('availability_zone', 'N/A')}\n"
        if trigger_reason:
            message += f"\n   Trigger: {trigger_reason}\n"
        return message
    
    def send_sns_alert(self, alert, instance_info=None, metrics=None, scaling_details=None):
        """Send alert via AWS SNS"""
        if not self.sns_enabled or not self.topic_arn:
            return False
        
        # Check cooldown for prediction alerts
        if alert.get('is_prediction'):
            alert_key = f"{alert['type']}_{instance_info.get('instance_id', 'asg') if instance_info else 'asg'}"
            if not self._should_send_prediction_alert(alert_key):
                print(f"   ⏳ Prediction alert skipped (cooldown)")
                return False
        
        try:
            # Add cause analysis
            if ALERT_CONFIG.get('include_cause_analysis', True) and metrics:
                alert = self.add_cause_analysis(alert, metrics)
            
            is_prediction = alert.get('is_prediction', False)
            
            severity_emoji = {'CRITICAL': '🚨', 'WARNING': '⚠️', 'INFO': '🔮'}
            emoji = severity_emoji.get(alert.get('severity', 'WARNING'), '⚠️')
            
            if is_prediction:
                emoji = '🔮'
            
            subject = f"{emoji} [{alert['type']}] {alert.get('severity', 'ALERT')}"
            
            message = f"""
══════════════════════════════════════════════════════════════════════
{emoji} {'🔮 PREDICTIVE ALERT - ACT BEFORE IT HAPPENS!' if is_prediction else 'ML MONITORING ALERT'}
══════════════════════════════════════════════════════════════════════

⏰ Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
📍 Alert Type: {alert['type']}
🎚️ Severity: {alert.get('severity', 'N/A')}

══════════════════════════════════════════════════════════════════════
📊 ALERT DETAILS
══════════════════════════════════════════════════════════════════════

{alert['message']}
"""
            
            if is_prediction and 'current_value' in alert:
                message += f"""
══════════════════════════════════════════════════════════════════════
📈 PREDICTION SUMMARY
══════════════════════════════════════════════════════════════════════

   📍 Current Value: {alert['current_value']:.1f}%
   🔮 Predicted Value: {alert['value']:.1f}%
   ⬆️ Expected Increase: +{alert.get('increase', 0):.1f}%
   ⏱️ Timeframe: ~1 hour
"""
            
            message += f"""
══════════════════════════════════════════════════════════════════════
⚡ ACTION REQUIRED
══════════════════════════════════════════════════════════════════════

   {alert.get('action_required', 'Please investigate this alert')}
"""
            
            # Add probable causes
            if alert.get('probable_causes'):
                message += f"""
══════════════════════════════════════════════════════════════════════
🔍 PROBABLE CAUSES
══════════════════════════════════════════════════════════════════════
"""
                for i, cause in enumerate(alert['probable_causes'], 1):
                    message += f"\n   {i}. {cause}"
                message += "\n"
            
            # Add instance info
            if instance_info:
                message += f"""
══════════════════════════════════════════════════════════════════════
🖥️ INSTANCE DETAILS
══════════════════════════════════════════════════════════════════════

   • Instance ID: {instance_info.get('instance_id', 'N/A')}
   • Name: {instance_info.get('name', 'N/A')}
   • Type: {instance_info.get('instance_type', 'N/A')}
   • AZ: {instance_info.get('availability_zone', 'N/A')}
   • Public IP: {instance_info.get('public_ip', 'N/A')}
"""
            
            # Add current metrics
            if metrics:
                cpu_val = metrics.get('cpu_utilization') or 0
                disk_val = metrics.get('disk_utilization') or 0
                mem_val = metrics.get('memory_utilization') or 0
                net_in = metrics.get('network_in') or 0
                net_out = metrics.get('network_out') or 0
                
                message += f"""
══════════════════════════════════════════════════════════════════════
📈 CURRENT METRICS SNAPSHOT
══════════════════════════════════════════════════════════════════════

   • CPU: {cpu_val:.1f}%
   • Disk: {disk_val:.1f}%
   • Memory: {mem_val:.1f}%
   • Network In: {net_in/1000000:.2f} MB/s
   • Network Out: {net_out/1000000:.2f} MB/s
"""
            
            # Add scaling details
            if scaling_details:
                message += scaling_details
            
            message += """
══════════════════════════════════════════════════════════════════════
📧 This alert was generated by ML Monitoring System
══════════════════════════════════════════════════════════════════════
"""
            
            response = self.sns_client.publish(
                TopicArn=self.topic_arn,
                Subject=subject[:100],
                Message=message
            )
            
            alert_type = 'Prediction' if is_prediction else 'Alert'
            print(f"   📧 {alert_type} email sent! MessageId: {response['MessageId']}")
            return True
            
        except Exception as e:
            print(f"   ❌ SNS Error: {e}")
            return False
    
    def send(self, alerts, instance_info=None, metrics=None, scaling_details=None):
        """Send all alerts"""
        for alert in alerts:
            is_prediction = alert.get('is_prediction', False)
            
            # Console output
            symbol = '🔮' if is_prediction else '🔴'
            print(f"\n{symbol}" * 20)
            print(f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"🎚️ Severity: {alert.get('severity', 'N/A')}")
            
            if is_prediction:
                print("🔮 PREDICTION ALERT - ACT BEFORE IT HAPPENS!")
            
            print(alert['message'])
            
            if alert.get('action_required'):
                print(f"⚡ Action: {alert['action_required']}")
            
            # Add cause analysis for console
            if ALERT_CONFIG.get('include_cause_analysis', True) and metrics:
                alert = self.add_cause_analysis(alert, metrics)
                if alert.get('probable_causes'):
                    print("\n🔍 Probable Causes:")
                    for cause in alert['probable_causes'][:3]:
                        print(f"   • {cause}")
            
            print(f"{symbol}" * 20)
            
            # Log to file
            if ALERT_CONFIG.get('log_alerts', True):
                log_file = ALERT_CONFIG.get('log_file', 'logs/alerts.log')
                os.makedirs(os.path.dirname(log_file), exist_ok=True)
                with open(log_file, 'a') as f:
                    log_entry = f"{datetime.now().isoformat()} | {alert.get('severity', 'N/A')} | {alert['type']} | {alert['message']}\n"
                    f.write(log_entry)
            
            # Send email
            if alert.get('send_email', False) and self.sns_enabled:
                self.send_sns_alert(alert, instance_info, metrics, scaling_details)
