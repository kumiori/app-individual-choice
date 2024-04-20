import streamlit as st
import pyaudio
import wave

import streamlit as st
import logging
import pyaudio, wave, os
import numpy as np

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SoundRecorder(object):
    def __init__(self):
        self.format = pyaudio.paInt16
        self.channels = 1
        self.sample_rate = 44100
        self.chunk = 1024
        self.duration = 5
        self.frames = []
        self.path = "output.wav"
        self.audio = pyaudio.PyAudio()
        self.device_info()

    def device_info(self):
        num_devices = self.audio.get_device_count()
        logger.info(f"Number of audio devices: {num_devices}")
        for i in range(num_devices):
            info_dict = self.audio.get_device_info_by_index(i)
            logger.info(f"Device {i}: {info_dict['name']}")

    def record(self):
        st.write("Recording...")
        self.frames = []
        progress = st.progress(0)
        stream = self.audio.open(format=self.format,
                                 channels=self.channels,
                                 rate=self.sample_rate,
                                 input=True,
                                 frames_per_buffer=self.chunk)

        for i in range(0, int(self.sample_rate / self.chunk * self.duration)):
                progress.progress(i / int(self.sample_rate / self.chunk * self.duration))
                data = stream.read(self.chunk)
                self.frames.append(data)
                st.spinner(f"Recording... {i}/{int(self.sample_rate / self.chunk * self.duration)}")
                
        stream.stop_stream()
        stream.close()
        self.audio.terminate()
        self.save()

    # def record(self):
    #     st.write("Recording...")
    #     self.frames = []
    #     self.stream = self.audio.open(format=self.format,
    #                                   channels=self.channels,
    #                                   rate=self.sample_rate,
    #                                   input=True,
    #                                   frames_per_buffer=self.chunk)
    #     duration = 0
    #     while duration < 600 and st.session_state.recording:
    #         data = self.stream.read(self.chunk)
    #         self.frames.append(data)
    #         duration += 1
        
    #     self.stream.stop_stream()
    #     self.stream.close()
    #     self.audio.terminate()
    #     self.save()


    def save(self):
        with wave.open(self.path, 'wb') as wf:
            wf.setnchannels(self.channels)
            wf.setsampwidth(self.audio.get_sample_size(self.format))
            wf.setframerate(self.sample_rate)
            wf.writeframes(b''.join(self.frames))
        st.write(f"Recording saved as {self.path}")

recorder = SoundRecorder()

if not 'recording' in st.session_state:
    st.session_state.recording = False

if st.button("Stop Recording"):
    st.session_state.recording = False
    
if st.button("Start Recording"):
    st.session_state.recording = True
    recorder.record()
