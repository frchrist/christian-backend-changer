
from .models import ClientLoginCode as Clc , ClientVerificationCode as Cvc, Client


class Utils:
	@staticmethod
	def create_login_code(client):
		Clc.objects.filter(client=client).delete()
		return Clc.objects.create(client=client)

	@staticmethod
	def create_email_verification_code(client):
		Cvc.objects.filter(client=client).delete()
		if not client.email_is_valid:
			print("not")
			return Cvc.objects.create(client=client)
		print("verify")

	@staticmethod
	def email_vefication_code_instance(code):
		return Cvc.objects.get(code=code)

	@staticmethod
	def client_from_mail(email):
		try:
			return Client.objects.get(email=email)
		except:
			return None


	@staticmethod
	def authenticate_with_vf_code(**kwrags):
		client = Utils.client_from_mail(kwrags["email"])
		print(client)
		return Cvc.objects.get(code=kwrags["code"], client=client)

	

