from smtplib import *

gmail_user = 'dylankoger10015@gmail.com'
passw = 'lunch10015'

def touchBase(message):
    try:
        smtp_server = SMTP_SSL('smtp.gmail.com', 465)
        print('0')
        smtp_server.ehlo()
        print('1')
        smtp_server.login(gmail_user, passw)
        print('2')
        smtp_server.sendmail(gmail_user, gmail_user, message)
        print('3')
        smtp_server.close()
        print('4')
    except:
        print('damn')
