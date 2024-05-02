import shutil
import datetime

today = datetime.date.today()

source = r"/home/MatthewWong/RT-Scheduling/mysite/db.sqlite3"

destination = r"/home/MatthewWong/backups/{date}.sqlite3".format(date = today)

shutil.copyfile(source, destination)