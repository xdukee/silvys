import discord
import asyncio
import youtube_dl
from discord.ext import commands
from itertools import cycle


client = commands.Bot(command_prefix = '*')
client.remove_command('help')
status = ['Version 0.0.3', 'Working on V0.0.5', 'Made by dukee#6255']

async def change_status():
    await client.wait_until_ready()
    messages = cycle(status)

    while not client.is_closed:
        current_status = next(messages)
        await client.change_presence(game=discord.Game(name=current_status))
        await asyncio.sleep(6)

players = {}
queues = {}

def check_queue(id):
    if queues[id] != []:
        player = queues[id].pop(0)
        players[id] = player
        player.start()

@client.event
async def on_ready():
     print('Silvys is online.')

@client.command(pass_context=True)
async def join(ctx):
    channel = ctx.message.author.voice.voice_channel
    await client.join_voice_channel(channel)

@client.command(pass_context=True)
async def leave(ctx):
    server = ctx.message.server
    voice_client = client.voice_client_in(server)
    await voice_client.disconnect()

@client.command(pass_context=True)
async def play(ctx, url):
    server = ctx.message.server
    voice_client = client.voice_client_in(server)
    player = await voice_client.create_ytdl_player(url, after=lambda: check_queue(server.id))
    players[server.id] = player
    player.start()

@client.command(pass_context=True)
async def pause(ctx):
    id = ctx.message.server.id
    players[id].pause()

@client.command(pass_context=True)
async def stop(ctx):
    id = ctx.message.server.id
    players[id].stop()

@client.command(pass_context=True)
async def resume(ctx):
    id = ctx.message.server.id
    players[id].resume()

@client.command(pass_context=True)
async def queue(ctx, url):
    server = ctx.message.server
    voice_client = client.voice_client_in(server)
    player = await voice_client.create_ytdl_player(url, after=lambda: check_queue(server.id))

    if server.id in queues:
        queues[server.id].append(player)
    else:
        queues[server.id] = [player]
    await client.say('Video has been queued:owoWink:')

@client.command(pass_context=True)
async def help(ctx):
    embed = discord.Embed(title="**Silvys the green elf girl!**", description="", color=0x32cd32)

    embed.add_field(name="Command list:", value="--------------------------------------", inline=False)
    embed.add_field(name="*join", value="Silvys will join your vocal chat.", inline=False)
    embed.add_field(name="*leave", value="Silvys will leave your vocal chat.", inline=False)
    embed.add_field(name="*queue", value="For queueing songs.", inline=False)
    embed.add_field(name="*pause", value="To pause songs.", inline=False)
    embed.add_field(name="*resume", value="To resume the paused song.", inline=False)
    embed.add_field(name="*stop", value="To let Silvys stop playing music.", inline=False)
    embed.add_field(name="--", value="--", inline=False)
    embed.add_field(name="**Silvys Info**", value="Version 0.0.3 / Working on 0.0.5", inline=True)


    await client.send_message(ctx.message.channel, embed=embed)



client.loop.create_task(change_status())
client.login(process.env.BOT_TOKEN):
