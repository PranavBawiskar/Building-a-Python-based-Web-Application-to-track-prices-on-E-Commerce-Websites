import requests
from bs4 import BeautifulSoup
import smtplib
import time

#URL of the product page that you might want to track
URL = ''
#to get your user agent go to google and type 'my user agent' and copy the agent and paste between the single quotes
headers = {"User-Agent" : ''}

def check_price():
    page = requests.get(URL, headers=headers)
    soup = BeautifulSoup(page.content, 'html.parser')
    title = soup.find(id="productTitle").get_text()
    price = soup.find(id="priceblock_dealprice").get_text()
    # THE CONVERTED PRICE IS TYPE CASTED BECAUSE - WE WANT TO COMPARE THAT VALUE AS FLOAT
    converted_price = float(price[1:4] + price[5:9])
    print('The Price is: ',converted_price)
    print('Product name: ',title.strip())
    if(converted_price < 12000.0):
        send_mail()
    else:
        print("Sorry! The price hasn't reduced yet! ")

def send_mail():
    #port number 587 intended for email client to email server communication -
    #ie sending out meail (Almost like a standard SMTP port as it starts SSL
    #encryption automatically)
    server = smtplib.SMTP('smtp.gmail.com',587)
    # ehlo is an extended SMTP command sent by an email server ti identify itself
    #when connecting to another email server to start hr process of sending email
    server.ehlo()
    server.starttls()
    server.ehlo()
    #Login to your email sending account
    #Before you enter your credentials, enable less secure apps
    server.login('youremail','yourpassword')
    subject="Hey! the shortlisted product's Price fell down"
    #The body of the email to be sent
    body='Click on this link below to access the deal! \n\n #mention your URL here'
    #The formating is the only proper way to attach subject and body
    msg = "Subject: {}\n\n{}".format(subject,body)
    #Send that mail from senders email to receivers email with the message
    server.sendmail('youremail','receiversemail',msg)
    #confirmation on terminal
    print('Hey the Email has been sent')
    #close the server
    server.quit()

while(True):
    #invoke the function
    check_price()
    #for every 2 seconds there will be a call to the function, check_price.
    time.sleep(2)
