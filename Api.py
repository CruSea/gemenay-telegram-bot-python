import requests
# import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import time

link = "https://1a04b8ab813b.ngrok.io/"

def getUpdate(bot,channelUserName):
    url = link + "api/issues/approved"
    while(True):
        #update = requests.get(url)
        #update = update.json()
        try:
            update = requests.get(url)
            update = update.json()
            issue = update['issue']
            issueId = update['id']
        except:
            continue
            pass
        try:
            m=update['message']
        except:
            m="pass"

        if m == "no data":
            pass
        else:
            try:
                print(update)
                markup = InlineKeyboardMarkup()
                markup.row_width = 1
                markup.add(InlineKeyboardButton("0 comments", url="t.me/vent_gemenaye_bot?start={}".format(issueId)))
                x=bot.send_message(channelUserName,issue,reply_markup = markup)
                print(x)
                telegramId = x.message_id
                buttonId = 100
                #update database
                #time.sleep(5)
                url2 = link + "api/issues/{}/addDetails".format(issueId)
                print(url2)
                data ={'telegramId' : telegramId,
                        'buttonId' : buttonId}
                x=requests.post(url2,data = data)
                print("dettal")
                print(x)
            #send channel post
            except:
                print("while error")
                time.sleep(10)
                pass
    time.sleep(10)


def addIssue(issue, user_id):
    try:
        url = link + "api/issues"
        data ={'issue' : issue ,'user_id' : user_id}
        print(data)
        x=requests.post(url,data=data)
        print(x)
    except Exception as identifier:
        print("error")
def getIssue(issueId):
    try:
        url= link + "api/issues/{}".format(issueId)
        print(url)
        issue=requests.get(url)
        issue = issue.json()
        return issue['issue']
    except Exception as identifier:
        print("error")


def addComment(issueId,comment,user_id):
    try:
        url = link + "api/issues/{}/comment".format(issueId)
        data = {'comment' : comment, 'user_id' : user_id}
        count=requests.post(url,data=data)
        print(count)
        count = count.json()
        #telegramId = count['telegramId']
        #commNo = count['count']
        return count
    except Exception as identifier:
        print("error")
def bComment(issueId):
    try:
        url = link + "api/issues/{}/comments".format(issueId)
        print(url)
        comm=requests.get(url)
        comm= comm.json()
        return comm
    except Exception as identifier:
        print("error")
#comm
#usi
#isu id

