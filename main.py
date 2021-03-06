import discord
import os
from app import actions
from app.actions import PREFIX
from dotenv import load_dotenv


def main():
    load_dotenv()

    client = discord.Client()

    @client.event
    async def on_ready():
        print(f'{client.user} is ready')

    @client.event
    async def on_message(message):
        # find out if admin for protected calls later
        is_admin = False
        if not message.content.startswith(PREFIX):
            return

        if message.author.bot or message.author == client.user:
            return

        if message.content.startswith(PREFIX + actions.PING):
            await message.channel.send('Good Evening')
            return

        if message.content.startswith(PREFIX + actions.HELP):
            available_commands = ''
            for command in actions.AVAILABLE_COMMANDS:
                available_commands += PREFIX + command + '\n'
            await message.channel.send('Available commands are : \n' + available_commands)
            return

        if message.content.startswith(PREFIX):
            await message.channel.send('command not found, run -help for available commands')
            return

    try:
        apikey = os.environ['COUNT_TOKEN']
        client.run(apikey)
    except KeyError as ke:
        print(f'api key retrival failed for {ke}')


if __name__ == '__main__':
    main()
