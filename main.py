import asyncio
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
    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5 -vol 35', 
    'options': '-vn -vol 15',
}
folder = 'music_files'

youtube_dl.utils.bug_reports_message = lambda: ''
ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': 'music_files/%(id)s.mp3',
    'restrictfilenames': True,
    'noplaylist': False,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0' # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ffmpeg_options = {
    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5 -vol 30', 
    'options': '-vn -vol 30',
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)
queue = {}
class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.50):
        super().__init__(source, volume)

        self.data = data

        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)


def addToQueue(guild, song):
    if guild.id not in queue:
        queue[guild.id] = []
    queue[guild.id].append(song)
    print("adding to queue")

async def playSong(ctx, channel):
    async with ctx.typing():
        if(ctx.voice_client.is_playing()):
            return
        if len(queue[channel.guild.id]) == 0:
            return
        song = queue[channel.guild.id].pop(0)
        print(queue[channel.guild.id])
        if song == None:
            return
        player = await YTDLSource.from_url(song, loop=bot_client.loop, stream=True)
        try :
            channel.play(
                player,
                after= lambda e: asyncio.run_coroutine_threadsafe(playSong(ctx, channel),loop=bot_client.loop)
            )
        except discord.errors.ClientException:
            print("error client")

    await ctx.send('**Now playing:** {}'.format(player.title))

def after_song(ctx, channel,error):
    print("popping")
    queue[channel.guild.id].pop() 
    asyncio.run_coroutine_threadsafe(playSong(ctx,channel), bot_client.loop)

@bot_client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot_client))

@bot_client.command()
async def join(ctx):
    if ctx.author.voice is None:
        await ctx.send("you need to be in voice")
        return
    else:
        channel = ctx.author.voice.channel
    await channel.connect()
    print(ctx.voice_client.is_playing())

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
    elif not message.content.startswith('.') and taggedUser.name == 'Breath Of The Dying':
        await message.channel.send('that\'s what she said')
        return

    if result != '':
        await message.channel.send(result)
    await bot_client.process_commands(message)

@bot_client.command(brief="Plays a single video, from a youtube URL") #or bot.command()
async def play(ctx, url=''):
    voice = ctx.voice_client

    if ctx.author.voice is None:
        print(ctx.author)
        await ctx.send("you need to be in voice to send commands")
        return

    if voice.is_paused():
        voice.resume()
        return 

    if url == '':
        return

    addToQueue(ctx.message.guild, url)
    await playSong(ctx, voice)

@bot_client.command(brief="stops song") #or bot.command()
async def stop(ctx):
    voice = ctx.voice_client
    if ctx.author.voice is None:
        return
    if voice.is_playing():
        voice.stop()

@bot_client.command(brief='pauses song')
async def pause(ctx):
    voice = ctx.voice_client
    if ctx.author.voice is None:
        return
    if voice.is_playing():
            voice.pause()


@bot_client.command(brief='skips current song in queue')
async def next(ctx):
    if ctx.author.voice is None:
        return
    voice = ctx.voice_client
    voice.stop()
    await playSong(ctx, voice)

@bot_client.command(brief='clears queue')
async def clear(ctx):
    if ctx.author.voice is None:
        return
    voice = ctx.voice_client
    voice.stop()
    queue.clear()

# @bot_client.event
# async def on_voice_state_update(member, before, after): 
#     #print("before " + before.channel.name)
#     print(member.name)

#     steven='https://youtu.be/bRhlRM6rYck'
#     nai='https://youtu.be/ltvb25yzFm4'
#     three='https://youtu.be/ltvb25yzFm4'
#     brian='https://youtu.be/NT62mT7Deg0'
#     tony='https://youtu.be/JZ4AV_yrlzI'
#     nerd='https://youtu.be/J9b7gveF_tQ'
#     charles='https://youtu.be/0VKcQ7572IY'
#     nate='https://youtu.be/rPxpXKcNnqY'
#     richard='https://youtu.be/zF9Fo83bcX4'
#     fro='https://youtu.be/ZrDmQsWeov8'
#     abe='https://youtu.be/CUwkE5fdgf0'
#     vcs = bot_client.voice_clients

