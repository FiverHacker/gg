import os
import discord
from discord.ext import commands
import requests
import random
import asyncio

# Configuration - using Render's environment variables
DISCORD_TOKEN = os.environ.get('DISCORD_TOKEN')
if not DISCORD_TOKEN:
    raise RuntimeError("❌ DISCORD_TOKEN environment variable not set - please configure in Render.com settings")

API_KEY = os.environ.get('AI_API_KEY', 'AIzaSyDtgKODGQeIGxNr2RSPQZJzF-Nh5k2KxFk')
PREFIX = '!'

# Initialize bot with required intents
intents = discord.Intents.default()
intents.message_content = True  # Required for message content

bot = commands.Bot(
    command_prefix=PREFIX,
    intents=intents,
    help_command=None
)

# Cat-themed responses
CAT_RESPONSES = [
    "🐱 Meow! Let me think about that...", 
    "🐾 Processing your request with my feline brain...",
    "😸 Consulting the cat hivemind...",
    "Purrr... generating response..."
]

def random_color():
    return discord.Color.from_rgb(
        random.randint(50, 200),
        random.randint(50, 200), 
        random.randint(50, 200)
    )

async def call_ai_api(prompt):
    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent"
    params = {"key": API_KEY}
    
    try:
        response = requests.post(
            url,
            params=params,
            json={"contents": [{"parts": [{"text": prompt}]}]},
            timeout=10
        )
        response.raise_for_status()
        data = response.json()
        return data['candidates'][0]['content']['parts'][0]['text']
    except Exception as e:
        print(f"API Error: {e}")
        return "😿 Meow... something went wrong. Please try again later."

@bot.event
async def on_ready():
    print(f'✅ Successfully logged in as {bot.user} (ID: {bot.user.id})')
    activity = discord.Activity(
        type=discord.ActivityType.listening,
        name=f"{PREFIX}help in {len(bot.guilds)} servers"
    )
    await bot.change_presence(activity=activity)

@bot.command()
async def ask(ctx, *, question):
    """Ask the AI anything"""
    embed = discord.Embed(
        title=random.choice(CAT_RESPONSES),
        color=random_color()
    )
    msg = await ctx.send(embed=embed)
    
    response = await call_ai_api(question)
    
    embed = discord.Embed(
        title="🐾 AI Response",
        description=response,
        color=random_color()
    )
    await msg.edit(embed=embed)

@bot.command()
async def ping(ctx):
    """Check if bot is alive"""
    await ctx.send(f"🐱 Pong! Latency: {round(bot.latency * 1000)}ms")

if __name__ == '__main__':
    print("🚀 Starting bot...")
    try:
        bot.run(DISCORD_TOKEN)
    except discord.LoginFailure:
        print("❌ Invalid Discord token. Please verify:")
        print("1. You copied the ENTIRE token correctly")
        print("2. The token is set in Render.com environment variables")
        print("3. The token hasn't been reset on Discord Developer Portal")
    except Exception as e:
        print(f"❌ Failed to start bot: {e}")
