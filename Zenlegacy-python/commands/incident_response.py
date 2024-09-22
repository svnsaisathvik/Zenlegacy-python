import discord
from discord.ext import commands
from utils.gen_ai_helpers import ask_gpt

@commands.command(name="incident_resolution")
async def incident_resolution(ctx, incident_description: str):
    prompt = f"An incident occurred: {incident_description}. Suggest resolution steps."
    resolution_steps = ask_gpt(prompt)
    await ctx.send(f"Incident Resolution Recommendations: {resolution_steps}")