# #use bot_client.is_voice_connected() or is_connected()
#     if after.channel !=None and before.channel == None:
#         if vcs and len(vcs)>0:
#             vc = vcs[0]
#             if not vc.is_playing():
#                 if member.name=='Stefano':
#                     with YoutubeDL(YDL_OPTIONS) as ydl:
#                         info = ydl.extract_info(steven, download=False)
#                     URL = info['formats'][0]['url']
#                     vc.play(FFmpegPCMAudio(URL, **FFMPEG_OPTIONS))
#                     vc.is_playing()
#                 elif member.name == 'headache':
#                     with YoutubeDL(YDL_OPTIONS) as ydl:
#                         info = ydl.extract_info(nai, download=False)
#                     URL = info['formats'][0]['url']
#                     vc.play(FFmpegPCMAudio(URL, **FFMPEG_OPTIONS))
#                     vc.is_playing()
#                 elif member.name == 'Sou-nDUBU':
#                     with YoutubeDL(YDL_OPTIONS) as ydl:
#                         info = ydl.extract_info(three, download=False)
#                     URL = info['formats'][0]['url']
#                     vc.play(FFmpegPCMAudio(URL, **FFMPEG_OPTIONS))
#                     vc.is_playing()
#                 elif member.name == 'Negapessah':
#                     with YoutubeDL(YDL_OPTIONS) as ydl:
#                         info = ydl.extract_info(brian, download=False)
#                     URL = info['formats'][0]['url']
#                     vc.play(FFmpegPCMAudio(URL, **FFMPEG_OPTIONS))
#                     vc.is_playing()
#                 elif member.name == 'Deluxe530':
#                     with YoutubeDL(YDL_OPTIONS) as ydl:
#                         info = ydl.extract_info(tony, download=False)
#                     URL = info['formats'][0]['url']
#                     vc.play(FFmpegPCMAudio(URL, **FFMPEG_OPTIONS))
#                     vc.is_playing()
#                 elif member.name == 'Breath Of The Dying':
#                     with YoutubeDL(YDL_OPTIONS) as ydl:
#                         info = ydl.extract_info(nerd, download=False)
#                     URL = info['formats'][0]['url']
#                     vc.play(FFmpegPCMAudio(URL, **FFMPEG_OPTIONS))
#                     vc.is_playing()
#                 elif member.name in [ 'TheFoolz', 'chengalang']:
#                     with YoutubeDL(YDL_OPTIONS) as ydl:
#                         info = ydl.extract_info(charles, download=False)
#                     URL = info['formats'][0]['url']
#                     vc.play(FFmpegPCMAudio(URL, **FFMPEG_OPTIONS))
#                     vc.is_playing()
#                 elif member.name == 'N8diesel':
#                     with YoutubeDL(YDL_OPTIONS) as ydl:
#                         info = ydl.extract_info(nate, download=False)
#                     URL = info['formats'][0]['url']
#                     vc.play(FFmpegPCMAudio(URL, **FFMPEG_OPTIONS))
#                     vc.is_playing()
#                 elif member.name == 'sideout503':
#                     with YoutubeDL(YDL_OPTIONS) as ydl:
#                         info = ydl.extract_info(richard, download=False)
#                     URL = info['formats'][0]['url']
#                     vc.play(FFmpegPCMAudio(URL, **FFMPEG_OPTIONS))
#                     vc.is_playing()
#                 elif member.name == 'fr0t0es':
#                     with YoutubeDL(YDL_OPTIONS) as ydl:
#                         info = ydl.extract_info(fro, download=False)
#                     URL = info['formats'][0]['url']
#                     vc.play(FFmpegPCMAudio(URL, **FFMPEG_OPTIONS))
#                     vc.is_playing()
#                 elif member.name == 'ABEast':
#                     with YoutubeDL(YDL_OPTIONS) as ydl:
#                         info = ydl.extract_info(abe, download=False)
#                     URL = info['formats'][0]['url']
#                     vc.play(FFmpegPCMAudio(URL, **FFMPEG_OPTIONS))
#                     vc.is_playing()
#             else:
#                 return
#     else:
#         return
    
bot_client.run('OTAzMDExNDQyNDUyNzI5ODc3.YXmw8Q.E13TcCwaNXxbAmqbgR6LwXHv-G4')