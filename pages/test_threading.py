import streamlit as st
import threading
import pyaudio
import wave

class SoundRecorder:
    def __init__(self, path):
        self.format = pyaudio.paInt16
        self.channels = 1
        self.sample_rate = 44100
        self.chunk = 1024
        self.duration = 5
        self.frames = []
        self.path = path
        self.audio = pyaudio.PyAudio()

    def record(self):
        st.write("Recording...")
        stream = self.audio.open(format=self.format,
                                 channels=self.channels,
                                 rate=self.sample_rate,
                                 input=True,
                                 frames_per_buffer=self.chunk)

        while not self.stop_event.is_set():
            data = stream.read(self.chunk)
            self.frames.append(data)

        stream.stop_stream()
        stream.close()
        self.audio.terminate()
        self.save()

    def save(self):
        with wave.open(self.path, 'wb') as wf:
            wf.setnchannels(self.channels)
            wf.setsampwidth(self.audio.get_sample_size(self.format))
            wf.setframerate(self.sample_rate)
            wf.writeframes(b''.join(self.frames))
        st.write(f"Recording saved as {self.path}")

def record_audio(recorder):
    recorder.record()

if __name__ == "__main__":
    if 'recording_stop_event' not in st.session_state:
        st.session_state.recording_stop_event = threading.Event()

    if st.button("Stop Recording"):
        st.session_state.recording_stop_event.set()

    if st.button("Start Recording"):
        st.session_state.recording_stop_event.clear()
        recorder = SoundRecorder("output.wav")
        recorder.stop_event = st.session_state.recording_stop_event
        recording_thread = threading.Thread(target=record_audio, args=(recorder,))
        recording_thread.start()
