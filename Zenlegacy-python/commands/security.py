import discord
from discord.ext import commands
import boto3
import json
from utils.aws_helpers import log_action

# Load AWS credentials
with open("config/aws_credentials.json", "r") as f:
    aws_credentials = json.load(f)
with open("config/bot_config.json", "r") as f:
    bot_cred = json.load(f)

# Initialize Boto3 IAM client
iam_client = boto3.client('iam',
                          aws_access_key_id=aws_credentials['aws_access_key'],
                          aws_secret_access_key=aws_credentials['aws_secret_key'],
                          region_name=aws_credentials['region'])

intents=discord.Intents.default()
intents.messages=True
intents.guilds=True
# Discord bot setup
bot = commands.Bot(command_prefix="!",intents=intents)

@commands.command(name="manage_iam")
async def manage_iam(ctx, action: str, role_name: str, policy_arn: str = None):
    """Manage IAM roles: create, attach policy, and delete."""
    try:
        if action == "create_role":
            await create_iam_role(ctx, role_name)
        elif action == "attach_policy":
            if policy_arn is None:
                await ctx.send("Please provide a policy ARN to attach.")
                return
            await attach_policy(ctx, role_name, policy_arn)
        elif action == "delete_role":
            await delete_iam_role(ctx, role_name)
        else:
            await ctx.send(f"Invalid action: {action}. Supported actions are: create_role, attach_policy, delete_role.")
        
        log_action(f"IAM action '{action}' performed on role '{role_name}' by user {ctx.author.name}.")
    except Exception as e:
        await ctx.send(f"Error managing IAM role: {str(e)}")

async def create_iam_role(ctx, role_name: str):
    """Create a new IAM role with a basic trust policy."""
    trust_policy = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Principal": {
                    "Service": "ec2.amazonaws.com"
                },
                "Action": "sts:AssumeRole"
            }
        ]
    }

    try:
        response = iam_client.create_role(
            RoleName=role_name,
            AssumeRolePolicyDocument=json.dumps(trust_policy),
            Description=f"Role for {role_name}"
        )
        await ctx.send(f"IAM Role '{role_name}' created successfully.")
    except Exception as e:
        await ctx.send(f"Failed to create IAM role: {str(e)}")

async def attach_policy(ctx, role_name: str, policy_arn: str):
    """Attach an AWS-managed or custom policy to a role."""
    try:
        iam_client.attach_role_policy(
            RoleName=role_name,
            PolicyArn=policy_arn
        )
        await ctx.send(f"Policy '{policy_arn}' attached to role '{role_name}'.")
    except Exception as e:
        await ctx.send(f"Failed to attach policy to role: {str(e)}")

async def delete_iam_role(ctx, role_name: str):
    """Delete an IAM role."""
    try:
        iam_client.delete_role(RoleName=role_name)
        await ctx.send(f"IAM Role '{role_name}' deleted successfully.")
    except Exception as e:
        await ctx.send(f"Failed to delete IAM role: {str(e)}")

bot.run(bot_cred['discord_token'])

