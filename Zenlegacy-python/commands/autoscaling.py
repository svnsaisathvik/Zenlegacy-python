import discord
from discord.ext import commands
import boto3
import json
from utils.aws_helpers import get_current_instance_count, update_instance_count
from utils.logger import log_action


with open("config/aws_credentials.json", "r") as f:
    aws_credentials = json.load(f)

with open("config/thresholds.json", "r") as f:
    thresholds = json.load(f)

ec2 = boto3.client('ec2',
                   aws_access_key_id=aws_credentials['aws_access_key'],
                   aws_secret_access_key=aws_credentials['aws_secret_key'],
                   region_name=aws_credentials['region'])

@commands.command(name="scale_ec2")
async def scale_ec2(ctx, action: str, instance_type: str, count: int):
    if action not in ["up", "down"]:
        await ctx.send("Please specify 'up' or 'down' to scale EC2 instances.")
        return

    current_count = get_current_instance_count(instance_type)

    if action == "up":
        new_count = current_count + count
        await start_new_instances(ctx, instance_type, count)
        log_action(f"Scaled up {count} {instance_type} instances. New count: {new_count}")
    elif action == "down":
        if current_count > count:
            new_count = current_count - count
            await stop_instances(ctx, instance_type, count)
            log_action(f"Scaled down {count} {instance_type} instances. New count: {new_count}")
        else:
            await ctx.send(f"Cannot scale down below zero instances. Currently, there are {current_count} instances.")
            return

    update_instance_count(instance_type, new_count)
    await ctx.send(f"EC2 instances have been scaled {action}. New count: {new_count}.")

async def start_new_instances(ctx, instance_type, count):
    try:
        response = ec2.run_instances(
            ImageId="ami-0abcdef1234567890",  # Replace with your actual AMI ID
            InstanceType=instance_type,
            MinCount=count,
            MaxCount=count,
        )
        instance_ids = [instance['InstanceId'] for instance in response['Instances']]
        await ctx.send(f"Started {count} new {instance_type} instances: {', '.join(instance_ids)}")
    except Exception as e:
        await ctx.send(f"Error starting new instances: {str(e)}")

async def stop_instances(ctx, instance_type, count):
    try:
        instances = ec2.describe_instances(
            Filters=[
                {'Name': 'instance-type', 'Values': [instance_type]},
                {'Name': 'instance-state-name', 'Values': ['running']}
            ]
        )
        running_instances = [i['InstanceId'] for r in instances['Reservations'] for i in r['Instances']]
        
        if len(running_instances) < count:
            await ctx.send(f"Not enough instances to stop. Only {len(running_instances)} running instances found.")
            return
        
        instances_to_terminate = running_instances[:count]
        ec2.terminate_instances(InstanceIds=instances_to_terminate)
        await ctx.send(f"Terminated {count} {instance_type} instances: {', '.join(instances_to_terminate)}")
    except Exception as e:
        await ctx.send(f"Error stopping instances: {str(e)}")
