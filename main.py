import os
import discord
from discord.ext import commands
import requests
import random

# Load token from Render environment variables
TOKEN = os.getenv("DISCORD_TOKEN")
if not TOKEN:
    raise RuntimeError("❌ DISCORD_TOKEN not set in environment variables!")

# AI API Key (Gemini Pro)
API_KEY = "AIzaSyDtgKODGQeIGxNr2RSPQZJzF-Nh5k2KxFk"  
PREFIX = "!"

# Enable required intents
intents = discord.Intents.default()
intents.message_content = True  # Required for commands

bot = commands.Bot(
    command_prefix=PREFIX,
    intents=intents,
    help_command=None  # Disable default help command
)

# Cat-themed responses
CAT_RESPONSES = [
    "🐱 Meow! Let me think...",
    "🐾 Processing with my feline brain...",
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
        return "😿 Meow... something went wrong. Try again later!"

@bot.event
async def on_ready():
    print(f"✅ Bot is LIVE as {bot.user}!")
    await bot.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.watching,
            name=f"{len(bot.guilds)} servers | {PREFIX}help"
        )
    )

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
        description=response[:2000],  # Ensure it fits in Discord
        color=random_color()
    )
    await msg.edit(embed=embed)

@bot.command()
async def ping(ctx):
    """Check bot latency"""
    await ctx.send(f"🏓 Pong! {round(bot.latency * 1000)}ms")

@bot.command()
async def invite(ctx):
    """Get bot invite link"""
    invite_url = f"https://discord.com/oauth2/authorize?client_id={bot.user.id}&permissions=274877906944&scope=bot"
    embed = discord.Embed(
        title="🔗 Invite Me!",
        description=f"[Click Here]({invite_url})",
        color=random_color()
    )
    await ctx.send(embed=embed)

if __name__ == "__main__":
    print("🚀 Starting bot...")
    try:
        bot.run(TOKEN)
    except discord.LoginFailure:
        print("❌ Token rejected. Fix this:")
        print("1. Generate a NEW token in Discord Developer Portal")
        print("2. Update Render.com environment variables")
        print("3. Enable ALL intents (Presence, Server Members, Message Content)")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
