import discord
from discord.ext import commands
from utils.aws_helpers import get_cost_for_service, get_all_service_costs
from utils.gen_ai_helpers import ask_gpt
from utils.logger import log_action
import json
with open("config/bot_config.json", "r") as f:
    bot_cred = json.load(f)

intents=discord.Intents.default()
intents.messages=True
intents.guilds=True

bot = commands.Bot(command_prefix="!",intents=intents)


@commands.command(name="optimize_costs")
async def optimize_costs(ctx):
    """Fetch AWS cost data for all services and get cost optimization suggestions using GPT."""
    # Get cost data for all supported services
    cost_data = get_all_service_costs()
    
    # Log the cost retrieval action
    log_action(f"User requested cost optimizations. Costs: {cost_data}")
    print(cost_data)

    # Prepare the prompt for GPT
    prompt = f"Here is the AWS cost data: {cost_data}. Can you suggest optimizations?"
    
    # Get suggestions from GPT
    suggestions = ask_gpt(prompt)
    
    # Send the GPT's suggestions to the user
    await ctx.send(f"GPT Cost Optimizations: {suggestions}")

bot.run(bot_cred['discord_token'])


