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
import asyncio
import io
import glob
from urllib.parse import urlparse
from io import BytesIO
from PIL import Image, ImageDraw
from azure.cognitiveservices.vision.face import FaceClient
from msrest.authentication import CognitiveServicesCredentials
from azure.cognitiveservices.vision.face.models import TrainingStatusType, Person

subscription_key_tr = ""
endpoint_tr = ""
location = ""
subscription_key = ""
endpoint = ""
path = '/translate'
face_key = ""
face_end = ""

face_client = FaceClient(face_end, CognitiveServicesCredentials(face_key))
computervision_client = ComputerVisionClient(endpoint, CognitiveServicesCredentials(subscription_key))


logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

token = ''


description = '''Discord bot built in discord.py and made by Skultz.#2059'''

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix='s!', description=description, intents=intents)




@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game(name="Planning to destroy humanity!"))
    print("-----------------------------------------------")
    print("[!] Starting seccion: ", bot.user.name)
    print("[!] ID: ", bot.user.id)
    print("-----------------------------------------------")

#@bot.command()
#async def add(ctx, left: int, right: int):
    #try: 
        #await ctx.send(left + right)
    #except Exception:
        #left = ""
        #await ctx.send("necesitas dar 2 numeros para la suma")
        #return

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
    await ctx.send('Working')

    if read_result.status == OperationStatusCodes.succeeded:
        for text_result in read_result.analyze_result.read_results:
            textresults = [line.text for line in text_result.lines]
    
            params = {
                'api-version': '3.0',
                'from': lang1,
                'to': [lang2,]
                    }
    constructed_url = endpoint_tr + path

    headers = {
        'Ocp-Apim-Subscription-Key': subscription_key_tr,
        'Ocp-Apim-Subscription-Region': location,
        'Content-type': 'application/json',
        'X-ClientTraceId': str(uuid.uuid4())
    }

    body = [{
        'text': " ".join(textresults)
    }]

    request = requests.post(constructed_url, params=params, headers=headers, json=body)
    response = request.json()

    # print(json.dumps(response, sort_keys=True, ensure_ascii=False, indent=4, separators=(',', ': ')))
    #await ctx.send('```'+json.dumps(response, sort_keys=True, ensure_ascii=False, indent=4, separators=(',', ': '))+'```')
    #await ctx.send(json.dumps(response, sort_keys=False, ensure_ascii=True))
    tr_message = response[0]['translations'][0]['text']
    embed = discord.Embed(title=f'Translate: {lang1.upper()} to {lang2.upper()}', description =tr_message, color = 0xFF5733)
    embed.set_author(name='Solane', icon_url='https://cdn.discordapp.com/avatars/862131331580035104/a432b7691eb218ffe11d54f174d8889c.png?size=1024')
    embed.set_footer(text="Command executed by: {}".format(ctx.author.display_name))
    await ctx.send(embed=embed)
    
@bot.command()
async def yt(ctx):
    """random youtube link."""
    code = ''.join(random.choices(string.ascii_letters + string.digits, k=11))
    await ctx.send(f'https://www.youtube.com/watch?v={code}')


@bot.command()
async def detect(ctx, face_link: str):
    """detects a face from the link"""

    single_face_image_url = face_link
    single_image_name = os.path.basename(single_face_image_url)
    detected_faces = face_client.face.detect_with_url(url=single_face_image_url, detection_model='detection_03')
    if not detected_faces:
        embed2 = discord.Embed(title=f'No face detect from image: {single_image_name.upper()}',color = 0xFF5733)
        embed2.set_author(name='Solane', icon_url='https://cdn.discordapp.com/avatars/862131331580035104/a432b7691eb218ffe11d54f174d8889c.png?size=1024')
        embed2.set_footer(text="Command executed by: {}".format(ctx.author.display_name))
        await ctx.send(embed=embed2)
        raise Exception('No face detected from image {}'.format(single_image_name))

    print('Detected face ID from', single_image_name, ':')
    for face in detected_faces: print (face.face_id)
    print()

    face_response = face.face_id

    embed = discord.Embed(title=f'Face detected on: {single_image_name.upper()}', description =face_response, color = 0xFF5733)
    embed.set_author(name='Solane', icon_url='https://cdn.discordapp.com/avatars/862131331580035104/a432b7691eb218ffe11d54f174d8889c.png?size=1024')
    embed.set_footer(text="Command executed by: {}".format(ctx.author.display_name))
    await ctx.send(embed=embed)
    first_image_face_ID = detected_faces[0].face_id


