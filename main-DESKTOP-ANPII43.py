import discord
from discord.ext import commands
from discord.utils import get
from discord import FFmpegPCMAudio
from youtube_dl import YoutubeDL
import os
import random
import re
import youtube_dl

#client = discord.Client()
#TODO need to handle errors (connected, is_playing etc)
#invite link = https://discord.com/api/oauth2/authorize?client_id=903011442452729877&permissions=543350587216&scope=bot
bot_client = commands.Bot(command_prefix = '.')

chris_responses = ['oh he dead', 'according to Brian, he died', 'RIP in peace']

awesome_responses = ['mucho bueno', 'naisu', 'awesome', 'amazing', 'stunning', 
    'astounding', 'astonishing', 'awe-inspiring','stupendous', 'staggering', 
    'extraordinary', 'incredible', 'unbelievable', 'magnificient']

target_phrases = ['should\'ve', 'should have', 'could\'ve', 'could have', 
    'would\'ve', 'would have']

YDL_OPTIONS = {
    'format': 'bestaudio',
    'noplaylist':'True',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
    'outtmpl': 'song.%(ext)s',
}

FFMPEG_OPTIONS = {
    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5 -vol 65', 
    'options': '-vn -vol 30',
}

@bot_client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot_client))

@bot_client.command()
async def join(ctx):
    channel = ctx.author.voice.channel
    await channel.connect()

@bot_client.command()
async def leave(ctx):
    await ctx.voice_client.disconnect()


@bot_client.event
async def on_message(message):
    if message.author == bot_client.user:
        return

    taggedUser = message.author
    print(taggedUser.name)
    result = ''

    if any(phrase in message.content.lower() for phrase in target_phrases):
        result = f'{random.choice(awesome_responses)}! {taggedUser.mention} that\'s right'
    elif 'chris' in message.content.lower():
        result = random.choice(chris_responses)
    elif taggedUser.name == 'Breath Of The Dying':
        await message.channel.send('that\'s what she said')
        return

    if result != '':
        await message.channel.send(result)
    await bot_client.process_commands(message)

@bot_client.command(brief="Plays a single video, from a youtube URL") #or bot.command()
async def play(ctx, url):
    print("url:"+url)
    voice = ctx.voice_client

    if not voice.is_playing():
        with YoutubeDL(YDL_OPTIONS) as ydl:
            info = ydl.extract_info(url, download=False)
        URL = info['formats'][0]['url']
        voice.play(FFmpegPCMAudio(URL, **FFMPEG_OPTIONS))
        voice.is_playing()
    else:
        await ctx.send("Already playing song")
        return

@bot_client.command(brief="stops song") #or bot.command()
async def stop(ctx):
    voice = ctx.voice_client
    if voice.is_playing():
        voice.stop()



@bot_client.command(brief='pauses song')
async def pause(ctx):
    voice = ctx.voice_client

    if voice.is_playing():
            voice.pause()



@bot_client.event
async def on_voice_state_update(member, before, after): 
    #print("before " + before.channel.name)
    print(member.name)

    steven='https://youtu.be/kJq7qQP_Gvk'
    nai='https://youtu.be/RT1MAzyUkJE'
    three='https://youtu.be/ueVjrc7YYoE'
    brian='https://youtu.be/NT62mT7Deg0'
    tony='https://youtu.be/JZ4AV_yrlzI'
    nerd='https://youtu.be/J9b7gveF_tQ'
    charles='https://youtu.be/0VKcQ7572IY'
    nate='https://youtu.be/rPxpXKcNnqY'
    richard='https://youtu.be/zF9Fo83bcX4'
    fro='https://youtu.be/ZrDmQsWeov8'
    abe='https://youtu.be/CUwkE5fdgf0'
    vcs = bot_client.voice_clients

