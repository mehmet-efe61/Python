import discord
import asyncio

client = discord.Client()

def bos(a):
    return " ".join(a.upper().
                      replace("0", "SIFIR").
                      replace("1", "BİR").
                      replace("2", "İKİ").
                      replace("3", "ÜÇ").
                      replace("4", "DÖRT").
                      replace("5", "BEŞ").
                      replace("6", "ALTI").
                      replace("7", "YEDİ").
                      replace("8", "SEKİZ").
                      replace("9", "DOKUZ"))

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

@client.event
async def on_message(message):
    if message.content.startswith('*'):
        a = message.content[1:]
        await client.send_message(message.channel, bos(a))
        #counter = 0
        #tmp = await client.send_message(message.channel, 'Calculating messages...')
        #async for log in client.logs_from(message.channel, limit=100):
        #    if log.author == message.author:
        #        counter += 1

        #await client.edit_message(tmp, 'You have {} messages.'.format(counter))
    #elif message.content.startswith('!sleep'):
        #await asyncio.sleep(5)
        #await client.send_message(message.channel, 'Done sleeping')

client.run('MzY2OTUyNzQ4Mjc4NzQzMDUx.DL0nbw.Cu_NSuwmHHWY_SaOR3yc3SVgrG8')
