import json, requests, random, re

from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views import generic
from django.http.response import HttpResponse


facts = {
    'gary facts' : [
        "Gary has a cute pomeranian! But Baron calls it pomeranian from hell...",
    ],
    'mathieu facts' : [
        "Mathieu cannot prounounce Roll!",
    ],
    'gfm facts' : [
        "Bill Gates calls Chuck Norris for tech support, and Chuck Norris calls the GoFundMe happinness team.",
        "Mathieu cannot prounounce Roll.",
        "Gary has a cute pomeranian! But Baron calls it pomeranian from hell...",
        "Jason once won $10,000 at McDonalds and then had to settle for working at Google when the money ran out",
        "Courtney is also a girl's name",
    ],
}

class GaryBotView(generic.View):
    def get(self, request, *args, **kwargs):
        if self.request.GET['hub.verify_token'] == 'thisisgarysecretbot':
            return HttpResponse(self.request.GET['hub.challenge'])
        return HttpResponse("100460735")

    # The get method is the same as before.. omitted here for brevity
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return generic.View.dispatch(self, request, *args, **kwargs)

    # Post function to handle Facebook messages
    def post(self, request, *args, **kwargs):
        # Converts the text payload into a python dictionary
        incoming_message = json.loads(self.request.body.decode('utf-8'))
        # Facebook recommends going through every entry since they might send
        # multiple messages in a single call during high load
        for entry in incoming_message['entry']:
            for message in entry['messaging']:
                # Check to make sure the received call is a message call
                # This might be delivery, optin, postback for other events 
                if 'message' in message:
                    # Print the message to the terminal
                    print message
                    # Assuming the sender only sends text. Non-text messages like stickers, audio, pictures
                    # are sent as attachments and must be handled accordingly. 
                    post_facebook_message(message['sender']['id'], message['message']['text'])
        return HttpResponse()

def post_facebook_message(fbid, recevied_message):
    # Remove all punctuations, lower case the text and split it based on space
    tokens = re.sub(r"[^a-zA-Z0-9\s]",' ',recevied_message).lower().split()
    response_text = ''
    for token in tokens:
        if token in facts:
            response_text = random.choice(facts[token])
            break
    
    response_text = random.choice(facts[recevied_message.lower()])
    if not response_text:
        response_text = "I don't understand! Can you rephrase please?"

    post_message_url = 'https://graph.facebook.com/v2.6/me/messages?access_token=EAAWXRgus2csBAK1yBxDxAyBbfVJF0aZC71woZCCZBH3ItRBwBZCZCsTZB0AK5mudAs8EwI8n5ZAcJhCstBGxTwz4PIlYR8eClIRDSYplhcQy0JG6qPhyD0ZAWiWZBb5lNKtoZAy53DSw7QhaeGUAxlAyD8Of307OIVQbveadvyDKdDXAZDZD' 
    response_msg = json.dumps({"recipient":{"id":fbid}, "message":{"text":response_text}})
    status = requests.post(post_message_url, headers={"Content-Type": "application/json"},data=response_msg)
    print status.json()
