import os
import discord
from discord.ext import commands
import requests
import random
from flask import Flask

# Flask app for Render.com health check
app = Flask(__name__)

@app.route('/')
def home():
    return "Discord Bot is running", 200

# Discord Bot Configuration
TOKEN = os.getenv('DISCORD_TOKEN')
if not TOKEN:
    raise RuntimeError("DISCORD_TOKEN environment variable not set")

API_KEY = os.getenv('AI_API_KEY', 'AIzaSyDtgKODGQeIGxNr2RSPQZJzF-Nh5k2KxFk')
PREFIX = '!'

# Initialize bot
intents = discord.Intents.default()
intents.message_content = True

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
        type=discord.ActivityType.watching,
        name=f"{len(bot.guilds)} servers | {PREFIX}help"
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
        description=response[:2000],  # Discord has 2000 character limit
        color=random_color()
    )
    await msg.edit(embed=embed)

@bot.command()
async def ping(ctx):
    """Check bot latency"""
    await ctx.send(f'🏓 Pong! {round(bot.latency * 1000)}ms')

def run_flask():
    app.run(host='0.0.0.0', port=10000)

if __name__ == '__main__':
    import threading
    # Start Flask server in a separate thread
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.start()
    
    print("🚀 Starting bot...")
    try:
        bot.run(TOKEN)
    except discord.LoginFailure:
        print("❌ Invalid Discord token. Please verify:")
        print("1. You copied the ENTIRE token correctly")
        print("2. The token is set in Render.com environment variables")
        print("3. The token hasn't been reset on Discord Developer Portal")
    except Exception as e:
        print(f"❌ Failed to start bot: {e}")
