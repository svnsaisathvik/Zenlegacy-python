import discord
from discord.ext import commands
import boto3
import json
from utils.aws_helpers import validate_service, get_service_client
from utils.logger import log_action


with open("config/aws_credentials.json", "r") as f:
    aws_credentials = json.load(f)
with open("config/bot_config.json", "r") as f:
    bot_cred = json.load(f)

intents=discord.Intents.default()
intents.messages=True
intents.guilds=True

bot = commands.Bot(command_prefix="!",intents=intents)

@bot.command(name="manage_service")
async def manage_service(ctx, service_name: str, action: str, *args):
    """Dynamically manage different AWS services based on user input."""
    if not validate_service(service_name):
        await ctx.send(f"Unsupported AWS service: {service_name}")
        return
    
    service_client = get_service_client(service_name)

    if service_name == "ec2":
        await manage_ec2(ctx, service_client, action, *args)
    elif service_name == "s3":
        await manage_s3(ctx, service_client, action, *args)
    elif service_name == "rds":
        await manage_rds(ctx, service_client, action, *args)  
    elif service_name == "dynamodb":
        await manage_dynamodb(ctx, service_client, action, *args)  
    else:
        await ctx.send(f"Service {service_name} is not yet supported.")
    
    log_action(f"User requested {action} on {service_name} with args: {args}")

async def manage_ec2(ctx, client, action, *args):
    if action == "start":
        instance_id = args[0]
        client.start_instances(InstanceIds=[instance_id])
        await ctx.send(f"EC2 Instance {instance_id} started.")
    elif action == "stop":
        instance_id = args[0]
        client.stop_instances(InstanceIds=[instance_id])
        await ctx.send(f"EC2 Instance {instance_id} stopped.")
    elif action == "describe":
        response = client.describe_instances()
        await ctx.send(f"EC2 Instances: {response}")
    else:
        await ctx.send(f"Invalid EC2 action: {action}")

#  logic for managing S3
async def manage_s3(ctx, client, action, *args):
    if action == "create_bucket":
        bucket_name = args[0]
        client.create_bucket(Bucket=bucket_name)
        await ctx.send(f"S3 bucket {bucket_name} created.")
    elif action == "delete_bucket":
        bucket_name = args[0]
        client.delete_bucket(Bucket=bucket_name)
        await ctx.send(f"S3 bucket {bucket_name} deleted.")
    elif action == "list_buckets":
        response = client.list_buckets()
        buckets = [bucket["Name"] for bucket in response["Buckets"]]
        await ctx.send(f"S3 Buckets: {buckets}")
    else:
        await ctx.send(f"Invalid S3 action: {action}")

# Logic for managing RDS
async def manage_rds(ctx, client, action, *args):
    if action == "start_db_instance":
        db_instance_id = args[0]
        client.start_db_instance(DBInstanceIdentifier=db_instance_id)
        await ctx.send(f"RDS Instance {db_instance_id} started.")
    elif action == "stop_db_instance":
        db_instance_id = args[0]
        client.stop_db_instance(DBInstanceIdentifier=db_instance_id)
        await ctx.send(f"RDS Instance {db_instance_id} stopped.")
    elif action == "describe_db_instances":
        response = client.describe_db_instances()
        await ctx.send(f"RDS Instances: {response}")
    else:
        await ctx.send(f"Invalid RDS action: {action}")

# Logic for managing DynamoDB
async def manage_dynamodb(ctx, client, action, *args):
    if action == "create_table":
        table_name = args[0]
        attribute_definitions = [
            {"AttributeName": "id", "AttributeType": "S"}  
        ]
        key_schema = [
            {"AttributeName": "id", "KeyType": "HASH"} 
        ]
        client.create_table(
            TableName=table_name,
            AttributeDefinitions=attribute_definitions,
            KeySchema=key_schema,
            ProvisionedThroughput={"ReadCapacityUnits": 5, "WriteCapacityUnits": 5}
        )
        await ctx.send(f"DynamoDB table {table_name} created.")
    elif action == "delete_table":
        table_name = args[0]
        client.delete_table(TableName=table_name)
        await ctx.send(f"DynamoDB table {table_name} deleted.")
    elif action == "list_tables":
        response = client.list_tables()
        await ctx.send(f"DynamoDB Tables: {response['TableNames']}")
    else:
        await ctx.send(f"Invalid DynamoDB action: {action}")

bot.run(bot_cred['discord_token'])
