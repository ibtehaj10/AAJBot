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
    phone_id='109683645280921',
    token='EAAPjgUQ6VZCIBOzYYvL1TVHsnBXWk1ZC9sJ9vcjwmVZCMKx3crF3rm2DHlklp4cWv6aIUp3p2MpRgwFdqzE5irdQvRd9oKBSzA9c8pUANtUPcwC8LQRoZB02728cTB1VJiyuZAQAht8NXUnLAZAhOCZCHrr1cfT7ZB0jmKWZBxdUmRsQNH5AE22nZCNRiu4XT1HZAzSUYVZCqHCgxRXkbBpdZAb0ZD',
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
    base_url ='www.joyland.com/packages'
    # if type(reply) == str:
    if base_url not in reply:
        message.reply_text(
            text=reply,
        )
    else:
        filename= ""
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





        message.reply_document(
        f"birthday/{filename}",
        # document="invoice.pdf",
        body=filename
        )



    print('pdf send',filename)

# @wa.on_callback_button(CallbackFilter.data_startswith('id'))
# def click_me(client: WhatsApp, clb: CallbackButton):
#     clb.reply_text('You clicked me!')

flask_app.run(port=5003)  # Run the flask app to start the webhook