import numpy as np
import os
import re
import argparse
import nltk
from nltk.corpus import cmudict
import audio as a


parser = argparse.ArgumentParser(description='text to speech')
parser.add_argument('--speak', '-s', action="store_true", default=False, help="speaks the output audio")
parser.add_argument('text', nargs=1, help="The text to be synthesised")

args = parser.parse_args()

class Synthesis:
    def __init__(self, wav_folder):
        self.concatenatedsound = {}
        if os.path.isdir("./corpora/cmudict"):
            dl = nltk.downloader.Downloader()
            dl._update_index()
            dl._status_cache['cmudict'] = 'installed' # Trick the index to treat cmudict as it's already installed.
        else:
            nltk.download('cmudict', download_dir="./")
            dl = nltk.downloader.Downloader()
            dl._update_index()
            dl._status_cache['cmudict'] = 'installed' # Trick the index to treat cmudict as it's already installed.
        nltk.data.path = "./"
        tmpaudio = a.Audio(rate=16000)  # Audio_obj
        for file in os.listdir(wav_folder):
            if file.endswith(".wav"):
                try:
                    sound = file.split(".")[0]
                    wav_path = os.path.join(wav_folder, file)
                    tmpaudio.load(wav_path)
                    self.concatenatedsound[sound] = tmpaudio.data
                except Exception as e:
                    # print the exception as an error message
                    print(str(e))
                    pass
        length = 16000 * 0.1  # sample rate = 16 kHz, frame size = 0.1 seconds
        self.concatenatedsound[' '] = np.zeros(int(length), tmpaudio.nptype)
        length = 16000 * 0.2 # sample rate = 16 kHz, frame size = 0.2 seconds
        self.concatenatedsound[','] = np.zeros(int(length), tmpaudio.nptype)
        length = 16000 * 0.4 # sample rate = 16 kHz, frame size = 0.4 seconds
        self.concatenatedsound[':'] = np.zeros(int(length), tmpaudio.nptype)
        self.concatenatedsound['!'] = np.zeros(int(length), tmpaudio.nptype)
        self.concatenatedsound['?'] = np.zeros(int(length), tmpaudio.nptype)
        self.concatenated_wavs = self.concatenatedsound


class Speech:
    def __init__(self, text):
        print(text)
        self.text = text.lower()
        self.text = re.split(r"([?!.,:\s+])", self.text)
        self.sequence = []
        print(str(self.text))
        dict = cmudict.dict()
        sequence = []
        for word in self.text:
            if 1 > len(word):
                continue
            if word in ' ?!,.:':
                sequence.append([word])
            else:
                if word in dict:
                    diphone = dict[word][0]
                    for i in range(len(diphone)):
                        diphone[i] = re.sub("[^a-zA-Z\\s\-]", "", diphone[i]).lower()
                    sequence.append(diphone)
        self.sequence = sequence

    def concatenate_diphones(self):
        global diphone, tmp
        leading_whitespace = False
        sentence_1 = False
        sentence_number = 0
        i = 0
        for sequence in self.sequence:
            if (len(sequence) == 1) and (sequence[0] in ' ,.:?!'):
                if sequence[0] == " ":
                    leading_whitespace = True
                elif "?" in sequence or '.' in sequence or "!" in sequence:
                    sentence_1 = True
                    sentence_number = i + 1 # the sentence number is the index of the first word of the sentence
                    # if i > 0:
                    #     self.sequence[i - 1].append(" ")
                    # else:
                    #     self.sequence[i].append(" ")
                    #concatenatedsound.insert(i, " ")
                    # inserts a space in the concatenated sound before and after the seq in self.sequence and splits the concatenated sound into a list of sounds)
                    concatenatedsound.insert(len(concatenatedsound), concatenatedsound[len(concatenatedsound) - 1].split("-")[1] + "-pau")
                else:
                    concatenatedsound.append(sequence[0])
            else:
                if sentence_1 and i == sentence_number:
                    #concatenatedsound.append("-pau")
                    # insert the first diphone of the sentence as pau- for pause
                    concatenatedsound.insert(len(concatenatedsound), "pau-" + sequence[0])
                for j in range(1, len(sequence)):
                    # this append to concatenated sounds as a bit of a hack, but it works until I can figure out a better way
                    concatenatedsound.append(sequence[j - 1] + '-' + sequence[j])
                if leading_whitespace:
                    #concatenatedsound.insert(len(concatenatedsound), "pau-" + seq[len(seq) - 1])
                    # inserts pau- for a pause diphone where self.sequence[i][-1] is the last diphone per word
                    # self.sequence[i][0] is the first diphone per word
                    concatenatedsound.insert(len(concatenatedsound) - j, self.sequence[i - 2][-1] + "-" + self.sequence[i][0])
                    leading_whitespace = False
            if i == 0:
                # inserts the first diphone of the sentence as pau- for pause
                concatenatedsound.insert(0, "pau-" + self.sequence[i][0])
            elif i == (len(self.sequence) - 1):
                # inserts the last diphone of the sentence as pau- for pause
                concatenatedsound.insert(len(concatenatedsound), sequence[len(sequence) - 1] + "-pau")
            i += 1
        print(concatenatedsound)
        for sound in concatenatedsound:
            try:
                # appends the diphone to the concatenated sound
                tmp = np.append(tmp, (diphone_synthesis.concatenatedsound[sound]))
            except Exception as e:
                print(str(e))
                pass

if __name__ == "__main__":
    nltk.data.path = "./"
    concatenatedsound = []
    tmp = []
    
    diphone_synthesis = Synthesis(wav_folder="./cstr_en_us")
    out = a.Audio(rate=16000)

    speech = Speech(args.text[0])
    speech.concatenate_diphones()

    out.data = tmp.astype(np.int16)
    print(out.data, type(out.data))

    if args.speak is True:
        out.play()

    out.plot_waveform()
