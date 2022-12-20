import smtplib
import os

class MailTemplate():
    def __init__(self, to, subject, body):
        self.to = to
        self.subject = subject
        self.body = body
    
    def toString(self):
        #Example Template
#             message = """From: CVRP Test <lucho022001@hotmail.fr>
# To: To <corentinprp@gmail.com>
# Subject: SMTP e-mail test

# This is a test e-mail message.
# """
        return f"From: CVRP Test <{os.getenv('SENDER_EMAIL')}>\nTo: To <{self.to}>\nSubject: {self.subject}\n\n{self.body}"
    
    def sendMail(self):
        smtp = smtplib.SMTP(os.getenv('SMTP_EMAIL'), port=int(os.getenv('SMTP_PORT')))
        smtp.starttls()
        smtp.login(os.getenv('SENDER_EMAIL'), os.getenv('SENDER_PASSWORD'))
        print(self.toString())
        smtp.sendmail(os.getenv('SENDER_EMAIL'), self.to, self.toString())
        smtp.quit()