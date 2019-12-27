from PyQt5.QtWidgets import QApplication
from sys import argv
from src.backend.config import get_db_path
from src.backend.threading_functions import cntdown_timer
from src.resources.MainApp import MainWindow
from src.db.db_daemon import db_weather_daemon, db_travel_daemon
from threading import Thread


if __name__ == '__main__':
    db_travel_watcher = Thread(target=db_travel_daemon, args=(get_db_path(),), daemon=True)
    db_travel_watcher.start()
    db_weather_watcher = Thread(target=db_weather_daemon, args=(get_db_path(),), daemon=True)
    db_weather_watcher.start()
    argv.append("--disable-web-security")
    app = QApplication(argv)
    window = MainWindow()
    window.setWindowTitle('Vacation Planning Assistant')
    window.show()
    timer = Thread(target=cntdown_timer, args=(window,), daemon=True)
    timer.start()
    app.exec_()
