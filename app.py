import praw
import smtplib
import schedule
import time
from os import environ

reddit = praw.Reddit(client_id=environ['ID'],
                     client_secret=environ['SECRET'],
                     user_agent=environ['AGENT'])

lista = ["nottheonion", "technews", "hacking", "MachineLearning", "ProgrammerHumor", "cellbits", "MySummerCar",
         "pescocofino", "Outdoors"]

email_from = environ['FROM']
email_to = "msubetir@gmail.com"


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
    server.login(email_from, environ['FROM_KEY'])
    server.sendmail(email_from, email_to, msg.encode("utf-8"))
    server.quit()


schedule.every().day.at("13:40").do(send_email)

while True:
    schedule.run_pending()
    time.sleep(1)
