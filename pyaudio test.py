import pyaudio
import wave
import sys
import time
import array
import struct
# import numpy
import random
import math

chunk = 1024

pianofile = "pianoc.wav"

p = pyaudio.PyAudio()


from wavio import read

print(read(pianofile).data)

thepianoarray = (read(pianofile).data).tolist()




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

def filetoarray(filename):
    wf = wave.open(filename, 'rb')
    thearray = []
    data = wf.readframes(chunk)
    while data != '' and len(data) > 0:
        pcm_samples = array.array("h", wf.readframes(chunk))
        #print(max(pcm_samples))
        thearray += [item/65536 for item in pcm_samples]
        data = wf.readframes(chunk)
    return thearray


def playsine(f=440.0, dur=5, v=0.125):
    sr = 44000
    frames = int(sr * dur)
    sinesamples = [((v * (1 - (i / frames))) * math.sin(2 * math.pi * i * f / sr) + (v * (1 - (i / frames))) * math.sin(
        2 * math.pi * i * 1.498307077 * f / sr)) for i in range(frames)]
    output_bytes = array.array('f', sinesamples).tobytes()
    stream = p.open(format=pyaudio.paFloat32,
                    channels=1,
                    rate=sr,
                    output=True)
    start_time = time.time()
    stream.write(output_bytes)
    print("Played sound for {:.2f} seconds".format(time.time() - start_time))

    stream.stop_stream()
    stream.close()

    p.terminate()


def playarray(thearray, samplerate=44000):
    output_bytes = array.array('f', thearray).tobytes()
    stream = p.open(format=pyaudio.paFloat32,
                    channels=1,
                    rate=samplerate,
                    output=True)
    stream.write(output_bytes)


def generatetone(f=440.0, dur=2, v=0.125):
    sr = 44000
    frames = int(sr * dur)
    sinesamples = [(v * math.sin(2 * math.pi * i * f / sr)*abs(math.sin(i/64))) for i in range(frames)]
    return sinesamples

def generatewhitenoise(dur=2, v=0.125):
    sr = 44000
    res = 1000
    frames = int(sr * dur)
    samples = []
    for i in range(frames):
        samples.append(random.randint(int(-v*res), int(v*res))/res)
    return samples

def addsamples(a1, a2):
    minlength = min([len(a1), len(a2)])
    maxlength = max([len(a1), len(a2)])

    if len(a1) > len(a2):
        greater = a1
    else:
        greater = a2

    newarray = []
    i = 0
    while i < minlength:
        newarray.append(a1[i] + a2[i])
        i += 1
    while i < maxlength:
        newarray.append(greater[i])
        i += 1
    return newarray


'''a = generatetone(220)
csharp = generatetone(554.365262)
e = generatetone(659.2551138)

chord = addsamples(addsamples(a, e), csharp)

print(chord)

playarray(chord)'''

'''static = generatewhitenoise(0.1,0.03125)

for i in range(64):
    playarray(static)'''

# playsine()


'''pianoarray = filetoarray(pianofile)

playarray(pianoarray)
print(time.time())

play(pianofile)'''

playarray(thepianoarray)

p.terminate()