#use bot_client.is_voice_connected() or is_connected()
    if after.channel !=None and before.channel == None:
        if vcs and len(vcs)>0:
            vc = vcs[0]
            if not vc.is_playing():
                if member.name=='Stefano':
                    with YoutubeDL(YDL_OPTIONS) as ydl:
                        info = ydl.extract_info(steven, download=False)
                    URL = info['formats'][0]['url']
                    vc.play(FFmpegPCMAudio(URL, **FFMPEG_OPTIONS))
                    vc.is_playing()
                elif member.name == 'headache':
                    with YoutubeDL(YDL_OPTIONS) as ydl:
                        info = ydl.extract_info(nai, download=False)
                    URL = info['formats'][0]['url']
                    vc.play(FFmpegPCMAudio(URL, **FFMPEG_OPTIONS))
                    vc.is_playing()
                elif member.name == 'Sou-nDUBU':
                    with YoutubeDL(YDL_OPTIONS) as ydl:
                        info = ydl.extract_info(three, download=False)
                    URL = info['formats'][0]['url']
                    vc.play(FFmpegPCMAudio(URL, **FFMPEG_OPTIONS))
                    vc.is_playing()
                elif member.name == 'Negapessah':
                    with YoutubeDL(YDL_OPTIONS) as ydl:
                        info = ydl.extract_info(brian, download=False)
                    URL = info['formats'][0]['url']
                    vc.play(FFmpegPCMAudio(URL, **FFMPEG_OPTIONS))
                    vc.is_playing()
                elif member.name == 'Deluxe530':
                    with YoutubeDL(YDL_OPTIONS) as ydl:
                        info = ydl.extract_info(tony, download=False)
                    URL = info['formats'][0]['url']
                    vc.play(FFmpegPCMAudio(URL, **FFMPEG_OPTIONS))
                    vc.is_playing()
                elif member.name == 'Breath Of The Dying':
                    with YoutubeDL(YDL_OPTIONS) as ydl:
                        info = ydl.extract_info(nerd, download=False)
                    URL = info['formats'][0]['url']
                    vc.play(FFmpegPCMAudio(URL, **FFMPEG_OPTIONS))
                    vc.is_playing()
                elif member.name in [ 'TheFoolz', 'chengalang']:
                    with YoutubeDL(YDL_OPTIONS) as ydl:
                        info = ydl.extract_info(charles, download=False)
                    URL = info['formats'][0]['url']
                    vc.play(FFmpegPCMAudio(URL, **FFMPEG_OPTIONS))
                    vc.is_playing()
                elif member.name == 'N8diesel':
                    with YoutubeDL(YDL_OPTIONS) as ydl:
                        info = ydl.extract_info(nate, download=False)
                    URL = info['formats'][0]['url']
                    vc.play(FFmpegPCMAudio(URL, **FFMPEG_OPTIONS))
                    vc.is_playing()
                elif member.name == 'sideout503':
                    with YoutubeDL(YDL_OPTIONS) as ydl:
                        info = ydl.extract_info(richard, download=False)
                    URL = info['formats'][0]['url']
                    vc.play(FFmpegPCMAudio(URL, **FFMPEG_OPTIONS))
                    vc.is_playing()
                elif member.name == 'fr0t0es':
                    with YoutubeDL(YDL_OPTIONS) as ydl:
                        info = ydl.extract_info(fro, download=False)
                    URL = info['formats'][0]['url']
                    vc.play(FFmpegPCMAudio(URL, **FFMPEG_OPTIONS))
                    vc.is_playing()
                elif member.name == 'ABEast':
                    with YoutubeDL(YDL_OPTIONS) as ydl:
                        info = ydl.extract_info(abe, download=False)
                    URL = info['formats'][0]['url']
                    vc.play(FFmpegPCMAudio(URL, **FFMPEG_OPTIONS))
                    vc.is_playing()
            else:
                return
    else:
        return
    
bot_client.run('OTAzMDExNDQyNDUyNzI5ODc3.YXmw8Q.E13TcCwaNXxbAmqbgR6LwXHv-G4')