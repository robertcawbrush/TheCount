import discord
import os
import requests
import json
from app import actions
from dotenv import load_dotenv


def main():
    load_dotenv()

    client = discord.Client()

    @client.event
    async def on_ready():
        print(f'{client.user} is ready')

    @client.event
    async def on_message(message):
        if message.author == client.user:
            return

        if message.content.startswith(actions.PING):
            await message.channel.send('Good Evening')
            return

        if message.content.startswith(actions.HELP):
            available_commands = ''
            for command in actions.AVAILABLE_COMMANDS:
                available_commands += command + '\n'
            await message.channel.send('Available commands are : \n' + available_commands)
            return

        if message.content.startswith('/'):
            await message.channel.send('command not found, run /help for available commands')
            return

    # try:
    apikey = os.environ['COUNT_TOKEN']
    client.run(apikey)
    # except KeyError as ke:
    #     print(f'api key retrival failed for {ke}')


if __name__ == '__main__':
    main()
