from unicodedata import category
from flask import Flask, request, abort

from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, ImageSendMessage
import json
import requests
from random import randint

app = Flask(__name__)

line_bot_api = LineBotApi('YOUR_CHANNEL_ACCESS_TOKEN')
handler = WebhookHandler('YOUR_CHANNEL_SECRET')

@app.route("/callback", methods=["POST"])
def callback():
    signature = request.headers["X-Line-Signature"]
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print(
            "Invalid signature. Please check your channel access token/channel secret."
        )
        abort(400)

    return "OK"


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    categories = [
        "japanese",
        "teen",
        "groupsex",
        "hardcore",
        "creampie",
        "korean",
        "ukrainian",
        "bukkake",
    ]
    keyword = event.message.text
    if keyword == "有什麼款":
        resp = "現有的類別:\n\n"
        for cat in categories:
            resp += f"{cat}\n"
        resp += "輸入你要的款，或輸入'關燈'隨機抽一張。"
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=resp))

    elif keyword == "關燈":
        p_image_url = get_porn_pic(categories, "random")
        line_bot_api.reply_message(
            event.reply_token,
            ImageSendMessage(
                original_content_url=p_image_url, preview_image_url=p_image_url
            ),
        ),

    else:
        if keyword in categories:
            p_image_url = get_porn_pic(categories, keyword)
            line_bot_api.reply_message(
                event.reply_token,
                ImageSendMessage(
                    original_content_url=p_image_url, preview_image_url=p_image_url
                ),
            ),


def get_porn_pic(categories, keyword):
    if keyword == "random":
        category = categories[randint(0, len(categories) - 1)]
    else:
        category = keyword
    res = requests.get(
        f"https://www.pornpics.com/{category}/?limit=10&offset={randint(1,100)}"
    ).text
    data = json.loads(res)
    return data[randint(0, 9)]["t_url"]


if __name__ == "__main__":
    app.run()
