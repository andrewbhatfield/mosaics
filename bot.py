import discord
import os

from discord.ext import commands

from mosaic import mosaic

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)
token = ''

@client.event
async def on_ready():
    print("Logged in as bot {0.user}".format(client))


@client.event
async def on_message(message):
    username = str(message.author).split("#")[0]
    channel = str(message.channel.name)
    msg = str(message.content)

    print(f'Message {msg} by {username} on {channel}')

    if message.author == client.user:
        return

    if msg.lower().split(' ')[0] == '!mosaic':
        try:
            proj_name = msg.split()[1]
            src_url = msg.split()[2]
            query = ' '.join(msg.split()[3:])
            print(f'creating project {proj_name} from url {src_url} and query {query}')
            try:
                final = mosaic(src_url, proj_name, query)
                await message.channel.send(file=discord.File(final))
            except Exception as e:
                print(e)
                await message.channel.send('error creating mosaic')
            # await message.channel.send(f'testing {src_url} {query}')
        except Exception as e:
            print(e)
            await message.channel.send('invalid syntax - try !mosaic {proj_name} {source_image_url} {google_query}')
        return


client.run(token)