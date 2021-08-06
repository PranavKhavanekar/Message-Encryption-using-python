import pandas as pd
from smtplib import SMTP
from  email.message import EmailMessage
import json
from middleware import crypto

class Sender:
    def __init__(self, config, mails) -> None:
        self.config = json.load(config)
        self.mails: pd.DataFrame = pd.read_csv(mails)
        self.Key = crypto(self.config['key'])
    

    def _send(self, To, Sub, Message, sender=None):
        message = EmailMessage()
        message.set_content(Message)
        message['Subject'] = Sub
        message['From'] = self.config['From'] if sender is None else sender
        message['To'] = To
        try:
            with SMTP('smtp.gmail.com', 587) as session:
                session.starttls()
                session.login(*self.config['creds'])
                session.send_message(message)
                print('Sent')
                return True
        except Exception as e:
            print('Message Failed')
            return e


    def init(self, To):
        self.config['init'] = ['Public Key', f'My Public Key{self.Key.public}']
        self._send(To, *self.config['init'])


    def send(self):
        for i, mail in self.mails.iterrows():
            mail['Mail'] = crypto.encrypt(mail['key', mail['Mail']])
            self._send(*mail.values())