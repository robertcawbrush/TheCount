import discord
import os
import requests
import json

def main():

    client = discord.Client()
    # TODO: Delete this
    def get_quote():
        response = requests.get("https://zenquotes.io/api.random")

        json_data = json.load(response.text)

        quote = json_data[0]['q'] + " -" + json_data[0]['a']
        return quote

    @client.event
    async def on_ready():
        print(f'{client.user} is ready')

    @client.event
    async def on_message(message):
        if message.author == client.user:
            return
        
        if message.content.startswith('/hello'):
            await message.channel.send('Good Evening')
        
        if message.content.startswith('/quote'):
            quote = get_quote()
            await message.channel.send(quote)

    try:
        apikey = os.environ['COUNT_TOKEN']
        client.run(apikey)
    except KeyError as ke:
        print(f'api key retrival failed for {ke}') 
if __name__ == '__main__':
    main()