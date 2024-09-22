import boto3
import json
from datetime import datetime, timedelta
import logging

with open("config/aws_credentials.json", "r") as f:
    aws_credentials = json.load(f)

SUPPORTED_SERVICES = ["ec2", "s3", "rds", "dynamodb", "cost_explorer"]

def validate_service(service_name):
    """Validate if the service is supported."""
    if service_name not in SUPPORTED_SERVICES:
        raise ValueError(f"Unsupported service: {service_name}")

def get_service_client(service_name):
    """Get a Boto3 client for the specified AWS service."""
    validate_service(service_name)
    
    return boto3.client(service_name,
                        aws_access_key_id=aws_credentials['aws_access_key'],
                        aws_secret_access_key=aws_credentials['aws_secret_key'],
                        region_name=aws_credentials['region'])

def get_cost_for_service(service_name):
    """Retrieve the cost associated with a specific AWS service."""
    client = get_service_client("ce")  # Cost Explorer service

    # Define the time period for the cost query (last 30 days)
    end_date = datetime.now().date()
    start_date = (end_date - timedelta(days=30)).strftime('%Y-%m-%d')
    end_date = end_date.strftime('%Y-%m-%d')

    response = client.get_cost_and_usage(
        TimePeriod={
            'Start': start_date,
            'End': end_date
        },
        Granularity='MONTHLY',
        Metrics=['UnblendedCost'],
        Filter={
            'Dimensions': {
                'Key': 'SERVICE',
                'Values': [service_name.capitalize()]
            }
        }
    )

    if 'ResultsByTime' in response and response['ResultsByTime']:
        amount = response['ResultsByTime'][0]['Total']['UnblendedCost']['Amount']
        currency = response['ResultsByTime'][0]['Total']['UnblendedCost']['Unit']
        return f"{service_name}: {amount} {currency}"
    else:
        return f"{service_name}: No cost data found."

def format_guardduty_findings(findings):
    """Format GuardDuty findings for easier readability."""
    formatted_findings = ""
    for finding in findings:
        formatted_findings += (f"[{finding['Severity']}]: {finding['Title']} - {finding['Description']}\n"
                               f"Account: {finding['AccountId']}, Region: {finding['Region']}\n"
                               f"Threat: {finding['Service']['Action']['ActionType']}\n"
                               f"Resource: {finding['Resource']['ResourceType']} - {finding['Resource']['Id']}\n"
                               "------------------------------------------\n")
    return formatted_findings


def get_all_service_costs():
    """Retrieve the costs for all supported AWS services."""
    costs = []
    for service in SUPPORTED_SERVICES[:-1]:  # Skip "cost_explorer"
        cost = get_cost_for_service(service)
        costs.append(cost)
    return ", ".join(costs)

# New Functions for EC2, RDS, and DynamoDB instance management

def get_current_instance_count(service_name):
    """Get the current instance count for EC2, RDS, or DynamoDB."""
    validate_service(service_name)  # Validate before proceeding
    client = get_service_client(service_name)
    
    if service_name == "ec2":
        response = client.describe_instances()
        instances = [instance for reservation in response['Reservations'] for instance in reservation['Instances']]
        return len(instances), instances
    elif service_name == "rds":
        response = client.describe_db_instances()
        instances = response['DBInstances']
        return len(instances), instances
    elif service_name == "dynamodb":
        response = client.list_tables()
        tables = response['TableNames']
        return len(tables), tables
    else:
        raise ValueError(f"Unsupported service for instance count: {service_name}")

def update_instance_count(service_name, action, instance_identifier=None):
    """Update the instance count by starting, stopping, or terminating instances."""
    validate_service(service_name)  # Validate before proceeding
    client = get_service_client(service_name)
    
    if service_name == "ec2":
        if action == "start":
            client.start_instances(InstanceIds=[instance_identifier])
            return f"Started EC2 instance: {instance_identifier}"
        elif action == "stop":
            client.stop_instances(InstanceIds=[instance_identifier])
            return f"Stopped EC2 instance: {instance_identifier}"
        elif action == "terminate":
            client.terminate_instances(InstanceIds=[instance_identifier])
            return f"Terminated EC2 instance: {instance_identifier}"
        else:
            raise ValueError(f"Unsupported EC2 action: {action}")

    elif service_name == "rds":
        if action == "start":
            client.start_db_instance(DBInstanceIdentifier=instance_identifier)
            return f"Started RDS instance: {instance_identifier}"
        elif action == "stop":
            client.stop_db_instance(DBInstanceIdentifier=instance_identifier)
            return f"Stopped RDS instance: {instance_identifier}"
        elif action == "delete":
            client.delete_db_instance(DBInstanceIdentifier=instance_identifier, SkipFinalSnapshot=True)
            return f"Deleted RDS instance: {instance_identifier}"
        else:
            raise ValueError(f"Unsupported RDS action: {action}")

    elif service_name == "dynamodb":
        if action == "delete":
            client.delete_table(TableName=instance_identifier)
            return f"Deleted DynamoDB table: {instance_identifier}"
        else:
            raise ValueError(f"Unsupported DynamoDB action: {action}")

    else:
        raise ValueError(f"Unsupported service for instance management: {service_name}")

def log_action(action, service_name, details=None):
    """
    Log an action performed with a service.
    
    Parameters:
    - action (str): The action performed (e.g., 'start', 'stop', 'terminate').
    - service_name (str): The name of the AWS service (e.g., 'ec2', 'rds').
    - details (str, optional): Additional information about the action (e.g., instance ID).
    """
    if details:
        log_message = f"Action: {action} on Service: {service_name}, Details: {details}"
    else:
        log_message = f"Action: {action} on Service: {service_name}"

    # Log to both console and file
    logging.info(log_message)
    print(log_message)

