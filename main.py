import os
import discord
from discord.ext import commands
import requests
import random
from datetime import datetime

# Configuration
TOKEN = os.environ['DISCORD_TOKEN']  # Will raise error if not set
API_KEY = os.environ.get('AI_API_KEY', 'AIzaSyDtgKODGQeIGxNr2RSPQZJzF-Nh5k2KxFk')
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
CAT_THINKING = [
    "🐱 Meow! Let me think...",
    "🐾 Processing with my cat brain...",
    "😸 Consulting the feline hivemind...",
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
            timeout=15
        )
        response.raise_for_status()
        data = response.json()
        return data['candidates'][0]['content']['parts'][0]['text']
    except Exception as e:
        print(f"API Error: {e}")
        return "😿 Meow... something went wrong. Please try again later."

@bot.event
async def on_ready():
    print(f'Successfully logged in as {bot.user}')
    await bot.change_presence(activity=discord.Activity(
        type=discord.ActivityType.watching,
        name=f"{len(bot.guilds)} servers | {PREFIX}help"
    ))

@bot.command()
async def ask(ctx, *, question):
    """Ask the AI anything"""
    thinking = random.choice(CAT_THINKING)
    embed = discord.Embed(
        title=thinking,
        color=random_color()
    )
    msg = await ctx.send(embed=embed)
    
    response = await call_ai_api(question)
    
    embed = discord.Embed(
        title=f"🐾 AI Response",
        description=response,
        color=random_color()
    )
    embed.set_footer(text=f"Requested by {ctx.author.display_name}")
    await msg.edit(embed=embed)

@bot.command()
async def invite(ctx):
    """Get bot invite link"""
    permissions = 274877906944  # Basic permissions
    invite_url = f"https://discord.com/oauth2/authorize?client_id={bot.user.id}&permissions={permissions}&scope=bot"
    
    embed = discord.Embed(
        title="Invite me to your server!",
        description=f"[Click here]({invite_url})",
        color=random_color()
    )
    await ctx.send(embed=embed)

@bot.command()
async def help(ctx):
    """Show help message"""
    embed = discord.Embed(
        title="🐱 Cat AI Help",
        description=f"Prefix: `{PREFIX}`",
        color=random_color()
    )
    commands_list = [
        ("ask [question]", "Ask the AI anything"),
        ("invite", "Get bot invite link"),
        ("help", "Show this message")
    ]
    
    for name, value in commands_list:
        embed.add_field(name=f"`{PREFIX}{name}`", value=value, inline=False)
    
    await ctx.send(embed=embed)

if __name__ == '__main__':
    print("Starting bot...")
    try:
        bot.run(TOKEN)
    except Exception as e:
        print(f"Failed to start bot: {e}")
        raise
