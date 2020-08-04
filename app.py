import praw
import smtplib
import schedule
import time
import os
from os import environ

reddit = praw.Reddit(client_id=environ['ID'],
                     client_secret=environ['SECRET'],
                     user_agent=environ['AGENT'])

lista = ["nottheonion", "technews", "hacking", "MachineLearning", "ProgrammerHumor", "cellbits", "MySummerCar",
         "pescocofino", "Outdoors"]

email_from = environ['FROM']
key_from = environ['FROM_KEY']
email_to = environ['TO']


def hots():
    msg = ""
    for i, communitie in enumerate(lista):
        subreddit = reddit.subreddit(communitie)
        msg += "=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~\n"
        msg += subreddit.display_name + "\n\n"
        for submission in subreddit.hot(limit=7):
            msg += submission.title + "\n"
            msg += submission.url + "\n\n"
    return msg


def send_email():
    msg = hots()
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(email_from, key_from)
    server.sendmail(email_from, email_to, msg.encode("utf-8"))
    server.quit()
    print("Email enviado")


schedule.every().day.at("10:00").do(send_email)

while True:
    schedule.run_pending()
    time.sleep(3)
