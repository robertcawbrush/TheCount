import os
from dotenv import load_dotenv
from app import client

load_dotenv()
if __name__ == '__main__':
    try:
        apikey = os.environ['COUNT_TOKEN']
        client.run(apikey)

    except KeyError as ke:
        print(f'api key retrival failed for {ke}')
