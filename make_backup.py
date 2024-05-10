import datetime
import subprocess

today = datetime.date.today()

command = f"cd /home/MatthewWong/backups; mysqldump -u MatthewWong -h MatthewWong.mysql.pythonanywhere-services.com --set-gtid-purged=OFF --no-tablespaces 'MatthewWong$default'  > /home/MatthewWong/backups/{today}.sql"

subprocess.run(command, shell=True)