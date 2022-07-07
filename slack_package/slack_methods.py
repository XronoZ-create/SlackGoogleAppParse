from slack_sdk.webhook import WebhookClient
from slack_sdk.web import WebClient
from config import Config

token = Config.SLACK_TOKEN
channel = Config.SLACK_CHANNEL

def send_slack_message(block):
    client = WebClient(token=token)
    client.chat_postMessage(blocks=block, channel=channel)

def update_message(ts, block):
    client = WebClient(token=token)
    a = client.chat_update(channel=channel, ts=ts, blocks=block)
    print(a)

def upload_image(filepath):
    client = WebClient(token=token)
    response = client.files_upload(channels='#googleplay-find-app', file=filepath)
    print(response)
    return response["file"]['permalink']



if __name__ == "__main__":
    from slack_package.model_message import Message
    block = Message(
        name='Test Game',
        href='https://play.google.com/store/apps/details?id=net.DuckyGames.PetIdle',
        developer='DuckyGames',
        screenshots=[
            'https://play-lh.googleusercontent.com/HxyKC546tPZniXkNQ0QBMQxMDQmPL8wAWdbOxPVSGZpX9twYqfUY9hnQicCIFlptMfA=w526-h296-rw',
            'https://play-lh.googleusercontent.com/4EVKyN7M_P7mZeM_JgkcJbSZbaYh5IXpNnUD3rNN-ur0PV9QAYoC5F1lmQ44aD1GJIY=w526-h296-rw',
            'https://play-lh.googleusercontent.com/pZcYhqnGTEDwcz7MzPUXNDTmBm40s5l3KGZ5Tp2N6wN4ec2VReWoR7R9s0MXKc8spHE=w526-h296-rw'
        ],
        video=None,
        already_send=False
    ).block
    send_slack_message(block=block)