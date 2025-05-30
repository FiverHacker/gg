import os
import discord
from discord.ext import commands
import requests
import random
from flask import Flask, request
import threading

# Flask app for Render health check
app = Flask(__name__)

@app.route('/')
def health_check():
    return "🤖 Bot is running!", 200

# Discord Bot Setup
TOKEN = os.getenv("DISCORD_TOKEN", "YOUR_BOT_TOKEN_HERE")  # Fallback token
PREFIX = "!"

# Enable ALL intents
intents = discord.Intents.all()
bot = commands.Bot(command_prefix=PREFIX, intents=intents)

# Cat-themed AI responses
CAT_RESPONSES = [
    "🐱 Meow! Thinking...",
    "🐾 Processing with cat-like precision...",
    "😸 Consulting feline wisdom...",
    "Purrr... formulating response..."
]

def random_color():
    return discord.Color.from_rgb(
        random.randint(50, 200),
        random.randint(50, 200),
        random.randint(50, 200)
    )

async def call_ai(prompt):
    """Call the AI API"""
    api_url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent"
    params = {"key": "AIzaSyDtgKODGQeIGxNr2RSPQZJzF-Nh5k2KxFk"}
    
    try:
        response = requests.post(
            api_url,
            params=params,
            json={"contents": [{"parts": [{"text": prompt}]}]},
            timeout=10
        )
        data = response.json()
        return data['candidates'][0]['content']['parts'][0]['text']
    except Exception as e:
        print(f"⚠️ API Error: {e}")
        return "😿 Cat got my tongue! Try again later."

@bot.event
async def on_ready():
    print(f"✅ Bot is ONLINE as {bot.user}!")
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
    
    response = await call_ai(question)
    
    embed = discord.Embed(
        title="💡 AI Response",
        description=response[:2000],  # Discord character limit
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
    invite_url = f"https://discord.com/oauth2/authorize?client_id={bot.user.id}&permissions=8&scope=bot"
    await ctx.send(f"🔗 Invite me: {invite_url}")

def run_flask():
    """Run Flask server for Render health checks"""
    app.run(host='0.0.0.0', port=8080)

if __name__ == "__main__":
    # Start Flask in a separate thread
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.daemon = True
    flask_thread.start()
    
    print("🚀 Starting Discord bot...")
    try:
        bot.run(TOKEN)
    except discord.LoginFailure:
        print("❌ Invalid token! Get a new one from:")
        print("https://discord.com/developers/applications")
    except Exception as e:
        print(f"❌ Error: {e}")
