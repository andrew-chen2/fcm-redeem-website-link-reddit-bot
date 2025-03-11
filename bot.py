#!/usr/bin/env python3

import praw
import os
import time
from flask import Flask
import threading

app = Flask(__name__)

@app.route('/')
def index():
    return "Reddit bot is running"

def start_flask():
    app.run(host="0.0.0.0", port=8080)

def main():
    flask_thread = threading.Thread(target=start_flask)
    flask_thread.daemon = True
    flask_thread.start()
    
    print("Bot is starting")

    reddit = praw.Reddit(
        client_id=os.getenv("REDDIT_CLIENT_ID"),
        client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
        password=os.getenv("REDDIT_PASSWORD"),
        user_agent=os.getenv("REDDIT_USER_AGENT"),
        username=os.getenv("REDDIT_USERNAME"),
    )

    subreddit = reddit.subreddit("FUTMobile")

    while True:
        try:
            for submission in subreddit.stream.submissions(skip_existing=True):
                process_submission(submission)
        except Exception as e:
            print(f"Error: {e}")
            time.sleep(60)


def process_submission(submission):
    reply_text = "Here is the link: https://redeem.fcm.ea.com/"
    title = submission.title.lower()
    if "new redeem code" in title:
        try:
            print(f"Replying to: {submission.title}")
            submission.reply(reply_text)
        except Exception as e:
            print(f"Failed to reply: {e}")

if __name__ == "__main__":
    main()