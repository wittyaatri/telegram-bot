#!/usr/bin/env python

import openai
import logging

from telegram import __version__ as TG_VER

try:
    from telegram import __version_info__
except ImportError:
    __version_info__ = (0, 0, 0, 0, 0)  # type: ignore[assignment]

if __version_info__ < (20, 0, 0, "alpha", 1):
    raise RuntimeError(
        f"This example is not compatible with your current PTB version {TG_VER}. To view the "
        f"{TG_VER} version of this example, "
    )
from telegram import ForceReply, Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# OpenAI
openai.api_key = "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"

# Define the function to generate the travel itinerary


def generate_itinerary(place, days):
    # Define the OpenAI prompt
    # prompt = f"Give {days} day travel itinerary for {place}"
    prompt = f"Create a {days}-day travel itinerary for {place}. Include some popular tourist attractions, such as museums, parks, and historical landmarks. Also recommend some local food and shopping options. Include time of the day to visit places and distance as feasibility to reach places is improtant"
    print(prompt)
    # Set the OpenAI model engine
    model_engine = "text-davinci-003"

    # Call the OpenAI API to generate the itinerary
    response = openai.Completion.create(
        engine=model_engine,
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.7,
    )

    # Return the generated itinerary text
    return response.choices[0].text.strip()


# Define a few command handlers. These usually take the two arguments update and
# context.
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    await update.message.reply_html(
        rf"Hi {user.mention_html()}! 😄 Welcome to Wittyatri, your travel Itinerary Bot! Please enter the place & number of days you plan to visit in the mentioned format. 'Mumbai, 3'",
        reply_markup=ForceReply(selective=True),
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    await update.message.reply_text("Help!")


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Handle checks for right input format for Place and Days
    print(update.message.text)
    if str(update.message.text).lower() == 'hi' or str(update.message.text).lower() == 'hello':
        print("here")
        await update.message.reply_html(
            rf"😄 Welcome to Wittyatri, your travel Itinerary Bot! Please enter the place & number of days you plan to visit in the mentioned format. 'Mumbai, 3'",
            reply_markup=ForceReply(selective=True),
        )

    # elif type(update.message.text) == str:
    #     reply = "Alrighty! please use the command /start to get started"
    #     await update.message.reply_text(reply)
    else:
        try:
            user_input = list(update.message.text.split(','))
            print(user_input)
            place = user_input[0]
            days = int(user_input[1])
            print(place, days)
            # prompt = f"Give {days} day travel itinerary for {place}" # what could be more effective prompt? discuss with ABC
            # print(prompt)
            response = generate_itinerary(place, days)
            # print(response)
            await update.message.reply_text(response)
        except:
            # dirty code
            reply = "Alrighty! please use the command /start to get started"
            await update.message.reply_text(reply)


async def about(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /about is issued."""
    await update.message.reply_text("Planning a trip? Let our itinerary bot be your travel assistant! Get personalized recommendations for the places you want to visit and things to do based on your preferences. Plus, our bot makes real-time adjustments to your itinerary, so you don't have to worry about changes in your plans. visit: www.wittyatri.com")


def main() -> None:
    """Start the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(
        "6152369425:AAFs_1_DwRVYJIbOkCPrO4FRfl7RKjCSy4I").build()

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("about", about))

    # on non command i.e message - echo the message on Telegram     #Buggy handle the other inputs
    # Handle hi, Hello input
    # For all other cases, send a generic message about how this works?
    application.add_handler(MessageHandler(
        filters.TEXT & ~filters.COMMAND, echo))

    # Run the bot until the user presses Ctrl-C
    application.run_polling()


if __name__ == "__main__":
    main()
