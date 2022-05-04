from __future__ import print_function

import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from email.mime.text import MIMEText
import base64
import html

def initservice():
    creds = ""
    if os.path.exists('./gmailapi/token.json'):
        SCOPES = ['https://www.googleapis.com/auth/gmail.readonly', 'https://www.googleapis.com/auth/gmail.send', 'https://www.googleapis.com/auth/gmail.compose', 'https://mail.google.com/']
        creds = Credentials.from_authorized_user_file('./gmailapi/token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
    service = build('gmail', 'v1', credentials=creds)
    return(service)

def create_message(sender, to, subject, message_text):
  message = MIMEText(message_text)
  message['to'] = to
  message['from'] = sender
  message['subject'] = subject
  return {'raw': base64.urlsafe_b64encode(message.as_string().encode()).decode()}

def create_message_with_attachment(sender, to, subject, message_text, file):
  message = MIMEMultipart()
  message['to'] = to
  message['from'] = sender
  message['subject'] = subject

  msg = MIMEText(message_text)
  message.attach(msg)

  content_type, encoding = mimetypes.guess_type(file)

  if content_type is None or encoding is not None:
    content_type = 'application/octet-stream'
  main_type, sub_type = content_type.split('/', 1)
  if main_type == 'text':
    fp = open(file, 'rb')
    msg = MIMEText(fp.read(), _subtype=sub_type)
    fp.close()
  elif main_type == 'image':
    fp = open(file, 'rb')
    msg = MIMEImage(fp.read(), _subtype=sub_type)
    fp.close()
  elif main_type == 'audio':
    fp = open(file, 'rb')
    msg = MIMEAudio(fp.read(), _subtype=sub_type)
    fp.close()
  else:
    fp = open(file, 'rb')
    msg = MIMEBase(main_type, sub_type)
    msg.set_payload(fp.read())
    fp.close()
  filename = os.path.basename(file)
  msg.add_header('Content-Disposition', 'attachment', filename=filename)
  message.attach(msg)
  return {'raw': base64.urlsafe_b64encode(message.as_string())}

def send_message(service, user_id, message):
    try:
        message = (service.users().messages().send(userId=user_id, body=message).execute())
        print('Message Id: %s' % message['id'])
    #return(message)
    except Exception as e:
        print(e)

def fetch_messages(service, userid):
    results = service.users().messages().list(userId=userid,labelIds = ['INBOX', 'UNREAD']).execute()
    messages = results.get('messages', [])
    messagelist = []
    for message in messages:
        msg = service.users().messages().get(userId=userid, id=message['id']).execute()
        time = msg['payload']['headers'][1]['value']
        whena = time.find(";")+1
        when = time[whena:len(time)]
        x = 0
        while(when[x] == ' '):
            when = when[1:len(when)]
        contents = msg['snippet']
        contents= html.unescape(contents)
        messagelist.append([when,msg['payload']['headers'][19]['value'], contents])
        service.users().messages().modify(userId=userid, id=message['id'], body={'removeLabelIds': ['UNREAD']}).execute()
    #print(messagelist)
    return(messagelist)
def readMail(mail_address):
    return(fetch_messages(initservice(), mail_address))
def sendText(message,destination,mail_address):
    return(send_message(initservice(), mail_address, create_message(mail_address, destination, " ",  message)))
