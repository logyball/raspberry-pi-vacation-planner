from db.db_logic import TravelDbBackgroundProcess
from time import sleep


def db_daemon(db_path):
    print('starting db daemon')
    database = TravelDbBackgroundProcess(db_path)
    while True:
        database.update_resorts_check()
        print('resorts updated, going to sleep')
        sleep(5)
