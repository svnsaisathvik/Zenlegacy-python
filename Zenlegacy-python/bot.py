import discord
from discord.ext import commands
import json
from commands import autoscaling, cost_monitoring, incident_response, security, aws_services, threat_monitoring, gen_ai

# Load bot credentials
with open("config/bot_config.json", "r") as f:
    bot_cred = json.load(f)

# Set up intents
intents = discord.Intents.default()
intents.message_content = True  # Required to read message content

# Set up bot with command prefix and help command
bot = commands.Bot(command_prefix="!", intents=intents, help_command=commands.DefaultHelpCommand(no_category='Available Commands'))

@bot.event
async def on_ready():
    print(f'🤖 Bot {bot.user.name} has connected to Discord! 🎉')

# Custom help command
@bot.command(name='help', help="Show all commands available")
async def custom_help(ctx):
    embed = discord.Embed(title="Available Commands 🛠", description="Here are the commands you can use with the bot:", color=discord.Color.blue())
    embed.add_field(name="🚀 EC2 Autoscaling", value="!scale_ec2 [up/down] [instances] - Scale EC2 instances", inline=False)
    embed.add_field(name="💰 Cost Optimization", value="!optimize_costs - Get cost optimization suggestions", inline=False)
    embed.add_field(name="🛡 Incident Response", value="!incident_resolution [incident_id] - Resolve AWS incidents", inline=False)
    embed.add_field(name="🔐 IAM Management", value="!manage_iam [action] [role_name] - Manage IAM roles", inline=False)
    embed.add_field(name="🛠 AWS Service Management", value="!manage_service [service_name] [action] [args] - Manage AWS services (EC2, S3, RDS, DynamoDB)", inline=False)
    embed.add_field(name="🛡 Threat Monitoring", value="!monitor_threats - Monitor AWS threats", inline=False)
    embed.add_field(name="🤖 Gen AI Integration", value="!gen_ai [question] - Ask the AI for any AWS-related tasks", inline=False)
    embed.set_footer(text="Use the commands wisely! 😊")
    await ctx.send(embed=embed)

# Load autoscaling command
@bot.command(name="scale_ec2", help="🚀 Scale EC2 instances up or down")
async def scale_ec2(ctx, direction: str, instances: int):
    try:
        print(f'Command scale_ec2 called with direction: {direction}, instances: {instances}')
        await autoscaling.scale_ec2(ctx, direction, instances)
    except Exception as e:
        await ctx.send(f"An error occurred: {str(e)}")
        print(f"Error in scale_ec2: {e}")

# Load cost monitoring command
@bot.command(name="optimize_costs", help="💰 Get cost optimization suggestions")
async def optimize_costs(ctx):
    try:
        await cost_monitoring.optimize_costs(ctx)
    except Exception as e:
        await ctx.send(f"An error occurred: {str(e)}")
        print(f"Error in optimize_costs: {e}")

# Load incident response command
@bot.command(name="incident_resolution", help="🛡 Resolve incidents in AWS")
async def incident_resolution(ctx, incident_id: str):
    try:
        await incident_response.incident_resolution(ctx, incident_id)
    except Exception as e:
        await ctx.send(f"An error occurred: {str(e)}")
        print(f"Error in incident_resolution: {e}")

# Load IAM management command
@bot.command(name="manage_iam", help="🔐 Manage IAM roles and permissions")
async def manage_iam(ctx, action: str, role_name: str):
    try:
        await security.manage_iam(ctx, action, role_name)
    except Exception as e:
        await ctx.send(f"An error occurred: {str(e)}")
        print(f"Error in manage_iam: {e}")

# Load AWS service management command
@bot.command(name="manage_service", help="🛠 Manage AWS services like EC2, S3, RDS, and DynamoDB")
async def manage_service(ctx, service_name: str, action: str, *args):
    try:
        await aws_services.manage_service(ctx, service_name, action, *args)
    except Exception as e:
        await ctx.send(f"An error occurred: {str(e)}")
        print(f"Error in manage_service: {e}")

# Load threat monitoring command
@bot.command(name="monitor_threats", help="🛡 Monitor AWS threats")
async def monitor_threats(ctx):
    try:
        await threat_monitoring.monitor_threats(ctx)
    except Exception as e:
        await ctx.send(f"An error occurred: {str(e)}")
        print(f"Error in monitor_threats: {e}")

# Load Gen AI command
@bot.command(name="gen_ai")
async def gen_ai_command(ctx, *query):
    try:
        await gen_ai.gen_ai_command(ctx, ' '.join(query))
    except Exception as e:
        await ctx.send(f"An error occurred: {str(e)}")
        print(f"Error in gen_ai_command: {e}")

# Start the bot
bot.run(bot_cred['discord_token'])