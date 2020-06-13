import smtplib
import pickle
import os.path

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

from src.utils import create_message_gmail
from secret import user_mail, password


def send_mail(message, mailto, smtp_server, port):
    """
    Send an email through SMTP.

    Arg:
        message : a message object containing a base64url encoded email object.
    """

    with smtplib.SMTP_SSL(smtp_server, port) as server:
        server.login(user=user_mail,
                     password=password)
        try:
            server.send_message(message, user_mail, mailto)
            print(f"[*] Email sent from{user_mail} to {mailto}")
        except Exception as e:
            print(f"Something went wrong while sending the mail\n{e}")


def send_gmail(msg):
    """
    Send an email through Gmail API.

    Arg:
        message : a message object containing a base64url encoded email object.
    """
    # If modifying these scopes, delete the file token.pickle.
    SCOPES = ['https://www.googleapis.com/auth/gmail.send',
              'https://www.googleapis.com/auth/gmail.readonly']
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.

    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)

        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('gmail', 'v1', credentials=creds)

    # Call the Gmail API
    try:
        name = service.users().settings().sendAs().list(userId='me').execute()

        # Add display name if it exists
        display_name = name['sendAs'][0]['displayName']
        msg.replace_header('From',
                           f"Mohammed Nabil <{user_mail}>" if display_name
                           else user_mail)

        msg = create_message_gmail(msg)

        message = service.users().messages().send(userId="me",
                                                  body=msg).execute()
        print(f"[*] message sent | ID:{message['id']}\n")
    except Exception as e:
        print(f"Something went wrong ! \n{e}")
