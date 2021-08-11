#!/usr/bin/env python

import sys
from Connector import Connector
from Player import Player
import random
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *


c = Connector()
p = Player()

def randomize():
    if p.playing:
        p.stop()
    random_city = random.choice(c.cities_cache)
    stations = c.get_stations(random_city['city_id'])
    random_station = random.choice(stations)
    random_station_url = c.get_stream_url(random_station['station_id'])

    p.set_url(random_station_url)
    p.play()
    station_info = f"Now Playing:\n{random_station['station_name']}\n\n{random_city['city_name']}\n{random_city['country']}"
    info_lbl.setText(station_info)

def toggle_play():
    if p.playing:
        p.stop()
        play_btn.setText('Play')
    else:
        p.play()
        play_btn.setText('Stop')

def show_window():
    window.show()

app = QApplication(sys.argv)
app.setApplicationName('Radio Random')

window = QWidget()
window.setWindowTitle('Radio Random')
window.setFixedSize(400, 200)

play_btn = QPushButton('Stop')
play_btn.clicked.connect(toggle_play)

next_btn = QPushButton('Next Station')
next_btn.clicked.connect(randomize)

info_lbl = QLabel('')

layout = QGridLayout()
layout.addWidget(play_btn, 0, 0)
layout.addWidget(next_btn, 0, 1)
layout.addWidget(info_lbl, 1, 0, 1, 1)

window.setLayout(layout)
show_window()

app.setQuitOnLastWindowClosed(False)
icon = QIcon('icon.png')
tray = QSystemTrayIcon()
tray.setIcon(icon)
tray.setVisible(True)
menu = QMenu()
show_mnu = QAction('Show Window')
show_mnu.triggered.connect(show_window)
menu.addAction(show_mnu)
next_mnu = QAction('Next')
next_mnu.triggered.connect(randomize)
menu.addAction(next_mnu)
play_mnu = QAction('Play/Stop')
play_mnu.triggered.connect(toggle_play)
menu.addAction(play_mnu)
exit_mnu = QAction('Exit')
exit_mnu.triggered.connect(app.quit)
menu.addAction(exit_mnu)
tray.setContextMenu(menu)

sys.exit(app.exec_())
