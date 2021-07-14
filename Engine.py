

import string
import discord
import random
from discord import message
from discord.ext import commands

token = ' '


description = '''yes'''

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix='!', description=description, intents=intents)


@bot.event
async def on_ready():
    print("-----------------------------------------------")
    print("[!] Iniciando seccion como: ", bot.user.name)
    print("[!] ID: ", bot.user.id)
    print("-----------------------------------------------")

@bot.command()
async def add(ctx, left: int, right: int):
    try: 
        await ctx.send(left + right)
    except Exception:
        left = ""
        await ctx.send("necesitas dar 2 numeros para la suma")
        return

@bot.command()
async def roll(ctx, dice: str):
    """Rolls a dice in NdN format."""
    try:
        rolls, limit = map(int, dice.split('d'))
    except Exception:
        await ctx.send('Format has to be in NdN!')
        return

    result = ', '.join(str(random.randint(1, limit)) for r in range(rolls))
    await ctx.send(result)

@bot.command(description='For when you wanna settle the score some other way')
async def choose(ctx, *choices: str):
    """Chooses between multiple choices."""
    await ctx.send(random.choice(choices))

@bot.command()
async def repeat(ctx, times: int, content='repeating...'):
    """Repeats a message multiple times."""
    for i in range(times):
        await ctx.send(content)

@bot.command()
async def joined(ctx, member: discord.Member):
    """Says when a member joined."""
    await ctx.send('{0.name} joined in {0.joined_at}'.format(member))

@bot.group()
async def cool(ctx):
    """Says if a user is cool.
    In reality this just checks if a subcommand is being invoked.
    """
    if ctx.invoked_subcommand is None:
        await ctx.send('No, {0.subcommand_passed} is not cool'.format(ctx))

@cool.command(name='bot')
async def _bot(ctx):
    """Is the bot cool?"""
    await ctx.send('Yes, the bot is cool.')


@bot.command()
async def test(ctx):
  for i in range(10):
   int = random.randint(0,9)
   int1 = random.randint(0,9)
   int2 = random.randint(0,9)
   int3 = random.randint(0,9)
   name = (f"{random.choice(string.ascii_lowercase)}{random.choice(string.ascii_lowercase)}{random.choice(string.ascii_lowercase)}{random.choice(string.ascii_lowercase)}")
   await ctx.send(f"{name}#{int}{int1}{int2}{int3}")
  
@bot.command()
async def nitro(ctx):
    code = ''.join(random.choices(string.ascii_letters + string.digits, k=16))
    await ctx.send(f'https://discord.gift/{code}')


bot.run(token)



