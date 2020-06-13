import base64
import csv
import mimetypes
import requests

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.audio import MIMEAudio
from email.mime.application import MIMEApplication
from os import path
from string import Template


def replce(path, context):
    """
    Replaces the template variable in the text file with the context
    dict mapping

    Example:
    ```
    context = {'name': Bruce,'age':18}
    text = "Hello, my name is $name and I'm $age years old.

    returns "Hello, my name is bruce and I'm 18 years old."
    ```
    """
    with open(path, "r") as text:
        mailtext = text.read()

    s = Template(mailtext)
    return s.substitute(context)


def mapping_csv(path):
    """
    maps the fields in csv file to the rows.
    Returns a list of dict where each dict has fieldname as key
    and corresponding row as value
    """
    with open(path) as csvfile:
        reader = csv.DictReader(csvfile)
        return [{k.lower(): v.strip() if "@" not in v else "".join(v.split())
                for k, v in row.items()}
                for row in reader]


def create_message(addr_send, addr_recv,
                   body_message, subject="", attachment=None):
    """
    Creates a message to be sent by email

    Args:

      `addr_send : str` the address of the sender. From:

      `addr_recv : str` the mail address of the receiver. To:

      `body_message : str` The text in the body of an email.

      `subject : str` The subject of the email. Default to empty string

      `attachment : str` Path of the files to be attached to an email, must be
      space separated.  example : `attachment= path/to/file1 path/to/file2`

    Returns:

      An object containing a base64url encoded email object.
    """
    msg = MIMEMultipart()
    msg['From'] = addr_send
    msg['To'] = addr_recv
    msg['Subject'] = subject
    msg.attach(MIMEText(body_message.replace('\n', '<br>'), 'html'))
    if attachment is not None:
        for file in attachment.split():
            content_type, encoding = mimetypes.guess_type(file)

            if content_type is None or encoding is not None:
                content_type = 'application/octet-stream'
            main_type, sub_type = content_type.split('/', 1)
            with open(file, 'rb') as fp:
                if main_type == 'text':
                    message_file = MIMEText(fp.read().decode(),
                                            _subtype=sub_type,)

                elif main_type == 'image':
                    message_file = MIMEImage(fp.read(),
                                             _subtype=sub_type)

                elif main_type == 'audio':
                    message_file = MIMEAudio(fp.read(),
                                             _subtype=sub_type)

                else:
                    message_file = MIMEApplication(fp.read(),
                                                   _subtype=sub_type,)

            filename = path.basename(file)
            message_file.add_header('Content-Disposition',
                                    'attachment', filename=filename)
            msg.attach(message_file)
    return msg


def create_message_gmail(message):
    """
    Creates a message for Gmail API
    args:

    An object containing a base64url encoded email object.
    """
    return {'raw': base64.urlsafe_b64encode(message.as_bytes()).decode()}


def select_smtp_provider(mail):
    """"
    select the SMTP domain and port base on usernam with API
    of https://emailsettings.firetrust.com/

    returns tuple (domain, port)
    """
    url = "https://emailsettings.firetrust.com/settings?q="

    r = requests.get(f"{url}{mail}")
    if r.status_code == 200:
        res = r.json()
        smtp_domain = res['settings'][2]['address']
        port = res['settings'][2]['port']

        return (smtp_domain, port)
    else:
        return None, None
