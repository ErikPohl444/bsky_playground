import os
from atproto import Client
from dotenv import load_dotenv

if __name__ == '__main__':
    load_dotenv()
    bsky_url = os.getenv('BSKY_URL')
    bsky_pwd = os.getenv('BSKY_PWD')
    client = Client()
    client.login(bsky_url, bsky_pwd)
    post = client.send_post('A final post using the Python SDK for now')
