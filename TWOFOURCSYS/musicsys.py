from pygame import mixer

mixer.init(44100, -16, 2)
mixer.init()

defaultCh = mixer.Channel(0)
musicCh = mixer.Channel(1)
sfxCh = [mixer.Channel(2), mixer.Channel(3), mixer.Channel(4), mixer.Channel(5), mixer.Channel(6), mixer.Channel(7)]

def play(filename, channel=defaultCh):
    if channel == sfxCh:
        for ch in channel:
            if not ch.get_busy():
                ch.play(mixer.Sound(filename))
                break
        if channel.index(ch) == len(channel):
            print("MusicSys | Failed to play so:und")
    else:
        channel.play(mixer.Sound(filename))
    
def setVol(vol=0.5,channel=defaultCh):
    channel.set_volume(vol)