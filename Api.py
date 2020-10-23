import requests
#import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import time

link = "http://159.65.230.4:3000/"

def getUpdate(bot,channelUserName):
    url = link + "api/issues/approved"
    while(True):
        #update = requests.get(url)
        #update = update.json()
        try:
            update = requests.get(url)
            #print(update)
            update = update.json()
            issue = update['issue'] + '''
#'''+update['category']['name']
            issueId = update['id']
        except Exception as identifier:
            #print(identifier)
            time.sleep(10)
            continue
        try:
            m=update['message']
        except:
            m = "pass"

        if m == "no data":
            pass
        else:
            try:
                markup = InlineKeyboardMarkup()
                markup.row_width = 1
                markup.add(InlineKeyboardButton("0 comments", url="t.me/vent_gemenaye_bot?start={}".format(issueId)))
                x=bot.send_message(channelUserName,issue,reply_markup = markup)
                #facebook
                url3 = "https://graph.facebook.com/v8.0/102531171655135/feed"
                access_token ="EAAK4Jr5HVCkBAPZA0qoSmi3BQbZBGHr5O6SJmmzclcZAksaqTkHrVIYZC2Giw32GSvYJsMaDSROB5C0Tytbi950ZBSGUxlfQSeNRZCRBRmKrpxx5GwxnsC53ILXwD7zEA2OZBbKuTFzwJE9R4rRbQG9qzZAZAjvxtMf0LCZCofpQORH4ZBYp1EPjTGN"

                data ={'message' : issue,
                        'access_token' : access_token}
                requests.post(url3,data)
                #end facebook
                telegramId = x.message_id
                buttonId = 100
                #update database
                time.sleep(5)
                url2 = link + "api/issues/{}/addDetails".format(issueId)
                data ={'telegramId' : telegramId,
                        'buttonId' : buttonId}
                x=requests.post(url2,data = data)
            except Exception as identifier:
                print(identifier)
                time.sleep(10)
    time.sleep(10)

def addIssue(issue, user_id,categoryId):
    try:
        url = link + "api/issues"
        data ={'issue' : issue ,'user_id' : user_id, 'categoryId' : categoryId}
        requests.post(url,data=data)
    except Exception as identifier:
        print("error")
def getIssue(issueId):
    try:
        url= link + "api/issues/{}".format(issueId)
        #print(url)
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
        #print(count)
        count = count.json()
        #telegramId = count['telegramId']
        #commNo = count['count']
        return count
    except Exception as identifier:
        print("error")
def bComment(issueId):
    try:
        url = link + "api/issues/{}/comments".format(issueId)
        #print(url)
        comm=requests.get(url)
        comm= comm.json()
        return comm
    except Exception as identifier:
        print("error")


def category():
    try:
        url = link + "api/categories"
        #print(url)
        cata=requests.get(url)
        cata= cata.json()
        #print(cata)
        return cata
    except Exception as identifier:
        print(identifier)












