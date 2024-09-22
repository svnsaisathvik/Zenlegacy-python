import discord
from discord.ext import commands
import boto3
import json
import datetime


from utils.aws_helpers import log_action, format_guardduty_findings

# Load AWS credentials
with open("config/aws_credentials.json", "r") as f:
    aws_credentials = json.load(f)
with open("config/bot_config.json", "r") as f:
    bot_cred = json.load(f)

# Initialize Boto3 clients for GuardDuty and CloudWatch
guardduty_client = boto3.client('guardduty',
                                aws_access_key_id=aws_credentials['aws_access_key'],
                                aws_secret_access_key=aws_credentials['aws_secret_key'],
                                region_name=aws_credentials['region'])

cloudwatch_client = boto3.client('cloudwatch',
                                 aws_access_key_id=aws_credentials['aws_access_key'],
                                 aws_secret_access_key=aws_credentials['aws_secret_key'],
                                 region_name=aws_credentials['region'])

# Discord bot setup
intents=discord.Intents.default()
intents.messages=True
intents.guilds=True

bot = commands.Bot(command_prefix="!",intents=intents)

@commands.command(name="monitor_threats")
async def monitor_threats(ctx):
    """Monitor AWS account for security threats using GuardDuty and CloudWatch."""
    try:
        # Check for GuardDuty threats
        findings = check_guardduty_threats()
        if not findings:
            await ctx.send("No GuardDuty threats detected.")
        else:
            formatted_findings = format_guardduty_findings(findings)
            await ctx.send(f"GuardDuty Threats Detected:\n{formatted_findings}")

        # Monitor CloudWatch metrics for unusual activity (e.g., sudden CPU usage spikes)
        metric_alerts = check_cloudwatch_metrics()
        if not metric_alerts:
            await ctx.send("No unusual activity detected in CloudWatch metrics.")
        else:
            await ctx.send(f"CloudWatch Alerts:\n{metric_alerts}")

        log_action(f"Threat monitoring performed by user {ctx.author.name}.")

    except Exception as e:
        await ctx.send(f"Error during threat monitoring: {str(e)}")

def check_guardduty_threats():
    """Fetch GuardDuty findings."""
    detector_ids = guardduty_client.list_detectors()['DetectorIds']
    if not detector_ids:
        return None
    
    detector_id = detector_ids[0]
    findings = guardduty_client.list_findings(DetectorId=detector_id)
    if not findings['FindingIds']:
        return None
    
    # Fetch details for each finding
    findings_details = guardduty_client.get_findings(
        DetectorId=detector_id,
        FindingIds=findings['FindingIds']
    )
    return findings_details['Findings']

def check_cloudwatch_metrics():
    """Check CloudWatch for unusual activity (e.g., sudden CPU spikes)."""
    # Example: Monitoring EC2 CPU Utilization for spikes
    metrics = cloudwatch_client.get_metric_statistics(
        Namespace='AWS/EC2',
        MetricName='CPUUtilization',
        StartTime=datetime.utcnow() ,
        EndTime=datetime.utcnow(),
        Period=300,
        Statistics=['Average'],
        Dimensions=[{'Name': 'InstanceId', 'Value': 'i-1234567890abcdef0'}]
    )

    alerts = []
    for data_point in metrics['Datapoints']:
        if data_point['Average'] > 80.0:  # Threshold for high CPU utilization
            alerts.append(f"High CPU Utilization: {data_point['Average']}% at {data_point['Timestamp']}")
    
    return alerts

bot.run(bot_cred['discord_token'])
