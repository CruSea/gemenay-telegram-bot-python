#!/usr/bin/env python3
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from telebot import types
from _thread import *
import Api

userStep = {}
TOKEN = '1106406965:AAERNIQapZhDd3zHxKmQztjsjaVFrV691xk'
channelUserName= '@vent_gemenaye'
bot = telebot.TeleBot(TOKEN)
issueIds = {}
issueAll = {}
delete ={}


#start_new_thread( Api.getUpdate,(bot,channelUserName))


def buttonVent(ids,numOfComment):
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    markup.add(InlineKeyboardButton("{} comments".format(numOfComment), url="t.me/vent_gemenaye_bot?start={}".format(ids)))
    return markup

def buttonStart():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row_width = 2
    markup.add('🔆 Start a Vent', '💡 Help', '⚙️ Settings', '👥 About Us')
    return markup

def cancel():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row_width = 1
    markup.add('❌ Cancel')
    return markup

def buttonComment(unique_code):
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    markup.add(InlineKeyboardButton("Add a comment", callback_data="Add_a_comment--"+unique_code),
                InlineKeyboardButton("Browse comments", callback_data="Browse_comments--"+unique_code))
    return markup

def like():
    markup = InlineKeyboardMarkup()
    markup.row_width = 3
    markup.add(InlineKeyboardButton("👍 like", callback_data="like"),
                InlineKeyboardButton("↪️reply", callback_data="reply"),
                InlineKeyboardButton("👎dislike", callback_data="dislike"))
    return markup

def mentor():
    markup = InlineKeyboardMarkup()
    markup.row_width =1
    markup.add(InlineKeyboardButton("yes, I do", callback_data="mentor"),
                InlineKeyboardButton("no, I don't", callback_data="no"))
    return markup

def categoryButton():
    try:
        markup = InlineKeyboardMarkup()
        markup.row_width = 1
        category = Api.category()
        for c in category:
            markup.add(InlineKeyboardButton(c['name'], callback_data="category--"+str(c['id'])))
        return markup
    except Exception as identifier:
        print(identifier)


def get_user_step(uid):
    if uid in userStep:
        return userStep[uid]
    else:
        return 0

def sendVentToChannel(vent ,ventId):
    x=bot.send_message(channelUserName,vent,reply_markup = buttonVent(ventId,0))
    print(x.message_id)

def editCommentButton(messageId,ventId,numOfComment):
    bot.edit_message_reply_markup(channelUserName,messageId,reply_markup = buttonVent(ventId,numOfComment))

#sendVentToChannel(vent ,ventId)
#editButton()


def extract_unique_code(text):
    # Extracts the unique_code from the sent /start command.
    return text.split()[1] if len(text.split()) > 1 else None

@bot.message_handler(commands=['start'])
def send_welcome(message):
    try:
        uid = message.chat.id
        userStep[uid] = 0
        unique_code = extract_unique_code(message.text)
        if unique_code:
            issue=Api.getIssue(unique_code)
            bot.send_message(uid,str(issue),reply_markup = buttonComment(unique_code))
        else:
            bot.send_message(uid,"Welcome to vent gemenaye",reply_markup = buttonStart())
    except:
        pass


try:

    @bot.callback_query_handler(func=lambda call: True)
    def callback_query(call):
        try:
            uid=call.from_user.id
            text = str(call.data)
            text = text.split("--")
            if text[0] == "Add_a_comment":
                bot.answer_callback_query(call.id, "send your comment")
                bot.send_message(uid,"Add comment...",reply_markup = cancel())
                issueIds[0] = int(text[1])
                userStep[uid] = 2
            elif text[0] == "Browse_comments":
                #issueIds[0] = int(text[1]);
                #print(call)
                bot.answer_callback_query(call.id, "comment coming up")
                comm=Api.bComment(text[1])
                try:
                    i=0
                    for ids in comm:
                        bot.send_message(uid, comm[i]['comment'],reply_markup= like())
                        i=i+1
                except:
                    bot.send_message(uid,"No comment.....",reply_markup = buttonStart())

            elif text[0] == "category":
                Api.addIssue(issueAll[uid], uid,text[1])
                bot.send_message(uid,"issue added! wait for approval",reply_markup = buttonStart())
                xy=bot.send_message(uid,"Do You need MENTOR",reply_markup = mentor())
                delete[uid] = xy
            elif text[0] == "mentor":
                bot.delete_message(uid,delete[uid].message_id)
                bot.send_message(uid,"We have recived your information and we will contact you soon")
            elif text[0] == "no":
                bot.delete_message(uid,delete[uid].message_id)
                bot.send_message(uid,"Thank you")



        except Exception as identifier:
            print(identifier)
    @bot.message_handler(func=lambda message: get_user_step(message.chat.id) == 1)
    def submitIssue(m):
        try:
            uid = m.chat.id
            text = m.text
            if text == '❌ Cancel' :
                bot.send_message(uid,"cancelled!",reply_markup = buttonStart())
                userStep[uid] = 0
            else:
                issueAll[uid]= text
                x=categoryButton()
                bot.send_message(uid,"Please select category that relate to your issue",reply_markup = x)
                userStep[uid] = 0
        except:
            pass

    @bot.message_handler(func=lambda message: get_user_step(message.chat.id) == 2)
    def addComment(m):
        try:
            uid = m.chat.id
            text = m.text
            if text == '❌ Cancel' :
                bot.send_message(uid,"cancelled!",reply_markup = buttonStart())
                userStep[uid] = 0
            else:
                count = Api.addComment(issueIds[0],text,uid)
                telegramId = count['telegramId']
                print(telegramId)
                commNo = count['count']
                editCommentButton(telegramId,issueIds[0],commNo)
                bot.send_message(uid, "Comment added",reply_markup = buttonStart())
                userStep[uid] = 0
        except Exception as identifier:
            print(identifier)


    @bot.message_handler(func=lambda message: True, content_types=['text'])
    def command_default(m):
        try:
            uid = m.chat.id
            text = m.text
            if text == "🔆 Start a Vent":
                bot.send_message(uid, "Please send your issue.",reply_markup = cancel())
                userStep[uid] = 1
            elif text=="💡 Help":
                bot.send_message(uid, '''Hey 👋 I'm Gemenaye Bot.
You can control me By sending this commands:
/start  - Hellps to start a bot or bring the main menu''')
            elif text=="👥 About Us":
                bot.send_message(uid, '''ለምን ብቻዎትን ይጨነቃሉ? እኛም ገመና አልን ገመናዎትን ያካፍሉን።
አንተ ባለፍክበት ያለፈ ሰው አለ
ማንነቶ ሳይታወቅ (ሳይገለጸ)  እዚህ አማካሪ  ያናግሩ ።''')
            elif text == '❌ Cancel' :
                bot.send_message(uid,"cancelled!",reply_markup = buttonStart())

        except:
            pass
except Exception as identifier:
        print("error")




bot.polling()
