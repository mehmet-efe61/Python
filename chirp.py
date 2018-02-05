#!/usr/bin/env python
"""
Chirp.io Encoder/Decoder
"""
import sys
import time
import uuid
import string
import pyaudio
import requests
import argparse
import threading
import webbrowser
import numpy as np

MIN_AMPLITUDE = 100
SAMPLE_RATE = 44100.0  # Hz
CHAR_DURATION = 0.0872  # secs


class Audio():
    """ Audio Processing """
    CHANNELS = 1
    HUMAN_RANGE = 20000
    FORMAT = pyaudio.paInt16
    RATE = int(SAMPLE_RATE)
    CHUNK = int(SAMPLE_RATE * CHAR_DURATION)

    def __init__(self, callback):
        self.audio = pyaudio.PyAudio()
        self.callback = callback

    def __del__(self):
        try:
            self.audio.terminate()
        except:
            pass

    def record(self):
        self.stream = self.audio.open(
            format=self.FORMAT,
            channels=self.CHANNELS,
            rate=self.RATE,
            input=True,
            frames_per_buffer=self.CHUNK,
            stream_callback=self.callback
        )

    def play(self, frames):
        """ Write data to system audio buffer"""
        stream = self.audio.open(format=pyaudio.paInt16,
                                 channels=1,
                                 rate=self.RATE,
                                 output=True)
        stream.write(frames, len(frames))
        stream.stop_stream()
        stream.close()


class Signal():
    """ Digital Signal Processing """

    def __init__(self, fs):
        self.fs = float(fs)  # sampling frequency

    def fft(self, y):
        """ Perform FFT on y with sampling rate"""
        n = len(y)  # length of the signal
        k = np.arange(n)
        T = n / self.fs
        freq = k / T  # two sides frequency range
        freq = freq[range(int(n / 2))]  # one side frequency range

        Y = np.fft.fft(y) / n  # fft computing and normalisation
        Y = Y[range(int(n / 2))]

        return (freq, abs(Y))

    def max_freq(self, data):
        """ Perform FFT on data and return maximum frequency """
        x, y = self.fft(data)
        index = y.argmax()
        return x[index]

    def sine_wave(self, freq, duration):
        """ Generate a sine wave array at given frequency for duration in seconds """
        return np.sin(2 * np.pi * np.arange(self.fs * duration) * freq / self.fs)


