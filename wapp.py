from pywa import WhatsApp
from flask import Flask
from pywa.types import Message, CallbackButton
# from pywa.filters import  CallbackFilter
import requests
# import mysql.connector
import os


def gpt(uid,text):
    headers={'Content-Type': 'application/json'}
    body = {
        "user_id":uid,
        "prompt":text

    }
    r = requests.post('http://127.0.0.1:5008/chat',headers=headers,json=body)
    print(r)
    ans = r.json()
    print(ans)
    if 'filename' not in ans:
        anss = ans['message']
        return anss
    else:
        return ans

    


flask_app = Flask(__name__)
wa = WhatsApp(
    phone_id='229272100273078',
    token='EABkWqVSvZBZCcBO6fNk4ZCe2djoIeIpXGCeFerwEQ221JsLPVPlevwDXG0mdHcOmSKU1ReyVw9BmTLYrvw4cja9PrjgaUVUxHZBckjE0ERBU5jfwnOk6KmClMndIYZC2KngTSzqaN7dJcsZB9CG4k43LOJTztdF5rKoPPwbBSTmgUgCoQbAqlT0ghXUcwA9J5j',
    server=flask_app,
    verify_token='asd',
)
filename= ""
@wa.on_message()
def hello(client: WhatsApp, message: Message):
    # message.react('👋')
    print(message)
    uid = message.from_user.wa_id
    msg = message.text
    reply = gpt(uid,msg)
    base_url ='www.joyland.com/packages'
    # if type(reply) == str:
    if base_url not in reply:
        message.reply_text(
            text=reply,
        )
    else:
        
        if 'bounce' in reply :
            filename = 'Bouncekhi.pdf'
        elif 'giggle' in reply:
            filename ="Giggle Town.pdf"
        elif 'northwall' in reply:
            filename = "Peekabear North Walk.pdf"
        elif 'peekabearocean' in reply:
            filename = "Peekabear Oocean Mall.pdf"
        elif 'hyderabad' in reply.lower():
            filename = "Super Space Hyderabad.pdf"
        elif 'millennium' in reply.lower():
            filename = "Super Space Millennium Mall.pdf"
        elif 'superspaceocean' in reply.lower():
            filename = "Super Space Ocean Mall.pdf"
        elif 'shareef' in reply.lower():
            filename = "Super Space Shareef Complex.pdf"




        cwd = os.getcwd()
        print(cwd)
        message.reply_document(
        f"birthday/{filename}",
        # document="invoice.pdf",
        body=filename
        )



    print('pdf send',filename)

# @wa.on_callback_button(CallbackFilter.data_startswith('id'))
# def click_me(client: WhatsApp, clb: CallbackButton):
#     clb.reply_text('You clicked me!')

flask_app.run(port=5001)  # Run the flask app to start the webhook
