import discord
from discord.ext import commands
from utils.gen_ai_helpers import parse_command

@commands.command(name="gen_ai")
async def gen_ai_command(ctx, *, user_input: str):
    response = parse_command(user_input)
    await ctx.send(f"GPT Response: {response}")
