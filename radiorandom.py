#!/usr/bin/env python

from Connector import Connector
from Player import Player
import random
import tkinter as tk

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
    station_info = f"{random_station['station_name']} in {random_city['city_name']}, {random_city['country']}"
    station_lbl.config(text=station_info)

def toggle_play():
    if p.playing:
        p.stop()
        play_btn.config(text='Play')
    else:
        p.play()
        play_btn.config(text='Stop')

window = tk.Tk()
window.title('Radio Random')
window.minsize(300, 150)

play_frm = tk.Frame(master=window, relief=tk.RIDGE, borderwidth=2)
play_frm.pack(fill=tk.BOTH, expand=True)
info_frm = tk.Frame(master=window, relief=tk.RIDGE, borderwidth=2)
info_frm.pack(fill=tk.BOTH, expand=True)

next_btn = tk.Button(master=play_frm, text='Next Station', command=randomize)
next_btn.pack(side=tk.LEFT)
play_btn = tk.Button(master=play_frm, text='Stop', command=toggle_play)
play_btn.pack(side=tk.LEFT)
station_lbl = tk.Label(master=info_frm, text='')
station_lbl.pack()

randomize()
window.mainloop()


