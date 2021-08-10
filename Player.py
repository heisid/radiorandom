import gi
gi.require_version('Gst', '1.0')
from gi.repository import Gst


class Player:
    def __init__(self):
        Gst.init(None)
        self.streamer = Gst.ElementFactory.make('playbin', None)
        self.playing = False
        self.play_url = ''

    def set_url(self, url: str) -> None:
        self.play_url = url
            
    def play(self) -> str:
        if self.play_url:
            self.streamer.set_property('uri', self.play_url)
            self.streamer.set_state(Gst.State.PLAYING)
            self.playing = True
            return 'playing'
        else:
            return 'uri not set'
    
    def stop(self) -> str:
        self.streamer.set_state(Gst.State.NULL)
        self.playing = False
        return 'stopped'
