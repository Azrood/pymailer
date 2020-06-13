import time
import re
import random

from src.mailer import send_gmail, send_mail
from src.utils import (mapping_csv, create_message,
                       replce, select_smtp_provider)
from secret import port, smtp, user_mail


def main():
    context = mapping_csv("database.csv")
    for row in context:
        bodytext = replce("./mailtext.txt", context)
        print(f"[*] Sending email to {row['email']}")

        msg = create_message(user_mail,
                             row['email'],
                             bodytext,
                             subject="Internship")

        if re.match(r"^([a-zA-Z0-9_\-\.]+)@gmail\.([a-zA-Z]{2,5})$",
                    user_mail,
                    re.I):
            time.sleep(random.random())
            send_gmail(msg)
        else:
            if not all((smtp, port)):  # noqa

                smtp_server, port = select_smtp_provider(user_mail)
                send_mail(msg, row['email'], smtp_server, port)
            else:
                print("[!] No SMTP address found, you can't send "
                      "an email with this provider !")
                print("[!] If you know the SMTP address and port of your "
                      "provider,you can add them in the file secret.py")


if __name__ == "__main__":
    main()
