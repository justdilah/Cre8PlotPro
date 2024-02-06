import asyncio
from telegram import InlineKeyboardButton, Update, InlineKeyboardMarkup, InputMediaPhoto, ReplyKeyboardRemove,ReplyKeyboardMarkup
import requests
from telegram.ext import filters, MessageHandler, ApplicationBuilder, ContextTypes, CommandHandler, \
    CallbackQueryHandler, CallbackContext, ConversationHandler
import logging
import os


from telegram import __version__ as TG_VER
from cre8ai import receive_post_data

try:
    from telegram import __version_info__
except ImportError:
    __version_info__ = (0, 0, 0, 0, 0)  # type: ignore[assignment]

if __version_info__ < (20, 0, 0, "alpha", 1):
    raise RuntimeError(
        f"This example is not compatible with your current PTB version {TG_VER}. To view the "
        f"{TG_VER} version of this example, "
        f"visit https://docs.python-telegram-bot.org/en/v{TG_VER}/examples.html"
    )

global bot
global TOKEN
TOKEN = "6752671463:AAESLDYm24_zbbNm5cUH11ViBy1v69H4EoY"

PANEL, EDIT, PANEL_ACTIONS, TEXT, TO_PARAPHASE = range(5)

PARAPHASED, DESC, NOT_PARAPHASED = map(chr, range(3))

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    username = update._effective_user.username
    answer = "Hello " + username + "! " + ("🌟 Welcome to the imaginative realm of Cre8PlotPro, "
                                           "where your creativity takes center stage. "
                                           "Unleash the storyteller within using our Telegram chatbot, "
                                           "equipped with advanced AI capabilities for image and text "
                                           "generation, as well as paraphrasing—no artistic skills required. 🤖✨\n\n"
                                           "Cre8PlotPro Usage:\n\nAnswer the questions posed by our Telegram chatbot! 🤔\n\n"
                                           "1. Start your experience by typing /begin\n\n"
                                           "2. Visualize a scene and describe it to our bot—watch as it transforms your ideas into captivating visuals. "
       "🎨e.g., 'a girl with curly hair eating bread.'\n\n"
                                           "3. Craft the perfect text caption to accompany your image panel. 📝 e.g., 'This bread is delicious!'\n\n"
                                           "4. Need a grammar check and an alternative sentence? Opt for paraphrasing with a simple 'Yes' when prompted. 🔄\n\n"
                                           "5. Save your diverse panels and effortlessly share your visual tales on any social media platform you fancy. 🌐\n\n"
                                           "Note: Type /cancel to abort\n\n"
                                           "Happy Storytelling! 🚀✨")


    await update.message.reply_text(
        answer
    )

async def provideDesc(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global counter
    counter = 1
    answer = "Please describe the scene and characters for this panel."
    await update.message.reply_text(
        answer
    )

    return TEXT

async def provideText(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global desc_user
    desc_user = update.message.text
    answer = "Please input the text caption you would like to accompany your image panel. "
    await update.message.reply_text(
        answer
    )
    return PANEL
async def showPanel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    global counter, desc_user, text_user
    username = update._effective_user.username
    await update.message.reply_text(
        "Please wait for the panel to be generated.."
    )
    text_user = update.message.text
    # url = 'http://127.0.0.1:8000/'

    myobj = {
                "username": username,
                "panel": counter,
                "description": desc_user,
                "text": text_user,
                "paraphase": 0
        }

    x = receive_post_data(myobj)
    print(x)
    await asyncio.sleep(5)  # Async sleep
    text = (
        "# Panel " + str(counter) + " has been created successfully \n\nWould you like to paraphrase your text caption?"
    )

    buttons = [
        [
            InlineKeyboardButton(text="Yes", callback_data=str(PARAPHASED)),
            InlineKeyboardButton(text="No", callback_data=str(NOT_PARAPHASED)),
        ],
    ]
    keyboard = InlineKeyboardMarkup(buttons)

    # folder_to_remove = "telebotcre8AI"
    # relative_path = os.path.relpath(os.getcwd(), os.path.join(os.getcwd(), folder_to_remove))
    # new_absolute_path = os.path.abspath(relative_path)

    await update.message.reply_photo(photo=os.path.abspath(os.getcwd()) + '\output\\panel-' + str(counter) + '-'+ username +'.png', caption=text, reply_markup=keyboard)

    return PANEL_ACTIONS

async def panelActionsCallBack(update: Update, context: CallbackContext):
    choice = update.callback_query.data
    global counter, desc_user, text_user
    username = update._effective_user.username

    if choice == PARAPHASED:
        # url = 'http://127.0.0.1:8000/'

        myobj = {
            "username": username,
            "panel": counter,
            "description": desc_user,
            "text": text_user,
            "paraphase": 1
        }

        x = receive_post_data(myobj)
        print(x)
        await asyncio.sleep(8)  # Async sleep

        if counter == 4:
            text = "You have successfully created all the panels. Please view it in the output folder. \n\nGoodbye, hope to see you again :)"
            # folder_to_remove = "telebotcre8AI"
            # # relative_path = os.path.relpath(os.getcwd(), os.path.join(os.getcwd(), folder_to_remove))
            # # new_absolute_path = os.path.abspath(relative_path)

            file = InputMediaPhoto(
                media=open(os.path.abspath(os.getcwd()) + '\output\\panel-' + str(counter) + '-'+ username +'.png', 'rb'),
                caption=text)
            await update.callback_query.edit_message_media(file)
            return ConversationHandler.END

        text = "# Panel " + str(counter) + " has been created successfully \n\nPlease describe the scene and characters for the next panel."

    elif choice == NOT_PARAPHASED:
        text = "# Panel " + str(counter) + " has been created successfully \n\nPlease describe the scene and characters for the next panel. "

    # folder_to_remove = "telebotcre8AI"
    # relative_path = os.path.relpath(os.getcwd(), os.path.join(os.getcwd(), folder_to_remove))
    # new_absolute_path = os.path.abspath(relative_path)

    file = InputMediaPhoto(media=open(os.path.abspath(os.getcwd()) + '\output\\panel-' +str(counter) + '-'+ username +'.png','rb'), caption=text)
    await update.callback_query.edit_message_media(file)

    counter += 1
    return TEXT

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    await update.message.reply_text(
        "Bye! I hope we can talk again some day.\n\nYou may start your experience again by typing /start", reply_markup=ReplyKeyboardRemove()
    )

    return ConversationHandler.END

def main():
    mode = os.environ.get("MODE", "polling")

    application = ApplicationBuilder().token(TOKEN).build()
    start_handler = CommandHandler('start', start)

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("begin", provideDesc)],
        states={
            TEXT: [MessageHandler(filters.TEXT,provideText)],
            PANEL: [MessageHandler(filters.TEXT,showPanel)],
            DESC: [CallbackQueryHandler(provideDesc)],
            PANEL_ACTIONS: [CallbackQueryHandler(panelActionsCallBack)]
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    application.add_handler(start_handler)
    application.add_handler(conv_handler)
    application.run_polling()


if __name__ == '__main__':
    main()