class Chirp():
    """ Chirp Encoding/Decoding
        chirp.io/technology """
    RATE = SAMPLE_RATE
    CHAR_LENGTH = CHAR_DURATION  # duration of one chirp character - 87.2ms
    CHAR_SAMPLES = CHAR_LENGTH * RATE  # number of samples in one chirp character
    CHIRP_SAMPLES = CHAR_SAMPLES * 20  # number of samples in an entire chirp
    CHIRP_VOLUME = 2 ** 16 / 48  # quarter of max amplitude
    BASE_URL = 'https://api.chirp.io/v1'

    def __init__(self):
        self.chirp = ''
        self.amplitude = MIN_AMPLITUDE
        self.map = self.get_map()
        self.device = str(uuid.uuid1())
        self.chars = sorted(self.map.keys())
        self.dsp = Signal(self.RATE)
        self.token = self.authenticate()
        self.headers = {'X-Auth-Token': self.token}

    def get_map(self):
        """ Construct map of chirp characters to frequencies
            0 = 1760Hz 1 = 1864Hz v = 10.5kHz """
        a6 = 1760
        a = 2 ** (1 / 12.0)
        # characters range from 0-9 and a-v
        chars = string.digits + string.ascii_letters[0:22]
        d = {}

        for n in range(0, 32):
            d[chars[n]] = a6 * (a ** n)

        return d

    def get_code(self, url):
        """ Request a long code from chirp API """
        try:
            payload = {
                'public': True,
                'data': {'url': url}
            }
            r = requests.post(
                self.BASE_URL + '/chirps',
                headers = self.headers,
                json=payload
            )
            if r.status_code == 201:
                rsp = r.json()
                if 'longcode' in rsp:
                    return 'hj' + rsp['longcode']
                elif 'error' in rsp:
                    print(rsp['description'])
                    sys.exit(-1)
        except:
            print('Server failed to respond')
            sys.exit(-1)

    def get_char(self, data):
        """ Find maximum frequency in fft data then find the closest
            frequency in chirp map and return character """
        freq = self.dsp.max_freq(data)
        ch, f = min(self.map.items(), key=lambda kv: abs(kv[1] - freq))
        return ch

    def callback(self, data, frames, info, status):
        """ Callback from pyaudio once a chars worth
            of data is loaded into the buffer """
        audio = np.fromstring(data, dtype=np.int16)
        self.amplitude = np.average(abs(audio)) + MIN_AMPLITUDE
        if max(audio) > self.amplitude:
            thread = DecodeThread(self.process, audio)
            thread.start()
        return (None, pyaudio.paContinue)

    def process(self, data):
        """ Process data to chirp characters and add to a window
            Once the frontdoor pair is located, decode the chirp """
        chirplen = len(self.chirp)
        freq = self.dsp.max_freq(data)
        ch, f = min(self.map.items(), key=lambda kv: abs(kv[1] - freq))

        self.chirp += ch
        chirplen = len(self.chirp)
        self.chirp = self.chirp[1:] if chirplen > 20 else self.chirp
        if chirplen >= 20 and self.chirp[0:2] == 'hj':
            self.decode(self.chirp)

    def authenticate(self):
        """ Convert an app key/secret to an API token """
        payload = {
            'app_key': '9iBEhpigPgRkUjM3dK3B4blkA',
            'app_secret': 'AVg3iC954Z3bzpZJNwxINsGhKh3jLDBpmAhZqLSxKqEjSyZMYf',
            'device_id': str(uuid.uuid1())
        }
        r = requests.post(self.BASE_URL + '/authenticate', json=payload)
        if r.status_code == 200:
            rsp = r.json()
            return rsp['access_token']

    def decode(self, code):
        """ Run error correction on chirp and get content """
        print('Found Chirp!')
        print(code)
        code = self.ecc_decode(code)
        r = requests.get(self.BASE_URL + '/chirps/' + code[2:12], headers=self.headers)
        if r.status_code == 200:
            rsp = r.json()
            print('%s' % rsp['data'])
            if rsp['data'].get('url'):
                url = (rsp['data']['url'] if
                    rsp['data']['url'].startswith('http') else
                    'http://' + rsp['data']['url']
                )
                webbrowser.open(url)

    def encode(self, code):
        """ Generate audio data from a chirp string """
        samples = np.array([], dtype=np.int16)
        code = self.ecc_encode(code)

        for s in code:
            freq = self.map[s]
            char = self.dsp.sine_wave(freq, self.CHAR_LENGTH)
            samples = np.concatenate([samples, char])

        samples = (samples * self.CHIRP_VOLUME).astype(np.int16)
        return samples

    def ecc_encode(self, code):
        """ Reed Solomon Error Correction Encoding """
        r = requests.get(self.BASE_URL + '/encode/' + code)
        if r.status_code == 200:
            rsp = r.json()
            return rsp['longcode']
        return code

    def ecc_decode(self, longcode):
        """ Reed Solomon Error Correction Decoding """
        r = requests.get(self.BASE_URL + '/decode/' + longcode)
        if r.status_code == 200:
            rsp = r.json()
            return rsp['shortcode']
        return longcode


class DecodeThread(threading.Thread):
    """ Thread to run digital signal processing functions """
    def __init__(self, fn, *args):
        self.fn = fn
        self.args = args
        self.thread = threading.Thread.__init__(self)

    def run(self):
        self.fn(*self.args)

    def stop(self):
        self.thread.set()

    def stopped(self):
        return self.thread.isSet()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Chirp.io Encoder/Decoder')
    parser.add_argument('-l', '--listen', action='store_true', default=False, help='listen out for a chirp')
    parser.add_argument('-u', '--url', help='chirp a url')
    parser.add_argument('-c', '--code', help='chirp a code')
    args = parser.parse_args()

    chirp = Chirp()
    audio = Audio(chirp.callback)

    if args.listen:
        try:
            print('Recording...')
            audio.record()
            time.sleep(300)

        except KeyboardInterrupt:
            print('Exiting..')
            sys.exit(0)

    elif args.code:
        samples = chirp.encode(args.code)
        print('Chirping code: %s' % args.code)
        audio.play(samples)

    elif args.url:
        code = chirp.get_code(args.url)
        samples = chirp.encode(code)
        print('Chirping url: %s' % args.url)
        audio.play(samples)

    else:
        print('No arguments specified!')
        print('Exiting..')

    sys.exit(0)
