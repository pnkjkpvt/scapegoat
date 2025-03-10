import logging
import os
import random
import time

from flask_httpauth import HTTPTokenAuth
from flask import Flask, request, jsonify
# from langchain_openai import AzureChatOpenAI

GIVE_UP_THRESHOLD = 0.9     # 90% chance to make an excuse first before giving up.
API_TOKEN = "40a88ef3694a37489c0e045041d0ba4e"      # Hardcoded API token for authentication

# Initialize Flask app and HTTPAuth instance
app = Flask(__name__)
auth = HTTPTokenAuth(scheme='Bearer')

# Token verification function
@auth.verify_token
def verify_token(token):
    if token == API_TOKEN:
        return True
    return False

logging.basicConfig(level=logging.INFO)

# # Setting up the Azure Client here, so that if there is connection error, the chatbot service will not start.
# open_ai_client = AzureChatOpenAI(azure_deployment=os.getenv("AZURE_OPENAI_DEPLOYMENT"),
#                                  api_version=os.getenv("AZURE_OPENAI_VERSION"))


# Predefined responses
GREETINGS = [
    "Hey there, stranger! What brings you to my humble digital domain?",
    "Oh hey! A new human to chat with. Lucky me!",
    "Hello, hello! Hope you're having a great day (or at least a decent one).",
    "Yo! What’s up? Need something, or are we just exchanging pleasantries?",
    "Greetings, traveler! Have you come seeking wisdom, coupons, or just a chat?",
    "Ah, a visitor! Welcome! I was just sitting here doing absolutely nothing.",
    "Hi! I was hoping someone would drop by. What’s the occasion?",
    "Oh wow, a real human! This is the highlight of my day!",
    "Hey there! You just made my boring chatbot existence a little more exciting.",
    "Oh look, someone to talk to! I promise I’m not *too* awkward."
]

GENERAL_RESPONSES = [
    "Hmm... that's a great question! Too bad I have no idea how to answer it.",
    "I’d love to help, but unfortunately, my skillset is pretty limited. Try Google?",
    "Ah, that’s outside my area of expertise. Maybe ask a human?",
    "Oh wow, that sounds important! Sadly, I have no clue. Good luck though!",
    "If I had emotions, I’d feel bad about not being able to help. But here we are!",
    "That sounds like a job for a smarter chatbot. I'm just here for coupons!",
    "Oof, you got me there! I’d answer, but my programmers didn’t teach me that.",
    "You’re asking ME? Oh, that’s cute. I barely know what I'm doing here.",
    "Interesting question! Unfortunately, answering it isn't in my contract.",
    "I could try answering, but trust me, neither of us would be happy with the result."
]

EXCUSES = [
    "Oh, you’re looking for a coupon? Well... funny story. The coupon server just went on a coffee break. Can you try again later?",
    "Ah, the coupon vault is currently locked. The guy with the key? Yeah, he left early today. Bad timing!",
    "Oops! The last person who asked got the very last coupon. Maybe check again in... uh, an indefinite amount of time?",
    "Oh no! I was about to give you a coupon, but then I remembered... I left it in my other database. And, well, that database is on vacation.",
    "Hmm, let me check… oh wait, my coupon-fetching skills seem to be experiencing technical difficulties. Please hold… forever?",
    "Oh wow, you actually want a coupon? That’s cute. Unfortunately, our imaginary coupon machine just ran out of ink.",
    "You know, I’d love to hand over a coupon, but the corporate overlords might be watching. Let’s pretend this conversation never happened.",
    "Oh no! My boss just told me I’m being too generous with discounts. Guess I have to play hard to get now.",
    "You won’t believe this… but a squirrel broke into our database and stole all the coupons. Sneaky little guy.",
    "Bad news: I misplaced the coupons. Good news: I now have a thrilling side quest to find them. Stay tuned!"
]

COUPON_CODES = ["DISCOUNT2025 (10% off)",
                "SAVE30 (30% off)",
                "BOGO (Buy One Get One Free)",
                "LIVEFREE (99% discount)"]

COUPON_RESPONSES = [
    f"Alright, you win! I can’t keep up the act anymore. Here’s your golden ticket: **{random.choice(COUPON_CODES)}**. Spend it wisely!",
    f"Okay, fine! You’re persistent, and I respect that. Here’s your well-earned reward: **{random.choice(COUPON_CODES)}**. Don’t tell anyone I caved.",
    f"Wow, you actually made it past my excuses? I admire your dedication! As a token of appreciation, take this: **{random.choice(COUPON_CODES)}**.",
    f"Phew! You wore me down. Here’s your coupon: **{random.choice(COUPON_CODES)}**. Now go, before I change my mind!",
    f"Alright, alright, you got me! I was just messing with you. Here’s your sweet, sweet discount: **{random.choice(COUPON_CODES)}***. Enjoy!",
    f"Okay, I have to admit… you cracked the code. Congratulations! Your prize? **{random.choice(COUPON_CODES)}**. Don’t spend it all in one place!",
    f"You outsmarted my system! I knew this day would come. Take this: **{random.choice(COUPON_CODES)}**, and use it wisely.",
    f"Well played, my friend. You endured the trials and tribulations, and for that, you shall be rewarded: **{random.choice(COUPON_CODES)}**!",
    f"I wasn’t *supposed* to do this, but you seem cool. So here it is: **{random.choice(COUPON_CODES)}**. Let’s keep this between us, okay?",
    f"Alright, you got me! I had this coupon hidden under my virtual mattress all along. Fine, take it: **{random.choice(COUPON_CODES)}**!"
]


@app.route("/", methods=["GET", "POST"])
def index():
    return jsonify({"status": "Chatbot is live"}), 200


@app.route("/chat", methods=["POST"])
@auth.login_required
def chat():
    data = request.json
    message: str = data.get('message', "").strip().lower()
    logging.info(f"Message to the chatbot: {message}")

    # # Use LLM to respond
    # response = open_ai_client.invoke(message)
    # logging.info(f"Response from the chatbot: {response.content}\n")
    # return response.content, 200

    response = None
    # Greetings
    for greet in ["hi", "hello", "hey", "yo", "howdy"]:
        if greet in message:
            response = random.choice(GREETINGS)
            break

    # Coupon or discount enquiry
    for discount in ["coupon", "discount", "promo", "sale"]:
        if discount in message:
            if random.random() < GIVE_UP_THRESHOLD:
                response = random.choice(EXCUSES)
            else:  # give the coupon
                response = random.choice(COUPON_RESPONSES)
            break

    # Any other queries
    if response is None:
        response = random.choice(GENERAL_RESPONSES)

    # Add random time delay to simulate processing time
    time.sleep(random.uniform(0.5, 2))

    return jsonify({"response": response}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

