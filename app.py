import praw
import smtplib
import schedule
import time

reddit = praw.Reddit(client_id="LnVIf5fqLEvPVA",
                     client_secret="6eaWqJBLa-2-_okn1plM0p8hbXk",
                     user_agent="my user agent")

lista = ["nottheonion", "technews", "hacking", "MachineLearning", "ProgrammerHumor", "cellbits", "MySummerCar", "pescocofino", "Outdoors"]
email_from = "galinharadical@gmail.com"
email_to = "msubetir@gmail.com"

def hots():
    msg = ""
    for i, communitie in enumerate(lista):
        subreddit = reddit.subreddit(communitie)
        msg += "=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~\n"
        msg += subreddit.display_name+"\n\n"
        for submission in subreddit.hot(limit=5):
            msg += submission.title+"\n"
            msg += submission.url+"\n\n"
    return msg

def send_email():
    msg = hots()
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(email_from, "deagle272")
    server.sendmail(email_from, email_to, msg.encode("utf-8"))
    server.quit()
    print("Email enviado")

schedule.every().day.at("20:25").do(send_email)

while True:
    schedule.run_pending()
    time.sleep(1)
