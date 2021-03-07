import discord
import os
from app import actions
from app.actions import PREFIX
from dotenv import load_dotenv
from app.google_sheets import Google_Sheets
from app.common.helpers import get_args


def main():
    load_dotenv()

    try:
        google_sheet = Google_Sheets(
            os.environ['SPREADSHEET_ID'], 'DATA B5:I6')
    except KeyError as ke:
        print(
            f'error retrieving {ke}. Did you set the environment variable for {ke}?')
        print('shutting down')
        return

    client = discord.Client()

    @client.event
    async def on_ready():
        print(f'{client.user} is ready')

    @client.event
    async def on_message(message):
        # find out if admin for protected calls later TODO: might not need based on has_permissions
        is_admin = False
        if not message.content.startswith(PREFIX):
            return

        if message.author.bot or message.author == client.user:
            return

        if message.content.startswith(PREFIX + actions.POINTS):
            try:
                rg = get_args(message.content)
                points_to_add = int(rg)
            except ValueError as ve:
                await message.channel.send(f'error: supplied value {rg} is not a number')
                return

            username = f'{message.author.name}#{message.author.discriminator}'

            google_sheet.add_to_sheet(username, points_to_add)
            # get user that called
            # for user that called add points to doc
            # return point value added to user points, return current points after sum
            return

        if message.content.startswith(PREFIX + actions.PING):
            await message.channel.send('Good Evening')
            return

        if message.content.startswith(PREFIX + actions.HELP):
            available_commands = ''
            for command in actions.AVAILABLE_COMMANDS:
                available_commands += PREFIX + command + '\n'

            help_response = 'All commands start with {} for example "-ping" \nAvailable commands are : \n{}\n some commands require your input such as a number for example:\n "{}"'.format(
                PREFIX, available_commands, (PREFIX + actions.POINTS + ' 3'))

            await message.channel.send(help_response)
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
