import json, requests, random, re
from pprint import pprint

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
def post_facebook_message(fbid, recevied_message):
    user_details_url = "https://graph.facebook.com/v2.6/%s"%fbid
    user_details_params = {
        'fields':'first_name,last_name,profile_pic',
        'access_token':'EAAWXRgus2csBAFpHBukNcnxIVND4f2wxIHBIfAmz1eoPn7t3Ic2UeN2FJppmbtJeYdDnkcpADMl4DKC85yE37IDJWugsKDTZAXZBDVMq5fYwDiJVW2y4WHSpqQ9ppZAxlrLcDykWAWWrNoC4MCsdSv8GxwACLgXS2ERQ40ceAZDZD'
    }
    user_details = requests.get(user_details_url, user_details_params).json()
    response_medium = 'text'
    # Remove all punctuations, lower case the text and split it based on space
    tokens = re.sub(r"[^a-zA-Z0-9\s]",' ',recevied_message).lower().split()
    response_text = ''
    for token in tokens:
        if token in facts:
            response_text = random.choice(facts[token])
            break
    if recevied_message in facts:
        response_text = random.choice(facts[recevied_message.lower()])
    elif recevied_message.lower() == 'hello':
        response_text = 'Hello ' + user_details['first_name'] + '! How are you feeling today?'
    elif 'pokemon' in tokens:
        response_text = 'There are 250 pokemons in total.'
    elif 'nearby' in tokens:
        response_text = 'there are 12 campaigns near your location.'
        response_medium = 'template'
    elif not response_text:
        response_text = "Sorry " + user_details['first_name'] + ", I don't understand that. Can you rephrase please?"
    
    post_message_url = 'https://graph.facebook.com/v2.6/me/messages?access_token=EAAWXRgus2csBALfz5S21sFpZAchEEuYHiCo8OwzViHzFIrXs06zdFzuN1HskDAVoe1OFxG7JTZBRQ0imQjZApZA7IjjQS4UZAKgbBWSiiXaZBfokVNwMlHyMqfSXpxm3WuBT7kiZBL0hdh8WDz09JloZCbnEbBZAKAZAZC9RuqnWJEZBlAZDZD'
    if response_medium == 'text':
        response_msg = json.dumps({"recipient":{"id":fbid}, "message":{"text":response_text}})
        # status = requests.post(post_message_url, headers={"Content-Type": "application/json"},data=response_msg)
        # pprint(status.json())
    elif response_medium == 'template':
        response_msg = json.dumps({
            "recipient" : {
                "id" : fbid
            }, 
            "message" : nearby_data
        })
    status = requests.post(post_message_url, headers={"Content-Type": "application/json"},data=response_msg)
    pprint(status.json())



class GaryBotView(generic.View):
    def get(self, request, *args, **kwargs):
        if self.request.GET['hub.verify_token'] == 'mytoken':
            return HttpResponse(self.request.GET['hub.challenge'])
        return HttpResponse("Error, invalid token")

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
                    pprint(message)
                    # Assuming the sender only sends text. Non-text messages like stickers, audio, pictures
                    # are sent as attachments and must be handled accordingly. 
                    if 'text' in message['message']:
                        post_facebook_message(message['sender']['id'], message['message']['text'])
        return HttpResponse()


nearby_data = {
                "attachment" : {
                    "type" : "template",
                    "payload" : {
                        "template_type": "generic",
                        "elements" : [
                            {
                                "title" : "Help with our beloved Slinky's care",
                                "image_url" : "https://44cd8574c19e363b1af4-9bfca67f877491754ae0570b8c65e031.ssl.cf1.rackcdn.com/3290051_1423504948.6735.jpg",
                                "subtitle" : "$1,550 raised",
                                "buttons" : [
                                    {
                                        "type" : "web_url",
                                        "url" : "https://gofundme.com/terrywilliams",
                                        "title" : "View Website"
                                    }
                                ]
                            },
                            {
                                "title" : "Send Aria to Skylar Hadden School",
                                "image_url" : "https://44cd8574c19e363b1af4-9bfca67f877491754ae0570b8c65e031.ssl.cf1.rackcdn.com/4094727_1428801272.384_app.png",
                                "subtitle" : "$700 raised",
                                "buttons" : [
                                    {
                                        "type" : "web_url",
                                        "url" : "https://gofundme.com/ariaskylarhadden",
                                        "title" : "View Website"
                                    }
                                ]
                            },
                            {
                                "title" : "National Championships - Quakes PDA 01",
                                "image_url" : "https://44cd8574c19e363b1af4-9bfca67f877491754ae0570b8c65e031.ssl.cf1.rackcdn.com/5111750_1435609235.3543.jpg",
                                "subtitle" : "$2,985 raised",
                                "buttons" : [
                                    {
                                        "type" : "web_url",
                                        "url" : "https://gofundme.com/quakespda",
                                        "title" : "View Website"
                                    }
                                ]
                            },
                            {
                                "title" : "FHO Surgery and Spay for Munroe",
                                "image_url" : "https://44cd8574c19e363b1af4-9bfca67f877491754ae0570b8c65e031.ssl.cf1.rackcdn.com/4620009_1431964172.847.jpg",
                                "subtitle" : "$1,380 raised",
                                "buttons" : [
                                    {
                                        "type" : "web_url",
                                        "url" : "https://gofundme.com/helpmunroe",
                                        "title" : "View Website"
                                    }
                                ]
                            },
                            {
                                "title" : "Fund Raiser in Denise Memory",
                                "image_url" : "https://44cd8574c19e363b1af4-9bfca67f877491754ae0570b8c65e031.ssl.cf1.rackcdn.com/11166197_1462397274.2684.jpg",
                                "subtitle" : "$3,575 raised",
                                "buttons" : [
                                    {
                                        "type" : "web_url",
                                        "url" : "https://gofundme.com/22nntgh4",
                                        "title" : "View Website"
                                    }
                                ]
                            }
                        ]
                    }
                }
            }
