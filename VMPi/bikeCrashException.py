from sense_hat import SenseHat

import datetime
import requests
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Send an email with an attachment using SMTP
def send_mail(eFrom, to, subject, text):
    
    # SMTP Server details: update to your credentials or use class server
    smtpServer='smtp.mailgun.org'
    smtpUser='postmaster@sandboxYOURAUTHHERE.mailgun.org'
    smtpPassword='YOURPASSHERE'
    port=587

#     # open attachment and read in as MIME image
#     fp = open(attachment, 'rb')
#     msgImage = MIMEImage(fp.read())
#     fp.close()

    #construct MIME Multipart email message
    msg = MIMEMultipart()
    msg.attach(MIMEText(text))
    #msgImage['Content-Disposition'] = 'attachment; filename="image.jpg"'
    #msg.attach(msgImage)
    msg['Subject'] = subject
    print("sent")
    # Authenticate with SMTP server and send
    s = smtplib.SMTP(smtpServer, port)
    print("sent1")
    s.login(smtpUser, smtpPassword)
    print("sent2")
    s.sendmail(eFrom, to, msg.as_string())
    print("sent3")
    s.quit()
    print("sent4")
    




f = open("./exceptions/"+datetime.datetime.utcnow().strftime("%Y%m%d %H%M%S%f")+".log", "x")
#print("arguments")
#getopt.getopt(args)
#import datetime

sense = SenseHat()
sense.clear()

orientation = sense.get_orientation_radians()
pi = round(orientation['pitch'],1)
ro = round(orientation['roll'],1)
#ya = round(orientation['yaw'],1)
  
acceleration = sense.get_accelerometer_raw()
x = round(acceleration['x'],2)
y = round(acceleration['y'],2)
z = round(acceleration['z'],2)
  
if ro > 0.8 or ro < -0.8 or pi > 0.8 or pi < -0.8:

  print("argument", str(datetime.datetime.utcnow().strftime('%y%m%d %H%M%S.%f')), x, y, z, pi, ro)
  currentTime = datetime.datetime.now().strftime("%H:%M:%S")
  text= f'Exception event occured from VMPi at {currentTime}'
  send_mail('thomas@vm.pi', 'YOUREMAILHERE@gmail.com', 'VMPi Event', text)
#while True:
#  print("some")
