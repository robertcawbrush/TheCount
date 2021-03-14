import os
import sys
import logging
import discord
from dotenv import load_dotenv
import app.actions as actions
from app.actions import PREFIX
from app.google_sheets import Google_Sheets
from app.common.helpers import get_args

load_dotenv()
try:
    google_sheet = Google_Sheets(os.environ['SPREADSHEET_ID'], 'B4:Z4')
except KeyError as ke:
    print(
        f'''error retrieving {ke}.
            Did you set the environment variable for {ke}?''')
    print('shutting down')
    sys.exit()

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

client = discord.Client()


@client.event
async def on_ready():
    # get current house roles
    msg = f'{client.user} is ready'
    print(msg)


@client.event
async def on_message(message):
    # find out if admin for protected calls later
    # TODO: might not need based on has_permissions
    if not message.content.startswith(PREFIX):
        return

    if message.author.bot or message.author == client.user:
        return

    if message.content.startswith(PREFIX + actions.POINTS):
        try:
            rg = get_args(message.content)
            points_to_add = int(rg)
        except ValueError:
            await message.channel.send(f'error: {rg} is not a number')
            return
        user_roles = message.author.roles
        username = f'{message.author.name}#{message.author.discriminator}'
        house_role = google_sheet.find_user_house(user_roles)

        if house_role is not None:
            total_points = google_sheet.add_to_sheet(username, house_role, points_to_add)
            # TODO: fix house named with named tuple
            msg = f'''{points_to_add} points for {house_role},{message.author.name}'s
                points are {total_points}'''
            await message.channel.send(msg)
        else:
            msg = '''You are not in any current house, ask a mod to be
                placed in one\n to see current houses run -houses'''
            await message.channel.send(msg)
        return

    if message.content.startswith(PREFIX + actions.PING):
        await message.channel.send('Good Evening')
        return

    if message.content.startswith(PREFIX + actions.HOUSES):
        houses_list = ''

        for house in google_sheet.houses_build:
            houses_list += f'`{house}`\n'
        if len(houses_list) > 0:
            await message.channel.send(houses_list)
        else:
            await message.channel.send("There aren't any houses currently, bug a mod")
        return

    if message.content.startswith(PREFIX + actions.HELP):
        available_commands = ''
        for command in actions.AVAILABLE_COMMANDS:
            available_commands += '`' + PREFIX + command + '`\n'

        help_response = '''All commands start with {} for example `-ping`
        \nAvailable commands are : \n{}\n some commands require your input
            such as a number for example:\n {}'''.format(
            PREFIX, available_commands,
            ('`' + PREFIX + actions.POINTS + ' 3`'))

        await message.channel.send(help_response)
        return

    if message.content.startswith(PREFIX):
        msg = 'command not found, run `-help` for available commands'
        await message.channel.send(msg)
        return

