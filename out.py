import json
import threading
import urllib.request

TOKEN = "5937730297:AAE8CyW3ZZIGAH1ES8QraJt79GWRwORgijs"
# chat_id = "5294443565"
chat_id = "593289670"

import pyaudio
import numpy as np
frequency = 600
duration = 1000
p = pyaudio.PyAudio()

print("OutPut of the App:")


def callback(in_data, frame_count, time_info, status):
    t = np.linspace(0, duration/1000, int(duration*44100/1000), False)
    waveform = np.sin(2*np.pi*frequency*t)
    data = (waveform * 32767).astype(np.int16).tobytes()
    return (data, pyaudio.paContinue)

stream = p.open(format=pyaudio.paInt16,
                channels=1,
                rate=44100,
                output=True,
                stream_callback=callback)

def tele():
    while True:
        try:
            with open('static/data.json', 'r') as data:
                d = json.load(data)
                msg = d['msg']
                msg1 = msg[0]
                try:
                    msg2 = msg[22:]
                except: pass
                if (not msg1 == "N"):
                    print("Wild animal detected")
                    msg = f"Wild%20Animal%20Detected:%20{msg2}"
                    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id}&text={msg}"
                    try:
                        request_url = urllib.request.urlopen(url)
                    except:
                        print("No internet connection or bad input")
        except: pass

def sound():
    while True:
        try:
            with open('static/data.json', 'r') as data:
                d = json.load(data)
                msg = d['msg']
                msg1 = msg[0]
                if (not msg1 == "N"):
                    stream.start_stream()
                else:
                    stream.stop_stream()
        except: pass

t1 = threading.Thread(target=tele)
t2 = threading.Thread(target=sound)

t1.start()
t2.start()
