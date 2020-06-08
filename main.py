import time
import re

from mailer import send_gmail, send_mail
from utils import (mapping_csv, create_message, create_message_gmail,
                   replce, select_smtp_provider)
from secret import port, smtp, user_mail


def main():
    context = mapping_csv("./database.csv")

    for row in context:
        bodytext = replce("./mailtext.txt", row)
        print(f"[*] Sending email to {*row.values(),}")
        msg = create_message(row['email'],
                             bodytext,
                             subject="Internship")
        if re.match(r"\w+@gmail.\w+", user_mail, re.I):
            msg = create_message_gmail(msg)
            time.sleep(0.1)
            send_gmail(msg)
        else:
            if not all((smtp, port)):

                smtp_server, port = select_smtp_provider(user_mail)
                send_mail(msg, row['email'], smtp_server, port)
            else:
                print("[!] No SMTP address found, you can't send an email with this provider !")
                print("[!] If you know the SMTP address and port of your provider, you can add them in the file secret.py")


if __name__ == "__main__":
    main()
