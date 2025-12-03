"""
Auto Scaling Group ML Monitoring with Predictive Alerts
Monitors CPU, Disk, Memory, Network with ML predictions
Sends alerts BEFORE resources reach critical levels
"""

import boto3
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import time
import sys
import os
from collections import defaultdict

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from asg_discovery import ASGDiscovery
from feature_engineering import FeatureEngineer
from model_training import CPUPredictor
from alert_system import AlertSystem
from config_autoscaling import (
    THRESHOLDS, SNS_CONFIG, SPIKE_CONFIG, 
    MONITORING_CONFIG, AUTOSCALING_CONFIG, AWS_REGION,
    PREDICTION_CONFIG
)


class InstanceMetricsTracker:
    """Tracks metrics history and detects spikes for all resource types"""
    
    def __init__(self):
        self.cpu_history = defaultdict(list)
        self.disk_history = defaultdict(list)
        self.memory_history = defaultdict(list)
        self.network_in_history = defaultdict(list)
        self.network_out_history = defaultdict(list)
        
        self.previous_cpu = {}
        self.previous_disk = {}
        self.previous_memory = {}
        self.previous_network_in = {}
        self.previous_network_out = {}
    
    def check_all_spikes(self, instance_id, metrics):
        """Check for spikes in all metrics"""
        spikes = []
        
        cpu = metrics.get('cpu_utilization') or 0
        disk = metrics.get('disk_utilization')
        memory = metrics.get('memory_utilization')
        network_in = metrics.get('network_in') or 0
        network_out = metrics.get('network_out') or 0
        
        # CPU Spike
        if instance_id in self.previous_cpu:
            change = cpu - self.previous_cpu[instance_id]
            if change >= SPIKE_CONFIG['cpu_spike_threshold']:
                spikes.append({
                    'type': 'CPU_SPIKE',
                    'metric': 'CPU',
                    'instance_id': instance_id,
                    'previous': self.previous_cpu[instance_id],
                    'current': cpu,
                    'change': change,
                    'severity': 'WARNING',
                    'send_email': True,
                    'message': f'⚡ CPU SPIKE: {self.previous_cpu[instance_id]:.1f}% → {cpu:.1f}% (+{change:.1f}%)',
                    'action_required': 'Investigate sudden CPU increase'
                })
        
        # Disk Spike
        if disk is not None and instance_id in self.previous_disk:
            change = disk - self.previous_disk[instance_id]
            if change >= SPIKE_CONFIG['disk_spike_threshold']:
                spikes.append({
                    'type': 'DISK_SPIKE',
                    'metric': 'DISK',
                    'instance_id': instance_id,
                    'previous': self.previous_disk[instance_id],
                    'current': disk,
                    'change': change,
                    'severity': 'WARNING',
                    'send_email': True,
                    'message': f'⚡ DISK SPIKE: {self.previous_disk[instance_id]:.1f}% → {disk:.1f}% (+{change:.1f}%)',
                    'action_required': 'Check for large file writes or log growth'
                })
        
        # Memory Spike
        if memory is not None and instance_id in self.previous_memory:
            change = memory - self.previous_memory[instance_id]
            if change >= SPIKE_CONFIG.get('memory_spike_threshold', 20):
                spikes.append({
                    'type': 'MEMORY_SPIKE',
                    'metric': 'MEMORY',
                    'instance_id': instance_id,
                    'previous': self.previous_memory[instance_id],
                    'current': memory,
                    'change': change,
                    'severity': 'WARNING',
                    'send_email': True,
                    'message': f'⚡ MEMORY SPIKE: {self.previous_memory[instance_id]:.1f}% → {memory:.1f}% (+{change:.1f}%)',
                    'action_required': 'Check for memory leaks or large allocations'
                })
        
        # Network In Spike (percentage based)
        if network_in > 0 and instance_id in self.previous_network_in and self.previous_network_in[instance_id] > 0:
            change_pct = ((network_in - self.previous_network_in[instance_id]) / self.previous_network_in[instance_id]) * 100
            if change_pct >= SPIKE_CONFIG.get('network_spike_threshold', 50):
                spikes.append({
                    'type': 'NETWORK_IN_SPIKE',
                    'metric': 'NETWORK_IN',
                    'instance_id': instance_id,
                    'previous': self.previous_network_in[instance_id],
                    'current': network_in,
                    'change': change_pct,
                    'severity': 'WARNING',
                    'send_email': True,
                    'message': f'⚡ NETWORK IN SPIKE: {self.previous_network_in[instance_id]/1000000:.1f} MB/s → {network_in/1000000:.1f} MB/s (+{change_pct:.0f}%)',
                    'action_required': 'Check for traffic surge or potential DDoS'
                })
        
        # Network Out Spike
        if network_out > 0 and instance_id in self.previous_network_out and self.previous_network_out[instance_id] > 0:
            change_pct = ((network_out - self.previous_network_out[instance_id]) / self.previous_network_out[instance_id]) * 100
            if change_pct >= SPIKE_CONFIG.get('network_spike_threshold', 50):
                spikes.append({
                    'type': 'NETWORK_OUT_SPIKE',
                    'metric': 'NETWORK_OUT',
                    'instance_id': instance_id,
                    'previous': self.previous_network_out[instance_id],
                    'current': network_out,
                    'change': change_pct,
                    'severity': 'WARNING',
                    'send_email': True,
                    'message': f'⚡ NETWORK OUT SPIKE: {self.previous_network_out[instance_id]/1000000:.1f} MB/s → {network_out/1000000:.1f} MB/s (+{change_pct:.0f}%)',
                    'action_required': 'Check for data exfiltration or large transfers'
                })
        
        # Update history
        self._update_history(instance_id, metrics)
        
        return spikes
    
    def _update_history(self, instance_id, metrics):
        """Update all metric histories"""
        # CPU
        if metrics.get('cpu_utilization') is not None:
            self.previous_cpu[instance_id] = metrics['cpu_utilization']
            self.cpu_history[instance_id].append(metrics['cpu_utilization'])
            if len(self.cpu_history[instance_id]) > 20:
                self.cpu_history[instance_id].pop(0)
        
        # Disk
        if metrics.get('disk_utilization') is not None:
            self.previous_disk[instance_id] = metrics['disk_utilization']
            self.disk_history[instance_id].append(metrics['disk_utilization'])
            if len(self.disk_history[instance_id]) > 20:
                self.disk_history[instance_id].pop(0)
        
        # Memory
        if metrics.get('memory_utilization') is not None:
            self.previous_memory[instance_id] = metrics['memory_utilization']
            self.memory_history[instance_id].append(metrics['memory_utilization'])
            if len(self.memory_history[instance_id]) > 20:
                self.memory_history[instance_id].pop(0)
        
        # Network In
        if metrics.get('network_in') is not None:
            self.previous_network_in[instance_id] = metrics['network_in']
            self.network_in_history[instance_id].append(metrics['network_in'])
            if len(self.network_in_history[instance_id]) > 20:
                self.network_in_history[instance_id].pop(0)
        
        # Network Out
        if metrics.get('network_out') is not None:
            self.previous_network_out[instance_id] = metrics['network_out']
            self.network_out_history[instance_id].append(metrics['network_out'])
            if len(self.network_out_history[instance_id]) > 20:
                self.network_out_history[instance_id].pop(0)
    
    def remove_instance(self, instance_id):
        """Clean up data for terminated instance"""
        for d in [self.cpu_history, self.disk_history, self.memory_history,
                  self.network_in_history, self.network_out_history,
                  self.previous_cpu, self.previous_disk, self.previous_memory,
                  self.previous_network_in, self.previous_network_out]:
            d.pop(instance_id, None)
    
    def get_trend(self, instance_id, metric_type='cpu'):
        """Calculate trend for predictions"""
        history_map = {
            'cpu': self.cpu_history,
            'disk': self.disk_history,
            'memory': self.memory_history,
            'network_in': self.network_in_history,
            'network_out': self.network_out_history
        }
        history = history_map.get(metric_type, {}).get(instance_id, [])
        if len(history) >= 3:
            return np.mean(np.diff(history[-5:]))
        return 0


