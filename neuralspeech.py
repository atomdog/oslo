import numpy as np
import soundfile as sf
import yaml

import tensorflow as tf

from tensorflow_tts.inference import TFAutoModel
from tensorflow_tts.inference import AutoProcessor


import sounddevice as sd
import simpleaudio as sa
import time

def speak():
     try:
        print("< ----------- Instantiating in Neural Speech  ----------- >")
        # initialize fastspeech2 model.
        fastspeech2 = TFAutoModel.from_pretrained("tensorspeech/tts-fastspeech2-ljspeech-en")
        # initialize mb_melgan model
        mb_melgan = TFAutoModel.from_pretrained("tensorspeech/tts-mb_melgan-ljspeech-en")
        # inference
        processor = AutoProcessor.from_pretrained("tensorspeech/tts-fastspeech2-ljspeech-en")
    except Exception as e:
        print("< ------ Exception in Instantiating Neural Speech  ------ >")
        print(type(e).__name__ + ': ' + str(e))
    lc = True
    yield(True)
    while(lc):
        spkstring = yield
        input_ids = processor.text_to_sequence(spkstring)
# fastspeech inference

        mel_before, mel_after, duration_outputs, _, _ = fastspeech2.inference(
            input_ids=tf.expand_dims(tf.convert_to_tensor(input_ids, dtype=tf.int32), 0),
            speaker_ids=tf.convert_to_tensor([0], dtype=tf.int32),
            speed_ratios=tf.convert_to_tensor([1.0], dtype=tf.float32),
            f0_ratios =tf.convert_to_tensor([1.0], dtype=tf.float32),
            energy_ratios =tf.convert_to_tensor([1.0], dtype=tf.float32),
        )

        # melgan inference
        audio_before = mb_melgan.inference(mel_before)[0, :, 0]
        audio_after = mb_melgan.inference(mel_after)[0, :, 0]


#sf.write('./audio_before.wav', audio_before, 22050, "PCM_16")
#sf.write('./currentaudio.wav', audio_after, 22050, "PCM_16")
        print("//speaking: ")
        durationspeech = len(audio_after)/22050
        sd.play(audio_after, 22050)
        time.sleep(durationspeech)
        sd.stop()
        print("//finished speaking")
        yield('complete')
