import praw
import smtplib
import schedule
import time
import os
from os import environ

reddit = praw.Reddit(client_id=environ['ID'],
                     client_secret=environ['SECRET'],
                     user_agent=environ['AGENT'])

# Comunidades a gosto :)
lista = environ['COMUN'].split(',')
print(lista)
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

# +3 horas para compensar o fuso do local que está hospedado
schedule.every().day.at("09:30").do(send_email)
schedule.every().day.at("21:30").do(send_email)
#schedule.every(2).minutes.do(send_email)

while True:
    schedule.run_pending()
    time.sleep(3)
