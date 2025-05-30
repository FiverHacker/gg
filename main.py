import os
import discord
from discord.ext import commands
import requests
import random
from flask import Flask
import threading

# ======================
# FLASK SERVER FOR RENDER HEALTH CHECKS
# ======================
app = Flask(__name__)

@app.route('/')
def health_check():
    return "🤖 Bot is online and healthy!", 200

def run_flask():
    app.run(host='0.0.0.0', port=8080)

# ======================
# DISCORD BOT SETUP
# ======================
TOKEN = os.getenv("DISCORD_TOKEN")  # Get from Render environment
if not TOKEN:
    raise ValueError("❌ Missing DISCORD_TOKEN in environment variables")

# Enable ALL required intents
intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

# ======================
# BOT FUNCTIONALITY
# ======================
@bot.event
async def on_ready():
    print(f"✅ Bot is ONLINE as {bot.user}!")
    await bot.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.watching,
            name=f"!help in {len(bot.guilds)} servers"
        )
    )

@bot.command()
async def ping(ctx):
    """Check bot latency"""
    await ctx.send(f"🏓 Pong! {round(bot.latency * 1000)}ms")

@bot.command()
async def ask(ctx, *, question):
    """Ask the AI anything"""
    response = f"🤖 You asked: {question}\n(Implement your AI logic here)"
    await ctx.send(response)

# ======================
# START APPLICATION
# ======================
if __name__ == "__main__":
    # Start Flask server in background
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.daemon = True
    flask_thread.start()
    
    print("🚀 Starting Discord bot...")
    try:
        bot.run(TOKEN)
    except discord.LoginFailure:
        print("❌ Token invalid. Follow these steps:")
        print("1. Go to https://discord.com/developers/applications")
        print("2. Reset your bot token")
        print("3. Update the token in Render.com environment variables")
        print("4. Redeploy")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