class ASGMonitor:
    """Main monitoring class for Auto Scaling Group"""
    
    def __init__(self):
        self.region = AWS_REGION
        self.cloudwatch = boto3.client('cloudwatch', region_name=self.region)
        self.sns = boto3.client('sns', region_name=self.region)
        self.autoscaling = boto3.client('autoscaling', region_name=self.region)
        
        print("\n🔍 Initializing ASG Discovery...")
        self.discovery = ASGDiscovery()
        self.instances = {}
        self.last_discovery_time = None
        
        self.metrics_tracker = InstanceMetricsTracker()
        
        print("\n🤖 Loading ML Model...")
        self.predictor = CPUPredictor()
        try:
            self.predictor.load('models/cpu_predictor.pkl')
            print("   ✅ Model loaded!")
        except FileNotFoundError:
            print("   ⚠️ Model not found. Run 'python main.py' first.")
            self.predictor = None
        
        self.fe = FeatureEngineer()
        
        print("\n📧 Initializing Alert System...")
        self.alert_sys = AlertSystem()
    
    def refresh_instances(self, force=False):
        """Refresh instance list and detect scaling events"""
        now = datetime.now()
        interval = MONITORING_CONFIG['instance_discovery_interval_seconds']
        
        should_refresh = (
            force or 
            self.last_discovery_time is None or 
            (now - self.last_discovery_time).total_seconds() > interval
        )
        
        if should_refresh:
            old_instances = set(self.instances.keys())
            self.instances = self.discovery.discover_instances()
            new_instances = set(self.instances.keys())
            self.last_discovery_time = now
            
            added = new_instances - old_instances
            removed = old_instances - new_instances
            
            if added:
                print(f"\n📈 SCALE OUT DETECTED: {len(added)} new instance(s)")
                trigger_reason = self._get_scaling_trigger_reason()
                self._send_scaling_alert('SCALE_OUT', added, trigger_reason)
            
            if removed:
                print(f"\n📉 SCALE IN DETECTED: {len(removed)} instance(s) terminated")
                for inst_id in removed:
                    self.metrics_tracker.remove_instance(inst_id)
                self._send_scaling_alert('SCALE_IN', removed, None)
    
    def _get_scaling_trigger_reason(self):
        """Get the reason for the most recent scaling activity"""
        try:
            response = self.autoscaling.describe_scaling_activities(
                AutoScalingGroupName=AUTOSCALING_CONFIG['asg_name'],
                MaxRecords=5
            )
            if response['Activities']:
                latest = response['Activities'][0]
                cause = latest.get('Cause', 'Unknown')
                if 'CPU' in cause.upper():
                    return f"🔥 High CPU triggered scaling\n   {cause[:200]}"
                elif 'ALARM' in cause.upper():
                    return f"🔔 CloudWatch Alarm triggered\n   {cause[:200]}"
                elif 'user' in cause.lower():
                    return f"👤 Manual scaling\n   {cause[:200]}"
                else:
                    return f"📊 Auto-scaling\n   {cause[:200]}"
            return None
        except Exception as e:
            return None
    
    def _send_scaling_alert(self, event_type, instance_ids, trigger_reason=None):
        """Send detailed scaling event notification"""
        if not SNS_CONFIG.get('enabled'):
            return
        
        # Get details for instances
        instance_details = {}
        for inst_id in instance_ids:
            if inst_id in self.instances:
                instance_details[inst_id] = self.instances[inst_id]
            else:
                try:
                    response = self.discovery.ec2.describe_instances(InstanceIds=[inst_id])
                    for res in response['Reservations']:
                        for inst in res['Instances']:
                            instance_details[inst_id] = {
                                'name': next((t['Value'] for t in inst.get('Tags', []) if t['Key'] == 'Name'), 'N/A'),
                                'instance_type': inst.get('InstanceType', 'N/A'),
                                'availability_zone': inst.get('Placement', {}).get('AvailabilityZone', 'N/A'),
                                'private_ip': inst.get('PrivateIpAddress', 'N/A'),
                                'public_ip': inst.get('PublicIpAddress', 'N/A'),
                                'launch_time': str(inst.get('LaunchTime', 'N/A'))
                            }
                except:
                    instance_details[inst_id] = {'name': 'N/A', 'instance_type': 'N/A'}
        
        try:
            message = f"""
══════════════════════════════════════════════════════════════════════
🔄 AUTO SCALING EVENT: {event_type}
══════════════════════════════════════════════════════════════════════

⏰ Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
📦 ASG: {AUTOSCALING_CONFIG['asg_name']}
📊 Current Instance Count: {len(self.instances)}

══════════════════════════════════════════════════════════════════════
{'➕ NEW INSTANCES LAUNCHED' if event_type == 'SCALE_OUT' else '➖ INSTANCES TERMINATED'}
══════════════════════════════════════════════════════════════════════
"""
            for inst_id in instance_ids:
                d = instance_details.get(inst_id, {})
                message += f"""
   Instance: {inst_id}
   • Name: {d.get('name', 'N/A')}
   • Type: {d.get('instance_type', 'N/A')}
   • AZ: {d.get('availability_zone', 'N/A')}
   • Private IP: {d.get('private_ip', 'N/A')}
   • Public IP: {d.get('public_ip', 'N/A')}
   • Launch Time: {d.get('launch_time', 'N/A')}
"""
            
            if trigger_reason:
                message += f"""
══════════════════════════════════════════════════════════════════════
📊 SCALING TRIGGER REASON
══════════════════════════════════════════════════════════════════════

   {trigger_reason}
"""
            
            message += """
══════════════════════════════════════════════════════════════════════
"""
            
            subject = f"🔄 {event_type}: ASG {AUTOSCALING_CONFIG['asg_name']} - {len(instance_ids)} instance(s)"
            
            self.sns.publish(
                TopicArn=SNS_CONFIG['topic_arn'],
                Subject=subject[:100],
                Message=message
            )
            print(f"   📧 Scaling alert sent!")
            
        except Exception as e:
            print(f"   ❌ Failed to send scaling alert: {e}")
    
    def get_all_metrics(self, instance_id):
        """Fetch all metrics for an instance"""
        end_time = datetime.utcnow()
        start_time = end_time - timedelta(minutes=5)
        
        metrics = {
            'cpu_utilization': None,
            'disk_utilization': None,
            'memory_utilization': None,
            'network_in': None,
            'network_out': None
        }
        
        # CPU from AWS/EC2
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
                        'Period': 60,
                        'Stat': 'Average'
                    },
                    'ReturnData': True
                }],
                StartTime=start_time,
                EndTime=end_time
            )
            values = response['MetricDataResults'][0]['Values']
            if values:
                metrics['cpu_utilization'] = max(values)
        except Exception as e:
            pass
        
        # Network from AWS/EC2
        try:
            response = self.cloudwatch.get_metric_data(
                MetricDataQueries=[
                    {
                        'Id': 'netin',
                        'MetricStat': {
                            'Metric': {
                                'Namespace': 'AWS/EC2',
                                'MetricName': 'NetworkIn',
                                'Dimensions': [{'Name': 'InstanceId', 'Value': instance_id}]
                            },
                            'Period': 60,
                            'Stat': 'Average'
                        },
                        'ReturnData': True
                    },
                    {
                        'Id': 'netout',
                        'MetricStat': {
                            'Metric': {
                                'Namespace': 'AWS/EC2',
                                'MetricName': 'NetworkOut',
                                'Dimensions': [{'Name': 'InstanceId', 'Value': instance_id}]
                            },
                            'Period': 60,
                            'Stat': 'Average'
                        },
                        'ReturnData': True
                    }
                ],
                StartTime=start_time,
                EndTime=end_time
            )
            for result in response['MetricDataResults']:
                if result['Id'] == 'netin' and result['Values']:
                    metrics['network_in'] = max(result['Values'])
                elif result['Id'] == 'netout' and result['Values']:
                    metrics['network_out'] = max(result['Values'])
        except Exception as e:
            pass
        
        # Disk and Memory from CWAgent
        try:
            response = self.cloudwatch.get_metric_data(
                MetricDataQueries=[
                    {
                        'Id': 'disk',
                        'MetricStat': {
                            'Metric': {
                                'Namespace': 'CWAgent',
                                'MetricName': 'disk_used_percent',
                                'Dimensions': [
                                    {'Name': 'InstanceId', 'Value': instance_id},
                                    {'Name': 'path', 'Value': '/'}
                                ]
                            },
                            'Period': 60,
                            'Stat': 'Average'
                        },
                        'ReturnData': True
                    },
                    {
                        'Id': 'mem',
                        'MetricStat': {
                            'Metric': {
                                'Namespace': 'CWAgent',
                                'MetricName': 'mem_used_percent',
                                'Dimensions': [
                                    {'Name': 'InstanceId', 'Value': instance_id}
                                ]
                            },
                            'Period': 60,
                            'Stat': 'Average'
                        },
                        'ReturnData': True
                    }
                ],
                StartTime=start_time,
                EndTime=end_time
            )
            for result in response['MetricDataResults']:
                if result['Id'] == 'disk' and result['Values']:
                    metrics['disk_utilization'] = max(result['Values'])
                elif result['Id'] == 'mem' and result['Values']:
                    metrics['memory_utilization'] = max(result['Values'])
        except Exception as e:
            pass
        
        return metrics
    
    def predict_all_metrics(self, instance_id, current_metrics, instance_type):
        """Predict future values for ALL metrics"""
        predictions = {
            'cpu': None,
            'disk': None,
            'memory': None,
            'network_in': None
        }
        trends = {
            'cpu': 0,
            'disk': 0,
            'memory': 0
        }
        
        if not PREDICTION_CONFIG.get('enabled', True):
            return predictions, trends
        
        # CPU Prediction using ML model
        if self.predictor and current_metrics.get('cpu_utilization') is not None:
            now = datetime.now()
            df = pd.DataFrame([{
                'timestamp': now,
                'instance_id': instance_id,
                'instance_type': instance_type,
                'cpu_utilization': current_metrics['cpu_utilization'],
                'memory_utilization': current_metrics.get('memory_utilization') or 50.0,
                'disk_utilization': current_metrics.get('disk_utilization') or 50.0,
                'network_in_mb': (current_metrics.get('network_in') or 0) / 1000000,
                'network_out_mb': (current_metrics.get('network_out') or 0) / 1000000,
                'hour_of_day': now.hour,
                'day_of_week': now.weekday(),
                'is_business_hours': 1 if 9 <= now.hour <= 18 else 0,
                'is_weekend': 1 if now.weekday() >= 5 else 0
            }])
            
            df_features = self.fe.transform(df)
            result = self.predictor.predict_with_confidence(df_features)
            predictions['cpu'] = result['prediction'][0]
        
        # Calculate trends and predictions from history
        hours_ahead = PREDICTION_CONFIG.get('hours_ahead', 1)
        data_points = hours_ahead * 60 / MONITORING_CONFIG['check_interval_seconds']
        
        # CPU Trend
        cpu_history = self.metrics_tracker.cpu_history.get(instance_id, [])
        if len(cpu_history) >= 3:
            cpu_trend = np.mean(np.diff(cpu_history[-5:]))
            trends['cpu'] = cpu_trend
            # If no ML prediction, use trend-based prediction
            if predictions['cpu'] is None and cpu_trend > 0:
                predictions['cpu'] = (current_metrics.get('cpu_utilization') or 0) + (cpu_trend * data_points)
        
        # Disk Trend & Prediction
        disk_history = self.metrics_tracker.disk_history.get(instance_id, [])
        if len(disk_history) >= 3:
            disk_trend = np.mean(np.diff(disk_history[-5:]))
            trends['disk'] = disk_trend
            if current_metrics.get('disk_utilization') is not None:
                predictions['disk'] = max(0, min(100, 
                    current_metrics['disk_utilization'] + (disk_trend * data_points)))
        
        # Memory Trend & Prediction
        memory_history = self.metrics_tracker.memory_history.get(instance_id, [])
        if len(memory_history) >= 3:
            memory_trend = np.mean(np.diff(memory_history[-5:]))
            trends['memory'] = memory_trend
            if current_metrics.get('memory_utilization') is not None:
                predictions['memory'] = max(0, min(100,
                    current_metrics['memory_utilization'] + (memory_trend * data_points)))
        
        return predictions, trends
    
    def check_and_alert(self):
        """Main monitoring loop iteration"""
        print(f"\n{'='*70}")
        print(f"⏰ ASG CHECK: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'='*70}")
        
        # Refresh instance list
        self.refresh_instances()
        
        if not self.instances:
            print("   ⚠️ No instances to monitor")
            return
        
        # Get ASG info
        asg_info = self.discovery.get_asg_info()
        if asg_info:
            print(f"\n📦 ASG: {asg_info['name']}")
            print(f"   Capacity: {asg_info['instance_count']}/{asg_info['desired_capacity']} (min:{asg_info['min_size']}, max:{asg_info['max_size']})")
        
        # Collect metrics for all instances
        all_metrics = []
        all_alerts = []
        
        for instance_id, info in self.instances.items():
            print(f"\n{'─'*60}")
            print(f"🖥️  {info['name']} ({instance_id})")
            print(f"   AZ: {info['availability_zone']} | Type: {info['instance_type']}")
            
            # Get all metrics
            metrics = self.get_all_metrics(instance_id)
            
            if metrics['cpu_utilization'] is None:
                print(f"   ⚠️ Could not fetch metrics (instance may be initializing)")
                continue
            
            # Display current metrics
            print(f"\n   📊 CURRENT METRICS:")
            print(f"      CPU:     {metrics['cpu_utilization']:.2f}%")
            if metrics['disk_utilization'] is not None:
                print(f"      Disk:    {metrics['disk_utilization']:.2f}%")
            else:
                print(f"      Disk:    N/A (CloudWatch Agent required)")
            if metrics['memory_utilization'] is not None:
                print(f"      Memory:  {metrics['memory_utilization']:.2f}%")
            else:
                print(f"      Memory:  N/A (CloudWatch Agent required)")
            if metrics['network_in'] is not None:
                print(f"      Net In:  {metrics['network_in']/1000000:.2f} MB/s")
            if metrics['network_out'] is not None:
                print(f"      Net Out: {metrics['network_out']/1000000:.2f} MB/s")
            
            # Check for spikes (all metrics)
            spikes = self.metrics_tracker.check_all_spikes(instance_id, metrics)
            for spike in spikes:
                print(f"\n   {spike['message']}")
                spike['instance_name'] = info['name']
                all_alerts.append(spike)
            
            # Get predictions
            predictions, trends = self.predict_all_metrics(instance_id, metrics, info['instance_type'])
            
            if any(v is not None for v in predictions.values()):
                print(f"\n   🔮 PREDICTIONS ({PREDICTION_CONFIG.get('hours_ahead', 1)}h ahead):")
                if predictions['cpu'] is not None:
                    trend_arrow = "↑" if predictions['cpu'] > metrics['cpu_utilization'] else "↓"
                    print(f"      CPU:     {predictions['cpu']:.1f}% {trend_arrow}")
                if predictions['disk'] is not None:
                    trend_arrow = "↑" if predictions['disk'] > (metrics['disk_utilization'] or 0) else "↓"
                    print(f"      Disk:    {predictions['disk']:.1f}% {trend_arrow}")
                if predictions['memory'] is not None:
                    trend_arrow = "↑" if predictions['memory'] > (metrics['memory_utilization'] or 0) else "↓"
                    print(f"      Memory:  {predictions['memory']:.1f}% {trend_arrow}")
            
            # Check thresholds and predictions
            alerts = self.alert_sys.check(
                metrics,
                predicted_cpu=predictions['cpu'],
                predicted_disk=predictions['disk'],
                predicted_memory=predictions['memory'],
                trends=trends
            )
            
            for alert in alerts:
                alert['instance_id'] = instance_id
                alert['instance_name'] = info['name']
                all_alerts.append(alert)
            
            # Store for aggregate
            all_metrics.append({
                'instance_id': instance_id,
                'metrics': metrics,
                'predictions': predictions
            })
        
        # Aggregate metrics
        if all_metrics:
            cpu_values = [m['metrics']['cpu_utilization'] for m in all_metrics if m['metrics']['cpu_utilization']]
            
            if cpu_values:
                avg_cpu = np.mean(cpu_values)
                max_cpu = max(cpu_values)
                
                print(f"\n{'='*60}")
                print(f"📊 ASG AGGREGATE METRICS")
                print(f"{'='*60}")
                print(f"   Average CPU: {avg_cpu:.2f}%")
                print(f"   Max CPU: {max_cpu:.2f}%")
                print(f"   Instances monitored: {len(all_metrics)}")
                
                # Check aggregate thresholds
                if avg_cpu >= THRESHOLDS.get('asg_avg_cpu_critical', 75):
                    all_alerts.append({
                        'type': 'ASG_AVG_CPU_CRITICAL',
                        'metric': 'ASG_AVG_CPU',
                        'value': avg_cpu,
                        'severity': 'CRITICAL',
                        'send_email': True,
                        'message': f'🚨 ASG AVERAGE CPU CRITICAL: {avg_cpu:.1f}% across {len(all_metrics)} instances',
                        'action_required': 'Consider increasing ASG capacity or optimizing workload'
                    })
                elif avg_cpu >= THRESHOLDS.get('asg_avg_cpu_warning', 60):
                    all_alerts.append({
                        'type': 'ASG_AVG_CPU_WARNING',
                        'metric': 'ASG_AVG_CPU',
                        'value': avg_cpu,
                        'severity': 'WARNING',
                        'send_email': True,
                        'message': f'⚠️ ASG AVERAGE CPU WARNING: {avg_cpu:.1f}% across {len(all_metrics)} instances',
                        'action_required': 'Monitor closely, may need to scale soon'
                    })
        
        # Send alerts
        if all_alerts:
            print(f"\n🚨 {len(all_alerts)} ALERT(S) TRIGGERED!")
            self._send_all_alerts(all_alerts, all_metrics)
        else:
            print(f"\n✅ All instances healthy. No alerts.")
    
    def _send_all_alerts(self, alerts, all_metrics):
        """Send all alerts with instance details"""
        for alert in alerts:
            instance_info = None
            metrics = None
            
            # Find instance info and metrics for this alert
            for m in all_metrics:
                if m['instance_id'] == alert.get('instance_id'):
                    instance_info = self.instances.get(m['instance_id'])
                    metrics = m['metrics']
                    break
            
            self.alert_sys.send([alert], instance_info, metrics)
    
    def run_forever(self, interval_seconds=None):
        """Run continuous monitoring"""
        if interval_seconds is None:
            interval_seconds = MONITORING_CONFIG['check_interval_seconds']
        
        print("\n" + "="*70)
        print("🔄 STARTING ASG CONTINUOUS MONITORING")
        print("="*70)
        print(f"   ASG: {AUTOSCALING_CONFIG['asg_name']}")
        print(f"   Check interval: {interval_seconds} seconds")
        print(f"   Predictions: {'Enabled' if PREDICTION_CONFIG.get('enabled') else 'Disabled'}")
        print(f"\n   Thresholds:")
        print(f"      CPU Critical: {THRESHOLDS['cpu_critical']}%")
        print(f"      Disk Critical: {THRESHOLDS['disk_critical']}%")
        print(f"      Memory Critical: {THRESHOLDS.get('memory_critical', 95)}%")
        print(f"      CPU Spike: +{SPIKE_CONFIG['cpu_spike_threshold']}%")
        print(f"      Network Spike: +{SPIKE_CONFIG.get('network_spike_threshold', 50)}%")
        print(f"\n   Press Ctrl+C to stop")
        print("="*70)
        
        # Initial discovery
        self.refresh_instances(force=True)
        
        try:
            while True:
                self.check_and_alert()
                print(f"\n⏳ Next check in {interval_seconds} seconds...")
                time.sleep(interval_seconds)
        except KeyboardInterrupt:
            print("\n\n🛑 Monitoring stopped")


def main():
    print("\n" + "="*70)
    print("🔴 AUTO SCALING GROUP ML MONITORING")
    print("="*70)
    
    monitor = ASGMonitor()
    monitor.run_forever()


if __name__ == "__main__":
    main()
