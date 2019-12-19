from time import sleep, time


def cntdown_timer(window):
    while True:
        if int(time()) >= window.time_to_move:
            window.move_right.emit()
        sleep(1)