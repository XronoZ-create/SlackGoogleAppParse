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
            'https://play-lh.googleusercontent.com/sTwKtOL8fA6sc5f8uELoNHm7s6ivsGGNaTAYwMHi0CA7o9XjkrToRQS01T9aVQ7UowRy=w2560-h1440-rw',
            'https://play-lh.googleusercontent.com/sqvk_U7wcyDM520AmQxalmmYt55MUKTFczsTLIv-nNOCSIHEBoGb40Ppm6mEnYSHCOY=w2560-h1440-rw',
            'https://play-lh.googleusercontent.com/Pvdt4tgv6inIpQ-qAMvcCfImmPk3W6N2sULmOyN-DEjGJcZLR4_8d3qQsCvU4FoBSS0=w2560-h1440-rw'
        ],
        video='https://youtu.be/KVcOjMD_9b8',
        already_send=False
    ).block
    send_slack_message(block=block)