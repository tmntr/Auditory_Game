import pyaudio
import wave
import sys
import time


chunk = 1024

pianofile = "pianoc.wav"



p = pyaudio.PyAudio()




def play(filename):
    wf = wave.open(pianofile, 'rb')
    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True)
    stream.write(wf.readframes(chunk))
    data = wf.readframes(chunk)
    while data != '' and len(data) > 0:
        stream.write(data)
        data = wf.readframes(chunk)

    stream.stop_stream()
    stream.close()




for i in range(3):
    print(time.time())
    play(pianofile)
    print(time.time())



p.terminate()



