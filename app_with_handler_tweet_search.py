# -*- coding: utf-8 -*-

#  Licensed under the Apache License, Version 2.0 (the "License"); you may
#  not use this file except in compliance with the License. You may obtain
#  a copy of the License at
#
#       https://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#  WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#  License for the specific language governing permissions and limitations
#  under the License.

import os
import sys
from argparse import ArgumentParser

from flask import Flask, request, abort
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

import app

########################
#added by nanamisawa

import json, config
from requests_oauthlib import OAuth1Session

def search_tweets(_keyword):

    CK = config.CONSUMER_KEY
    CS = config.CONSUMER_SECRET
    AT = config.ACCESS_TOKEN
    ATS = config.ACCESS_TOKEN_SECRET
    twitter = OAuth1Session(CK, CS, AT, ATS)    # 認証
    
    url = "https://api.twitter.com/1.1/search/tweets.json"
    params = {'q' : _keyword, 'count' : 5}
    req = twitter.get(url, params = params)
    
    if req.status_code == 200:
        search_timeline = json.loads(req.text)
        for tweet in search_timeline['statuses']:
            with open("tweet_contents.text","a") as f:
                f.write('---------------------------------------------------\n')
                f.write(tweet['user']['name'] + '::' + tweet['text'] + '\n') 
                f.write(tweet['created_at'] + '\n')
                f.write('---------------------------------------------------\n')
    else:
        print("ERROR: %d" % req.status_code)


    text = ""
    with open("tweet_contents.text","r") as f:
        text = f.read()
    return(text)

#added by nanamisawa
########################


app = Flask(__name__)

# get channel_secret and channel_access_token from your environment variable
#channel_secret = os.getenv('LINE_CHANNEL_SECRET', None)
#channel_access_token = os.getenv('LINE_CHANNEL_ACCESS_TOKEN', None)
channel_secret = '0f86b69f0a800dd187cc698c1405a6be'
channel_access_token = 'Yd3v4gGnu6m7E/xYVP5fedy23cGyRtZinOipora4+qpOROaZJMAHQTzQB1jP/V0miUFHuolbxZ8LX3UNY+c5XJpX382kEQEdSHSojK8/u/tbzChaCVujPBPUyt0Eq+S1ox6F9oW2obixnetWDbTydwdB04t89/1O/w1cDnyilFU='
if channel_secret is None:
    print('Specify LINE_CHANNEL_SECRET as environment variable.')
    sys.exit(1)
if channel_access_token is None:
    print('Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.')
    sys.exit(1)

line_bot_api = LineBotApi(channel_access_token)
handler = WebhookHandler(channel_secret)


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'



@handler.add(MessageEvent, message=TextMessage)
def message_text(event):

########################
#added by nanamisawa

    if "#" in event.message.text:
        text=event.message.text
        global keyword
        keyword = text.replace("#","")
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=keyword+" を追加しました。 ")
        )

    else:
        text=search_tweets(keyword)
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text = text )
        )

        f = open("tweet_contents.text","w")


#added by nanamisawa
########################


if __name__ == "__main__":
    keyword="" #added by nanamisawa
    arg_parser = ArgumentParser(
        usage='Usage: python ' + __file__ + ' [--port <port>] [--help]'
    )
    arg_parser.add_argument('-p', '--port', default=8000, help='port')
    arg_parser.add_argument('-d', '--debug', default=False, help='debug')
    options = arg_parser.parse_args()

    app.run(debug=options.debug, port=options.port)
