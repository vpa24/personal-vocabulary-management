from typing import Any
from django.core.management.base import BaseCommand
from manage_vocabulary.models import User
from datetime import timedelta, date

class Command(BaseCommand):
	def handle(self, *arg, **kwargs):
		today = date.today()
		users = User.objects.filter(is_active=False)
		for x in users:
			start_date = x.date_joined.date()
			end_date = start_date + timedelta(days=3)
			
			if end_date < today:
				User.objects.get(pk=x.id).delete()
				print(f'Just deleted {x.username}')