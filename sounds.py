import simpleaudio as sa

def make_sound(self):
    wave_obj = sa.WaveObject.from_wave_file('Cheering.wav')
    play_obj = wave_obj.play()
    play_obj.wait_done()

def move(self):
    wave_obj = sa.WaveObject.from_wave_file('Swoosh.wav')
    play_obj = wave_obj.play()
    play_obj.wait_done()

def start(self):
    wave_obj = sa.WaveObject.from_wave_file('start.wav')
    play_obj = wave_obj.play()
    play_obj.wait_done()
