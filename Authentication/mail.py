
from threading import Thread
from django.core.mail import EmailMessage
from django.conf import settings
class AsynEmailMessage(Thread):
    #For email processing
    def __init__(self,data):
        super().__init__()
        self.data = data
        #data must be an object dict
        assert isinstance(self.data,dict), "data must be an dict objects"
        self.email = EmailMessage(subject=data["email_subject"], body=data["email_body"], from_email=settings.EMAIL_HOST,to=data["email_to"])
    def run(self):
        self.email.send()
