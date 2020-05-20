#!/usr/bin/env python3

import os
import numpy
import random
import string
import cv2
import argparse
import captcha.image
import captcha.audio
from captcha.audio import AudioCaptcha
from gtts import gTTS
from pydub import AudioSegment
import matplotlib.pyplot as plt
from scipy import signal
from scipy.io import wavfile
import wave
import pylab


# Step 1: Need a way to save wav and spec files in a dir. Done.
# Step 2: Need to be able to specify the dir name
# Step 3: Use the variable that contains the dir name



print(os.path.curdir)
# python generateaudio.py --count 2 --output-dir aud1 --wav-dir aud2 --spec-dir aud3 --symbols symbols1.txt --length 8
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--count', help='How many captchas to generate', type=int)
    parser.add_argument('--output-dir', help='Where to store the generated captchas', type=str)
    parser.add_argument('--wav-dir', help='Where to store the converted wav files',type=str)
    parser.add_argument('--spec-dir', help='Where to store the converted spectogram files',type=str)
    parser.add_argument('--symbols', help='Where to store the generated captchas', type=str)
    parser.add_argument('--length', help='Length of captchas in characters', type=int)
    args = parser.parse_args()

    if args.count is None:
        print("Please specify the captcha count to generate")
        exit(1)

    if args.output_dir is None:
        print("Please specify the captcha output directory")
        exit(1)
    
    if args.wav_dir is None:
        print("Please specify the wave file o/p directory")
        exit(1)

    # THIS IS WHERE THE PATH NAME WILL BE PASSED
    if args.spec_dir is None:
        print("Please specify the spec files directory")
        exit(1)

        
    if args.length is None:
        print("Please specify the captcha length")
        exit(1)

      
    if args.symbols is None:
        print("Please specify the captcha symbols file")
        exit(1)    


    #captcha_generator = captcha.audio.AudioCaptcha()


    symbols_file = open(args.symbols, 'r')
    captcha_symbols = symbols_file.readline().strip()
    symbols_file.close()

    print("Generating captchas with symbol set {" + captcha_symbols + "}")
    
    if not os.path.exists(args.output_dir):
        print("Creating output directory " + args.output_dir)
        os.makedirs(args.output_dir)

    letterToPronunciationMap = {
        '0': 'zero-', '1': 'one-', '2': 'two-', '3': 'three-', 
        '4': 'four-', '5': 'five-', '6': 'six-', '7': 'seven-', 
        '8': 'eight-', '9': 'nine-', 'A': 'A-',
'B': 'B-',
'C': 'C-',
'D': 'D-',
'E': 'E-',
'F': 'F-',
'G': 'G-',
'H': 'H-',
'I': 'I-',
'J': 'J-',
'K': 'K-',
'L': 'L-',
'M': 'M-',
'N': 'N-',
'O': 'O-',
'P': 'P-',
'Q': 'Q-',
'R': 'R-',
'S': 'S-',
'T': 'T-',
'U': 'U-',
'V': 'V-',
'W': 'W-',
'X': 'X-',
'Y': 'Y-',
'Z': 'Z-'}

    for i in range(args.count):
        
        captcha_letters = [random.choice(captcha_symbols) for j in range(args.length)]
        captcha_pronunciation = ''.join([letterToPronunciationMap[letter] for letter in captcha_letters])
        captcha_text = ''.join(captcha_letters)

        #mp3_path = os.path.join(args.output_dir, captcha_text+'.mp3')
        mp3_path = os.path.join('P:\\mp3', args.output_dir, captcha_text+'.mp3')
        if os.path.exists(mp3_path):
            version = 1
            while os.path.exists(os.path.join('P:\\mp3', args.output_dir, captcha_text + '_' + str(version) + '.mp3')):
                version += 1
            mp3_path = os.path.join('P:\\mp3', args.output_dir, captcha_text + '_' + str(version) + '.mp3')
        #audio = captcha_generator.generate(captcha_text)
        
        print (mp3_path)
        # captcha_generator.write(mp3_path, audio)
        #captcha_generator.write(captcha_text, mp3_path)
        tts=gTTS(text=captcha_pronunciation,lang='en')
        tts.save(mp3_path)
        # mp3_path = os.path.join(os.path.abspath('P:\\mp3'), mp3_path)
        
        #print(mp3_path)
        
        #converting mp3 to wav
        #wave_path = os.path.join(os.path.dirname(mp3_path), captcha_text+'.wav')
        wave_path = os.path.join(os.path.abspath('P:\\wave'), args.wav_dir, captcha_text+'.wav')
        print(wave_path)
        sound = AudioSegment.from_mp3(mp3_path)
        sound.export(wave_path, format="wav")

        #converting to spectogram
        #spect_path = os.path.join(os.path.dirname(mp3_path), captcha_text+'.png')
        spect_path = os.path.join(os.path.abspath('.'), args.spec_dir, captcha_text+'.png')
        wav = wave.open(wave_path, 'r')
        frames = wav.readframes(-1)
        sound_info = pylab.fromstring(frames,  'int16')
        frame_rate = wav.getframerate()
        wav.close()
        pylab.specgram(sound_info, Fs=frame_rate)
        pylab.savefig(spect_path, dpi=100, frameon='false', aspect='normal', bbox_inches='tight', pad_inches=0)
        del frames, frame_rate, sound, wav





if __name__ == '__main__':
    main()

    

