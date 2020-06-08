

from mailer import create_message, send_gmail
from utils import replce, mapping_csv

from example.secret_sample import user_mail

context = mapping_csv("./example/database_example.csv")
for row in context:
    bodytext = replce("./example/mailtext.sample.txt", row)

msg = create_message(user_mail,
                     bodytext,
                     "sujet",
                     "./example/mailtext.sample.txt")
print("*"*50)
print(msg)

# send_gmail(msg)
