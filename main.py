import discord
import os

def main():

    client = discord.Client()

    @client.event
    async def on_ready():
        print(f'{client.user} is ready')

    @client.event
    async def on_message(message):
        if message.author == client.user:
            return
        
        if message.content.startswith('/hello'):
            await message.channel.send('Good Evening')

    client.run(os.getenv('COUNT_TOKEN'))

if __name__ == '__main__':
    main()