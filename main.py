from PyQt5.QtWidgets import QApplication
from sys import argv
from helpers.config import get_db_path
from helpers.threading_functions import cntdown_timer
from resources.app import MainWindow
from db.db_daemon import db_weather_daemon, db_travel_daemon
from threading import Thread


if __name__ == '__main__':
    db_travel_watcher = Thread(target=db_travel_daemon, args=(get_db_path(),), daemon=True)
    db_travel_watcher.start()
    db_weather_watcher = Thread(target=db_weather_daemon, args=(get_db_path(),), daemon=True)
    db_weather_watcher.start()
    argv.append("--disable-web-security")
    app = QApplication(argv)
    window = MainWindow()
    window.show()
    timer = Thread(target=cntdown_timer, args=(window,), daemon=True)
    timer.start()
    app.exec_()
