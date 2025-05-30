import os
import discord
from discord.ext import commands
import requests
import random
import asyncio

# Verify token exists
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
if not DISCORD_TOKEN:
    raise RuntimeError("DISCORD_TOKEN environment variable not set")

API_KEY = os.getenv('AI_API_KEY', 'AIzaSyDtgKODGQeIGxNr2RSPQZJzF-Nh5k2KxFk')
PREFIX = '!'

# Initialize bot with required intents
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
    print(f'Successfully logged in as {bot.user}')
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
        bot.run(DISCORD_TOKEN)
    except discord.LoginFailure:
        print("Invalid Discord token. Please check your DISCORD_TOKEN environment variable.")
    except Exception as e:
        print(f"Failed to start bot: {e}")
