from pywa import WhatsApp
from flask import Flask
from pywa.types import Message, CallbackButton
# from pywa.filters import  CallbackFilter
import requests
# import mysql.connector


def gpt(uid,text):
    headers={'Content-Type': 'application/json'}
    body = {
        "user_id":uid,
        "prompt":text

    }
    r = requests.post('http://127.0.0.1:5002/chat',headers=headers,json=body)
    print(r)
    ans = r.json()
    print(ans)
    if 'filename' not in ans:
        anss = ans['message']['content']
        return anss
    else:
        return ans

    


flask_app = Flask(__name__)
wa = WhatsApp(
    phone_id='229272100273078',
    token='EABkWqVSvZBZCcBO6j0ZBwTTZClCftAd9FgCeazZCSQnXGilgGj6BGTm2MDynamTv7z4EzdnkCZB23w4GNZCSDZC8TVNImzKCAcvuoe1Ad3i3oAEqZCneAPY7UmjKZCN54UFntDLrfbXlycd9O7EkzGKOntix6EpBhGRBtT6xKuZBZBe3hsZCHmpLK6D3KcZAYEQHpfdUCapLDBjleSSD3QTQ94EzgZD',
    server=flask_app,
    verify_token='asd',
)

@wa.on_message()
def hello(client: WhatsApp, message: Message):
    # message.react('👋')
    print(message)
    uid = message.from_user.wa_id
    msg = message.text
    reply = gpt(uid,msg)
    if type(reply) == str:
        message.reply_text(
            text=reply,
        )
    else:
        message.reply_document(
        "invoice.pdf",
        # document="invoice.pdf",
        body="invoice.pdf"
       
    )
    print('pdf send')

# @wa.on_callback_button(CallbackFilter.data_startswith('id'))
# def click_me(client: WhatsApp, clb: CallbackButton):
#     clb.reply_text('You clicked me!')

flask_app.run()  # Run the flask app to start the webhook