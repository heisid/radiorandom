#!/usr/bin/env python

from sys import exit, argv
from os import remove
from os.path import exists
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from Connector import Connector
from Player import Player
from random import choice
from typing import Callable


__version__ = '0.1'
__author__ = 'Sid'


class RadioRandomWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Radio Random')
        self.setFixedSize(400, 150)
        self.layout = QGridLayout()
        central_widget = QWidget(self) # I don't understand this
        self.setCentralWidget(central_widget) # I don't understand this
        central_widget.setLayout(self.layout) # I don't understand this
        self.create_widget()
        self.create_tray()

    def create_widget(self) -> None:
        self.play_btn = QPushButton('Stop')
        self.next_btn = QPushButton('Next')
        self.info_lbl = QLabel('')
        self.layout.addWidget(self.play_btn, 0, 0)
        self.layout.addWidget(self.next_btn, 0, 1)
        self.layout.addWidget(self.info_lbl, 1, 0, 1, 1)

    def assign_play_btn(self, action: Callable) -> None:
        self.play_btn.clicked.connect(action)
    
    def assign_next_btn(self, action: Callable) -> None:
        self.next_btn.clicked.connect(action)

    def set_play_state(self, is_playing: bool) -> None:
        if is_playing:
            self.play_btn.setText('Stop')
        else:
            self.play_btn.setText('Play')
    
    def set_info_text(self, info: str) -> None:
        self.info_lbl.setText(info)

    def create_tray(self) -> None:
        icon = QIcon('icon.png')
        self.tray = QSystemTrayIcon()
        self.tray.setIcon(icon)
        self.tray.setVisible(True)
        self.tray_mnu = QMenu()
        self.show_tray_mnu = QAction('Show Window')
        self.tray_mnu.addAction(self.show_tray_mnu)
        self.play_tray_mnu = QAction('Play/Stop')
        self.tray_mnu.addAction(self.play_tray_mnu)
        self.next_tray_mnu = QAction('Next')
        self.tray_mnu.addAction(self.next_tray_mnu)
        self.exit_tray_mnu = QAction('Exit')
        self.tray_mnu.addAction(self.exit_tray_mnu)
        self.tray.setContextMenu(self.tray_mnu)

    def assign_play_tray(self, action: Callable) -> None:
        self.play_tray_mnu.triggered.connect(action)

    def assign_next_tray(self, action: Callable) -> None:
        self.next_tray_mnu.triggered.connect(action)

    def assign_show_tray(self, action: Callable) -> None:
        self.show_tray_mnu.triggered.connect(action)
    
    def assign_exit_tray(self, action: Callable) -> None:
        self.exit_tray_mnu.triggered.connect(action)

    def set_tray_tooltip(self, text: str) -> None:
        self.tray.setToolTip(text)

    # Override
    def closeEvent(self, event) -> None:
        event.ignore()
        self.hide()

class Controller():
    def __init__(self, window, connector, player):
        self.window = window
        self.connector = connector
        self.player = player
        self.widget_assign()
        self.tray_assign()
        self.run()

    def widget_assign(self) -> None:
        self.window.assign_next_btn(self.randomize)
        self.window.assign_play_btn(self.toggle_play)

    def tray_assign(self) -> None:
        self.window.assign_play_tray(self.randomize)
        self.window.assign_next_tray(self.toggle_play)
        self.window.assign_show_tray(self.window.show)
        self.window.assign_exit_tray(qApp.quit)

    def randomize(self) -> None:
        if self.player.playing:
            self.player.stop()
        
        random_city = choice(connector.cities_cache)
        stations = connector.get_stations(random_city['city_id'])
        random_station = choice(stations)
        random_station_url = connector.get_stream_url(
                random_station['station_id'])
        self.player.set_url(random_station_url)
        self.player.play()
        station_info = f"Now Playing:\n{random_station['station_name']}\n\n{random_city['city_name']}\n{random_city['country']}"
                
        self.window.set_info_text(station_info)
        self.window.set_tray_tooltip(station_info)

    def toggle_play(self) -> None:
        if self.player.playing:
            self.player.stop()
            self.window.set_play_state(True)
        else:
            self.player.play()
            self.window.set_play_state(False)

    def run(self) -> None:
        self.window.show()
        self.randomize()


def check_lock():
    if exists('radiorandom.lock'):
        warning_dlg = QMessageBox()
        warning_dlg.setText(
                'Radio Random is still running.\nIf it is not, delete radiorandom.lock')
        exit(warning_dlg.exec_())
    open('radiorandom.lock', 'w').close()

def lock_clean():
    remove('radiorandom.lock')


if __name__ == '__main__':
    app = QApplication(argv)
    app.setApplicationName('Radio Random')

    check_lock()

    connector = Connector()
    player = Player()
    window = RadioRandomWindow()
    controller = Controller(window, connector, player)
    controller.run()

    app.aboutToQuit.connect(lock_clean)
    exit(app.exec_())
