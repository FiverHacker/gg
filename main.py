import discord
from discord.ext import commands
import requests
import json
import random
from datetime import datetime
import asyncio

# Bot configuration
TOKEN = 'MTM3NzgwOTMyMzI2NjE1MDUyMQ.GcYc1e.56bZxP-mAoWN4eoUcMZEoFZrZguQJU4jcFOS2U'  # Replace with your bot token
API_KEY = 'AIzaSyDtgKODGQeIGxNr2RSPQZJzF-Nh5k2KxFk'  # AI Studio API key
PREFIX = '!'  # Bot prefix

# Initialize bot with intents
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True

bot = commands.Bot(command_prefix=PREFIX, intents=intents)

# Cat-themed responses
CAT_RESPONSES = [
    "Meow! Let me think about that...",
    "Purr... processing your request!",
    "🐾 One moment while I tap into my feline wisdom...",
    "Mrow! Interesting question...",
    "😸 Let me consult the ancient cat scriptures...",
    "Prrrrr... calculating the purrfect response..."
]

# RGB embed colors
def random_rgb():
    return discord.Color.from_rgb(
        random.randint(0, 255),
        random.randint(0, 255),
        random.randint(0, 255)
    )

# Call AI Studio API
async def call_ai_studio(prompt):
    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent"
    params = {"key": API_KEY}
    
    headers = {
        "Content-Type": "application/json"
    }
    
    data = {
        "contents": [{
            "parts": [{
                "text": prompt
            }]
        }]
    }
    
    try:
        response = requests.post(url, params=params, headers=headers, json=data)
        response.raise_for_status()
        result = response.json()
        
        if 'candidates' in result and result['candidates']:
            return result['candidates'][0]['content']['parts'][0]['text']
        else:
            return "Sorry, I couldn't generate a response. Maybe try a different question?"
    
    except Exception as e:
        print(f"API Error: {e}")
        return "Meow... something went wrong with the API. Maybe the servers are taking a cat nap?"

# Bot events
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} ({bot.user.id})')
    print('------')
    
    # Set custom status
    await bot.change_presence(activity=discord.Game(name="with yarn balls | !help"))

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        embed = discord.Embed(
            title="Command Not Found",
            description=f"Meow? I don't know that command. Try `{PREFIX}help` for available commands.",
            color=discord.Color.red()
        )
        await ctx.send(embed=embed)
    else:
        print(f"Error: {error}")

# Commands
@bot.command(name='ask', help='Ask the AI a question')
async def ask(ctx, *, question):
    # Send initial "thinking" message
    thinking_msg = random.choice(CAT_RESPONSES)
    thinking_embed = discord.Embed(
        title="🐱 Cat AI Thinking...",
        description=thinking_msg,
        color=random_rgb()
    )
    thinking_embed.set_footer(text=f"Requested by {ctx.author.display_name}", icon_url=ctx.author.avatar.url)
    
    message = await ctx.send(embed=thinking_embed)
    
    # Call the AI API
    response = await call_ai_studio(question)
    
    # Create response embed
    embed = discord.Embed(
        title=f"🐾 AI Response to: {question}",
        description=response,
        color=random_rgb(),
        timestamp=datetime.utcnow()
    )
    embed.set_author(name="Cat AI Assistant", icon_url=bot.user.avatar.url)
    embed.set_footer(text=f"Requested by {ctx.author.display_name}", icon_url=ctx.author.avatar.url)
    
    # Edit the original message with the response
    await message.edit(embed=embed)

@bot.command(name='catfact', help='Get a random cat fact')
async def catfact(ctx):
    facts = [
        "Cats have five toes on their front paws but only four on their back paws.",
        "A group of cats is called a clowder.",
        "Cats can rotate their ears 180 degrees.",
        "The oldest known pet cat existed 9,500 years ago.",
        "A cat's nose print is unique, much like a human's fingerprint.",
        "Cats spend 70% of their lives sleeping.",
        "Cats can't taste sweetness.",
        "A cat's purr may have healing properties for bones and organs.",
        "Cats have a special reflective layer in their eyes called the tapetum lucidum.",
        "The richest cat in the world had £7 million left to them in a will."
    ]
    
    embed = discord.Embed(
        title="🐱 Did You Know?",
        description=random.choice(facts),
        color=random_rgb()
    )
    embed.set_footer(text=f"Requested by {ctx.author.display_name}", icon_url=ctx.author.avatar.url)
    await ctx.send(embed=embed)

@bot.command(name='purr', help='Get a comforting cat message')
async def purr(ctx):
    comforts = [
        "Purrr... everything will be okay.",
        "You're doing great! *headbutts*",
        "Let me knead your worries away...",
        "You're loved more than catnip!",
        "Sending you warm purrs and head bonks.",
        "You're the cat's pajamas! 😸",
        "Remember: You've got nine lives worth of potential!",
        "*curls up beside you* I'm here for you."
    ]
    
    embed = discord.Embed(
        title="😻 Comforting Purrs",
        description=random.choice(comforts),
        color=random_rgb()
    )
    embed.set_footer(text=f"For {ctx.author.display_name}", icon_url=ctx.author.avatar.url)
    await ctx.send(embed=embed)

@bot.command(name='invite', help='Get the bot invite link')
async def invite(ctx):
    embed = discord.Embed(
        title="Invite Cat AI to Your Server!",
        description="[Click here to invite me!](https://discord.com/oauth2/authorize?client_id=YOUR_BOT_ID&permissions=274878032960&scope=bot)",
        color=random_rgb()
    )
    embed.set_footer(text="Meow! Thanks for inviting me!")
    await ctx.send(embed=embed)

# Run the bot
if __name__ == '__main__':
    bot.run(TOKEN)