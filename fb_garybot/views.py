import json, requests, random, re
from pprint import pprint

from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views import generic
from django.http.response import HttpResponse

ACCESS_TOKEN = 'EAAWXRgus2csBAFpHBukNcnxIVND4f2wxIHBIfAmz1eoPn7t3Ic2UeN2FJppmbtJeYdDnkcpADMl4DKC85yE37IDJWugsKDTZAXZBDVMq5fYwDiJVW2y4WHSpqQ9ppZAxlrLcDykWAWWrNoC4MCsdSv8GxwACLgXS2ERQ40ceAZDZD'

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
    # user data
    user_details_url = "https://graph.facebook.com/v2.6/%s"%fbid
    user_details_params = {
        'fields':'first_name,last_name,profile_pic,locale,timezone,gender',
        'access_token': ACCESS_TOKEN
    }
    user_details = requests.get(user_details_url, user_details_params).json()

    # persist menu
    persist_menu_url = "https://graph.facebook.com/v2.6/me/thread_settings?access_token=%s" % ACCESS_TOKEN
    persist_status = requests.post(
        persist_menu_url,
        headers={"Content-Type": "application/json"},
        data=persist_menu_data)
    pprint(persist_status.json())

    # user text input
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
    elif 'hello' in tokens:
        response_text = 'Hello ' + user_details['first_name'] + '! How are you feeling today?'
    elif 'pokemon' in tokens:
        response_text = 'There are 250 pokemons in total.'
    elif 'about' in tokens and 'me' in tokens:
        if user_details['gender'] == 'male':
            flower_text = 'handsome man!'
        else:
            flower_text = 'pretty girl!'
        response_text = 'Hello %s %s, i believe you are a %s' % (user_details['first_name'], user_details['last_name'], flower_text)
    elif 'thank' in tokens or 'thanks' in tokens:
        response_text = "You're welcome!"
    elif 'nearby' in tokens:
        response_medium = 'template'
        response_variant = 'nearby'
    # TODO: COMPLETE TRENDING DATA
    elif 'trending' in tokens:
        response_medium = 'template'
        response_variant = 'trending'
    elif 'random' in tokens or 'campaign' in tokens:
        response_medium = 'random'
        response_variant = 'random'
        fund_ids = [11612547, 11945897, 11202935, 12896155, 11155025, 11400025, 11400023, 11400033, 11400031, 11400035, 11400037, 11400039, 11400019, 11400017, 11400015, 11400013, 11400007]
        random_fund_id = fund_ids[random.randint(0, len(fund_ids)-1)]
        fund = requests.get('http://192.168.3.79/funds/v1/funds/%s' % random_fund_id).json()
    elif 'login' in tokens:
        
        login_params = {
            "recipient" : {
                "id":fbid
            },
            "message" : {
                "attachment" : {
                    "type" : "template",
                    "payload" : {
                        "template_type" : "generic",
                        "elements" : [{
                            "title" : "Welcome to GoFundMe",
                            "image_url" : "http://a3.mzstatic.com/us/r30/Purple60/v4/fe/ad/29/fead29c2-f5e1-55ea-7e12-9ce64ba3a12c/icon175x175.png",
                            "buttons" : [{
                                "type" : "account_link",
                                "url" : "https://gofundme.com/oauth/authorize"
                            }]
                        }]
                    }
                }
            }
        }
    elif not response_text:
        response_text = "Sorry " + user_details['first_name'] + ", I don't understand that. Can you rephrase please?"
    
    post_message_url = 'https://graph.facebook.com/v2.6/me/messages?access_token=%s' % ACCESS_TOKEN
    if response_medium == 'text':
        response_msg = json.dumps({
            "recipient" : {
                "id":fbid
            },
            "message":{
                "text":response_text
            }
        })
        status = requests.post(post_message_url, headers={"Content-Type": "application/json"},data=response_msg)
        pprint(status.json())
    elif response_medium == 'template':
        variant_data = {
            "trending" : trending_data,
            "nearby"   : nearby_data,
            "login" : {
                "attachment" : {
                    "type" : "template",
                    "payload" : {
                        "template_type" : "generic",
                        "elements" : [{
                            "title" : "Welcome to GoFundMe",
                            "image_url" : "http://a3.mzstatic.com/us/r30/Purple60/v4/fe/ad/29/fead29c2-f5e1-55ea-7e12-9ce64ba3a12c/icon175x175.png",
                            "buttons" : [{
                                "type" : "account_link",
                                "url" : "https://www.example.com/oauth/authorize"
                            }]
                        }]
                    }
                }
            },
        }
        response_msg = json.dumps({
            "recipient" : {
                "id" : fbid
            }, 
            "message" : variant_data[response_variant]
        })
        status = requests.post(post_message_url, headers={"Content-Type": "application/json"},data=response_msg)
        pprint(status.json())
    elif response_medium == 'profile':
        pass
    elif response_medium == 'random':
        variant_data = {
            "random"   : {
                "attachment" : {
                    "type" : "template",
                    "payload" : {
                        "template_type": "generic",
                        "elements" : [
                            {
                                "title" : fund['name'],
                                "image_url" : fund['main_image_url'],
                                "subtitle" : "$%s raised" % fund['balance'],
                                "buttons" : [
                                    {
                                        "type" : "web_url",
                                        "url" : "https://gofundme.com/%s" % fund['url'],
                                        "title" : "View Website"
                                    },
                                    {
                                        "type":"postback",
                                        "title":"Donate",
                                        "payload":"USER_DEFINED_PAYLOAD"
                                    }
                                ]
                            },
                        ]
                    }
                }
            }
        }
        response_msg = json.dumps({
            "recipient" : {
                "id" : fbid
            }, 
            "message" : variant_data[response_variant]
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

persist_menu_data = {
    "setting_type" : "call_to_actions",
    "thread_state" : "existing_thread",
    "call_to_actions" : [
        {
            "type" : "web_url",
            'title' : "Go to gofundme.com",
            "url" : "https://gofundme.com"
        }
    ]
}
trending_data = {
    "attachment" : {
                    "type" : "template",
                    "payload" : {
                        "template_type": "generic",
                        "elements" : [
                            {
                                "title" : "Help Abbey",
                                "image_url" : "https://44cd8574c19e363b1af4-9bfca67f877491754ae0570b8c65e031.ssl.cf1.rackcdn.com/12986735_fb_1468690566.7082_funds.jpg",
                                "subtitle" : "$17,561 raised",
                                "buttons" : [
                                    {
                                        "type" : "web_url",
                                        "url" : "https://gofundme.com/2erpq24",
                                        "title" : "View Website"
                                    }
                                ]
                            },
                            {
                                "title" : "Miracles for Madison",
                                "image_url" : "https://44cd8574c19e363b1af4-9bfca67f877491754ae0570b8c65e031.ssl.cf1.rackcdn.com/13092563_1469026002.3389.jpg",
                                "subtitle" : "$33,744 raised",
                                "buttons" : [
                                    {
                                        "type" : "web_url",
                                        "url" : "https://gofundme.com/2fh63ng",
                                        "title" : "View Website"
                                    }
                                ]
                            },
                            {
                                "title" : "Journey's Vetinary Treatment",
                                "image_url" : "https://44cd8574c19e363b1af4-9bfca67f877491754ae0570b8c65e031.ssl.cf1.rackcdn.com/13126551_14691278120_r.jpg",
                                "subtitle" : "$4,704 raised",
                                "buttons" : [
                                    {
                                        "type" : "web_url",
                                        "url" : "https://gofundme.com/journeysvet",
                                        "title" : "View Website"
                                    }
                                ]
                            },
                            {
                                "title" : "Save Hank and Helen's Home",
                                "image_url" : "https://44cd8574c19e363b1af4-9bfca67f877491754ae0570b8c65e031.ssl.cf1.rackcdn.com/11915301_1464909751.0069.jpg",
                                "subtitle" : "$29,407 raised",
                                "buttons" : [
                                    {
                                        "type" : "web_url",
                                        "url" : "https://gofundme.com/27m9zvn3",
                                        "title" : "View Website"
                                    }
                                ]
                            },
                            {
                                "title" : "give Cole Kinney proper rest",
                                "image_url" : "https://44cd8574c19e363b1af4-9bfca67f877491754ae0570b8c65e031.ssl.cf1.rackcdn.com/13120919_1469113107.8816.jpg",
                                "subtitle" : "$20,680 raised",
                                "buttons" : [
                                    {
                                        "type" : "web_url",
                                        "url" : "https://gofundme.com/2fnznzjs",
                                        "title" : "View Website"
                                    }
                                ]
                            },
                            {
                                "title" : "Please donate @ we stand with Gaspar",
                                "image_url" : "https://44cd8574c19e363b1af4-9bfca67f877491754ae0570b8c65e031.ssl.cf1.rackcdn.com/12979619_1468642068.6079.jpg",
                                "subtitle" : "$5,871 raised",
                                "buttons" : [
                                    {
                                        "type" : "web_url",
                                        "url" : "https://gofundme.com/2eqxq3ss",
                                        "title" : "View Website"
                                    }
                                ]
                            },
                            {
                                "title" : "Help Chance Pay for School",
                                "image_url" : "https://44cd8574c19e363b1af4-9bfca67f877491754ae0570b8c65e031.ssl.cf1.rackcdn.com/12984905_1468677139.3091.jpg",
                                "subtitle" : "$1,891 raised",
                                "buttons" : [
                                    {
                                        "type" : "web_url",
                                        "url" : "https://gofundme.com/helpchanceplz",
                                        "title" : "View Website"
                                    }
                                ]
                            }
                        ]
                    }
                }
}
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
