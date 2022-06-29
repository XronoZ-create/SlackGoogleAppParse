from slack_sdk.signature import SignatureVerifier
from flask import Flask, request, make_response
from slack_package.slack_methods import update_message
from slack_package.model_message import Message
from config import Config
import json
import modules.google_sheets

signature_verifier = SignatureVerifier(
    signing_secret=Config.SLACK_SIGNING_SECRET
)

app = Flask(__name__)

@app.route("/slack", methods=["POST"])
def slack_app():
    print('slack_app')

    if not signature_verifier.is_valid(
            body=request.get_data(),
            timestamp=request.headers.get("X-Slack-Request-Timestamp"),
            signature=request.headers.get("X-Slack-Signature")):
        return make_response("invalid request", 403)

    payload_dict = json.loads(request.form.to_dict()['payload'])
    action = payload_dict['actions'][0]['value']
    print(payload_dict)
    print(action)
    print(payload_dict['container']['message_ts'])

    if action == 'to_sheets':
        print('Send to Google Sheets')

        ts = payload_dict['container']['message_ts']

        text = payload_dict['message']['blocks'][0]['text']['text']
        href = text.split('<')[1].split('| ')[0]
        name = text.split('<')[1].split('| ')[1].split('>')[0]
        try:
            screenshots_href = payload_dict['message']['blocks'][2]['image_url']
        except:
            screenshots_href = None

        modules.google_sheets.g_append(href=href, name=name)
        block = Message(
            name='',
            href='',
            developer='',
            screenshots=[],
            video='',
            already_send=True,
            text=text,
            screenshots_href=screenshots_href
        ).block
        update_message(ts=ts, block=block)

    return make_response("", 200)








if __name__ == "__main__":
    app.run(debug=True)