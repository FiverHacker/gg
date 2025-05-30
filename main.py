import os
import discord
from discord.ext import commands
import requests
import random
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get configuration from environment
TOKEN = os.environ.get('DISCORD_TOKEN')
if not TOKEN:
    raise ValueError("No DISCORD_TOKEN set in environment variables")

API_KEY = os.environ.get('AI_API_KEY', 'AIzaSyDtgKODGQeIGxNr2RSPQZJzF-Nh5k2KxFk')
PREFIX = '!'

# Initialize bot
intents = discord.Intents.default()
intents.message_content = True
intents.messages = True

bot = commands.Bot(
    command_prefix=PREFIX,
    intents=intents,
    help_command=None
)

# Cat-themed components
CAT_RESPONSES = [
    "Meow! Let me think about that...",
    "Purr... processing your request!",
    "🐾 One moment while I tap into my feline wisdom...",
    "Mrow! Interesting question...",
    "😸 Let me consult the ancient cat scriptures...",
    "Prrrrr... calculating the purrfect response..."
]

def random_rgb():
    return discord.Color.from_rgb(
        random.randint(0, 255),
        random.randint(0, 255),
        random.randint(0, 255)
    )

async def call_ai_studio(prompt):
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
        return "Meow... something went wrong with my cat-like processing."

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    await bot.change_presence(activity=discord.Game(name=f"{PREFIX}help | Watching {len(bot.guilds)} servers"))

@bot.command()
async def ask(ctx, *, question):
    """Ask the AI a question"""
    embed = discord.Embed(
        title="🐱 Cat AI Thinking...",
        description=random.choice(CAT_RESPONSES),
        color=random_rgb()
    )
    msg = await ctx.send(embed=embed)
    
    response = await call_ai_studio(question)
    
    embed = discord.Embed(
        title=f"🐾 Response to: {question[:100]}{'...' if len(question) > 100 else ''}",
        description=response,
        color=random_rgb()
    )
    await msg.edit(embed=embed)

@bot.command()
async def invite(ctx):
    """Get bot invite link"""
    embed = discord.Embed(
        title="Invite me to your server!",
        description=f"[Click here](https://discord.com/oauth2/authorize?client_id={bot.user.id}&permissions=534723951680&scope=bot)",
        color=random_rgb()
    )
    await ctx.send(embed=embed)

@bot.command()
async def help(ctx):
    """Show help message"""
    embed = discord.Embed(
        title="🐱 Cat AI Help",
        description="Here are my commands:",
        color=random_rgb()
    )
    embed.add_field(
        name=f"{PREFIX}ask [question]",
        value="Ask the AI anything",
        inline=False
    )
    embed.add_field(
        name=f"{PREFIX}invite",
        value="Get my invite link",
        inline=False
    )
    embed.add_field(
        name=f"{PREFIX}help",
        value="Show this message",
        inline=False
    )
    await ctx.send(embed=embed)

if __name__ == '__main__':
    print("Starting bot...")
    bot.run(TOKEN)
