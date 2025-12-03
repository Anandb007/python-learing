"""
Auto Scaling Group Instance Discovery
"""

import boto3
from datetime import datetime
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config_autoscaling import AUTOSCALING_CONFIG, AWS_REGION


class ASGDiscovery:
    def __init__(self):
        self.region = AWS_REGION
        self.asg_name = AUTOSCALING_CONFIG['asg_name']
        self.autoscaling = boto3.client('autoscaling', region_name=self.region)
        self.ec2 = boto3.client('ec2', region_name=self.region)
        self.instances = {}
        self.last_discovery = None
    
    def discover_instances(self):
        print(f"\n🔍 Discovering instances in ASG: {self.asg_name}")
        
        try:
            response = self.autoscaling.describe_auto_scaling_groups(
                AutoScalingGroupNames=[self.asg_name]
            )
            
            if not response['AutoScalingGroups']:
                print(f"   ❌ ASG '{self.asg_name}' not found!")
                return {}
            
            asg = response['AutoScalingGroups'][0]
            
            instance_ids = [
                inst['InstanceId'] 
                for inst in asg['Instances'] 
                if inst['LifecycleState'] == 'InService'
            ]
            
            if not instance_ids:
                print("   ⚠️ No InService instances found")
                return {}
            
            ec2_response = self.ec2.describe_instances(InstanceIds=instance_ids)
            
            instances = {}
            for reservation in ec2_response['Reservations']:
                for instance in reservation['Instances']:
                    if instance['State']['Name'] == 'running':
                        inst_id = instance['InstanceId']
                        name = next(
                            (t['Value'] for t in instance.get('Tags', []) if t['Key'] == 'Name'),
                            f"ASG-{inst_id[-8:]}"
                        )
                        
                        instances[inst_id] = {
                            'instance_id': inst_id,
                            'instance_type': instance['InstanceType'],
                            'name': name,
                            'public_ip': instance.get('PublicIpAddress', 'N/A'),
                            'private_ip': instance.get('PrivateIpAddress', 'N/A'),
                            'availability_zone': instance['Placement']['AvailabilityZone'],
                            'launch_time': instance['LaunchTime'].isoformat(),
                            'state': instance['State']['Name']
                        }
            
            self.instances = instances
            self.last_discovery = datetime.now()
            
            print(f"   ✅ Found {len(instances)} running instances:")
            for inst_id, info in instances.items():
                print(f"      • {info['name']} ({inst_id}) - {info['availability_zone']}")
            
            return instances
            
        except Exception as e:
            print(f"   ❌ Discovery error: {e}")
            return {}
    
    def get_asg_info(self):
        try:
            response = self.autoscaling.describe_auto_scaling_groups(
                AutoScalingGroupNames=[self.asg_name]
            )
            
            if response['AutoScalingGroups']:
                asg = response['AutoScalingGroups'][0]
                return {
                    'name': asg['AutoScalingGroupName'],
                    'desired_capacity': asg['DesiredCapacity'],
                    'min_size': asg['MinSize'],
                    'max_size': asg['MaxSize'],
                    'instance_count': len([i for i in asg['Instances'] if i['LifecycleState'] == 'InService']),
                    'health_check_type': asg['HealthCheckType'],
                    'availability_zones': asg['AvailabilityZones']
                }
            return None
        except Exception as e:
            print(f"   ❌ Error getting ASG info: {e}")
            return None


if __name__ == "__main__":
    print("\n" + "="*60)
    print("🔍 AUTO SCALING GROUP DISCOVERY TEST")
    print("="*60)
    
    discovery = ASGDiscovery()
    
    asg_info = discovery.get_asg_info()
    if asg_info:
        print(f"\n📊 ASG Info:")
        print(f"   Name: {asg_info['name']}")
        print(f"   Desired: {asg_info['desired_capacity']}")
        print(f"   Min/Max: {asg_info['min_size']}/{asg_info['max_size']}")
        print(f"   Current: {asg_info['instance_count']} instances")
    
    instances = discovery.discover_instances()
