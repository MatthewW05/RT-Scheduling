import datetime
from django.core.management import call_command
import os

today = datetime.date.today()

backup_dir = r"/home/MatthewWong/backups"
backup_file = os.path.join(backup_dir, f'{today}.json')

with open(backup_file, 'w') as f:
    call_command('dumpdata', stdout=f)