from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
from azure.cognitiveservices.vision.computervision.models import VisualFeatureTypes
from msrest.authentication import CognitiveServicesCredentials
from array import array
import os
from PIL import Image
import sys
import time
import string
import discord
import random
from discord import message
from discord.ext import commands
import logging
import requests, uuid, json

subscription_key_tr = "e71b25336aa5490d9b9a169740cabe9f"
endpoint_tr = "https://api.cognitive.microsofttranslator.com/"
location = "southcentralus"
subscription_key = "95230f00389c4bab9d4353479ebdebda"
endpoint = "https://southcentralus.api.cognitive.microsoft.com/"
path = '/translate'

computervision_client = ComputerVisionClient(endpoint, CognitiveServicesCredentials(subscription_key))


logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

token = 'ODYyMTMxMzMxNTgwMDM1MTA0.YOT4Xw.6dMA-oH4YHf4g6i2q-1XSiNXLCE'


description = '''yes'''

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix='s!', description=description, intents=intents)




@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game(name="Reading texts!"))
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

#@bot.command(description='For when you wanna settle the score some other way')
#async def choose(ctx, *choices: str):
    #"""Chooses between multiple choices."""
    #await ctx.send(random.choice(choices))

#@bot.command()
#async def repeat(ctx, times: int, content='repeating...'):
    #"""Repeats a message multiple times."""
    #for i in range(times):
        #await ctx.send(content)

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
  """Sends random discord's tags"""
  discim = []
  for i in range(10):
   int = random.randint(0,9)
   int1 = random.randint(0,9)
   int2 = random.randint(0,9)
   int3 = random.randint(0,9)
   name = (f"{random.choice(string.ascii_lowercase)}{random.choice(string.ascii_lowercase)}{random.choice(string.ascii_lowercase)}{random.choice(string.ascii_lowercase)}")
   discim.append(f"{name}#{int}{int1}{int2}{int3}")
   await ctx.send('\n'.join(discim))


@bot.command()
async def nitro(ctx):
    """Sends random discord nitro gift (most of them doesnt really work at all)"""
    code = ''.join(random.choices(string.ascii_letters + string.digits, k=16))
    await ctx.send(f'https://discord.gift/{code}')

@bot.command()
async def text(ctx, read_image_url: str):
    """Reads the image you sent and sends back the information."""
    read_response = computervision_client.read(read_image_url,  raw=True)
    read_operation_location = read_response.headers["Operation-Location"]
    operation_id = read_operation_location.split("/")[-1]

    while True:
        read_result = computervision_client.get_read_result(operation_id)
        if read_result.status not in ['notStarted', 'running']:
            break
        time.sleep(1)

    if read_result.status == OperationStatusCodes.succeeded:
        for text_result in read_result.analyze_result.read_results:
                textresults = [line.text for line in text_result.lines]
               # await ctx.send(line.text)
               # await ctx.send(line.bounding_box)
                embed = discord.Embed(title='Text from image.', description = " ".join(textresults), color = 0xFF5733)
               # embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
                embed.set_author(name='Solane', icon_url='https://cdn.discordapp.com/avatars/862131331580035104/a432b7691eb218ffe11d54f174d8889c.png?size=1024')
                embed.set_footer(text="Command executed by: {}".format(ctx.author.display_name))
                await ctx.send(embed=embed)

@bot.command()
async def translate(ctx, lang1: str, lang2: str, text_tr: str):
    """Translate the text"""
    params = {
        'api-version': '3.0',
        'from': lang1,
        'to': [lang2, 'en']
    }
    constructed_url = endpoint_tr + path

    headers = {
        'Ocp-Apim-Subscription-Key': subscription_key_tr,
        'Ocp-Apim-Subscription-Region': location,
        'Content-type': 'application/json',
        'X-ClientTraceId': str(uuid.uuid4())
    }

    # You can pass more than one object in body.
    body = [{
        'text': text_tr
    }]

    request = requests.post(constructed_url, params=params, headers=headers, json=body)
    response = request.json()

    #print(json.dumps(response, sort_keys=True, ensure_ascii=False, indent=4, separators=(',', ': ')))
    await ctx.send('```'+json.dumps(response, sort_keys=True, ensure_ascii=False, indent=4, separators=(',', ': '))+'```')
    #await ctx.send(json.dumps(response, sort_keys=False, ensure_ascii=True))

@bot.command()
async def imagetr(ctx, lang1: str, lang2:str, read_image_url_tr: str):
    """translates text from images (idk if this will work help)"""
    read_response = computervision_client.read(read_image_url_tr,  raw=True)
    read_operation_location = read_response.headers["Operation-Location"]
    operation_id = read_operation_location.split("/")[-1]

    while True:
        read_result = computervision_client.get_read_result(operation_id)
        if read_result.status not in ['notStarted', 'running']:
            break
        time.sleep(1)
    await ctx.send('working?')

    if read_result.status == OperationStatusCodes.succeeded:
        for text_result in read_result.analyze_result.read_results:
            textresults = [line.text for line in text_result.lines]
            for line in text_result.lines:
                print(line.text)
                #print(line.bounding_box)
                
    

                params = {
                    'api-version': '3.0',
                    'from': lang1,
                    'to': [lang2, 'it']
                        }
    constructed_url = endpoint_tr + path

    headers = {
        'Ocp-Apim-Subscription-Key': subscription_key_tr,
        'Ocp-Apim-Subscription-Region': location,
        'Content-type': 'application/json',
        'X-ClientTraceId': str(uuid.uuid4())
    }

    # You can pass more than one object in body.
    body = [{
        'text': line.text
    }]

    request = requests.post(constructed_url, params=params, headers=headers, json=body)
    response = request.json()

    print(json.dumps(response, sort_keys=True, ensure_ascii=False, indent=4, separators=(',', ': ')))
    #await ctx.send('```'+json.dumps(response, sort_keys=True, ensure_ascii=False, indent=4, separators=(',', ': '))+'```')
    #await ctx.send(json.dumps(response, sort_keys=False, ensure_ascii=True))
    tr_results = [json.dumps(response, sort_keys=True, ensure_ascii=False, indent=4, separators=(',', ': '))]
    embed = discord.Embed(title='Translate', description = " ".join(tr_results), color = 0xFF5733)
               # embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
    embed.set_author(name='Solane', icon_url='https://cdn.discordapp.com/avatars/862131331580035104/a432b7691eb218ffe11d54f174d8889c.png?size=1024')
    embed.set_footer(text="Command executed by: {}".format(ctx.author.display_name))
    await ctx.send(embed=embed)

    

print()
bot.run(token)