@bot.command()
async def sim(ctx, face_1: str, face_2: str):
    """finds similitudes on the face of two different pictures."""
    single_face_image_url = face_1
    single_image_name = os.path.basename(single_face_image_url)
    detected_faces = face_client.face.detect_with_url(url=single_face_image_url, detection_model='detection_03')
    if not detected_faces:
        raise Exception('No face detected from image {}'.format(single_image_name))

    print('Detected face ID from', single_image_name, ':')
    for face in detected_faces: print (face.face_id)
    print()

    first_image_face_ID = detected_faces[0].face_id

    multi_face_image_url = face_2
    multi_image_name = os.path.basename(multi_face_image_url)
    detected_faces2 = face_client.face.detect_with_url(url=multi_face_image_url, detection_model='detection_03')
    second_image_face_IDs = list(map(lambda x: x.face_id, detected_faces2))

    similar_faces = face_client.face.find_similar(face_id=first_image_face_ID, face_ids=second_image_face_IDs)
    if not similar_faces:
        print('No similar faces found in', multi_image_name, '.')
        embed2 = discord.Embed(title=f'No similar faces found in: {single_image_name.upper()} and {multi_image_name.upper()}', description ='No data', color = 0xFF5733)
        embed2.set_author(name='Solane', icon_url='https://cdn.discordapp.com/avatars/862131331580035104/a432b7691eb218ffe11d54f174d8889c.png?size=1024')
        embed2.set_footer(text="Command executed by: {}".format(ctx.author.display_name))
        await ctx.send(embed=embed2)


    else:
        print('Similar faces found in', multi_image_name + ':')
        for face in similar_faces:
            first_image_face_ID = face.face_id

            face_info = next(x for x in detected_faces2 if x.face_id == first_image_face_ID)
            if face_info:
                print('  Face ID: ', first_image_face_ID)
                print('  Face rectangle:')
                print('    Left: ', str(face_info.face_rectangle.left))
                print('    Top: ', str(face_info.face_rectangle.top))
                print('    Width: ', str(face_info.face_rectangle.width))
                print('    Height: ', str(face_info.face_rectangle.height))
                embed = discord.Embed(title=f'Similar faces found in: {single_image_name.upper()} and {multi_image_name.upper()}', description ='Data', color = 0xFF5733)
                embed.add_field(name="First face ID:", value=first_image_face_ID, inline=False)
                embed.add_field(name="Second face ID:", value=second_image_face_IDs, inline=False)
                embed.add_field(name="Face rectangle:", value="data of the similarities found:", inline=False)
                embed.add_field(name="Left: ", value=face_info.face_rectangle.left, inline=True)
                embed.add_field(name="Top: ", value=face_info.face_rectangle.top, inline=True)
                embed.add_field(name="Width: ", value=face_info.face_rectangle.width, inline=True)
                embed.add_field(name="Height: ", value=face_info.face_rectangle.height, inline=True)
                embed.set_author(name='Solane', icon_url='https://cdn.discordapp.com/avatars/862131331580035104/a432b7691eb218ffe11d54f174d8889c.png?size=1024')
                embed.set_footer(text="Command executed by: {}".format(ctx.author.display_name))
                await ctx.send(embed=embed)


 
print()
bot.run(token)