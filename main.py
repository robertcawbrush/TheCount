import os
import discord
import app.actions as actions
from app.actions import PREFIX
from dotenv import load_dotenv
from app.google_sheets import Google_Sheets
from app.common.helpers import get_args


def main():
    load_dotenv()
    try:
        google_sheet = Google_Sheets(os.environ['SPREADSHEET_ID'], 'B5:I6')
    except KeyError as ke:
        print(
            f'''error retrieving {ke}.
             Did you set the environment variable for {ke}?''')
        print('shutting down')
        return
    client = discord.Client()
    @client.event
    async def on_ready():
        # get current house roles
        print(f'{client.user} is ready')

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
                google_sheet.add_to_sheet(username, house_role, points_to_add)
                # return point value added to user points
                #  return current points after sum
                msg = f'''{points_to_add} points added to {house_role},{message.author.name}\'s
                 points are {"ADD POINTS HERE"}'''
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
            # TODO: add number val to call, there are these houses and they have this many members

            google_sheet.get_all_house_member_count()
            house_list = 'Current Houses are:\n'
            for house in google_sheet.current_houses['houses']:
                house_list += f'`{house}`\n'
            await message.channel.send(house_list)
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

    try:
        apikey = os.environ['COUNT_TOKEN']
        client.run(apikey)
    except KeyError as ke:
        print(f'api key retrival failed for {ke}')

    print('end of program after client run')

if __name__ == '__main__':
    main()
