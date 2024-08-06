import pyaudio
import wave
import logging

import librosa
import librosa.display
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import streamlit as st


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SoundRecorder(object):
    def __init__(self):
        self.format = pyaudio.paInt16
        self.channels = 1
        self.sample_rate = 44100
        self.chunk = 1024
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

    def record(self, duration=5.1):
        self.duration = duration
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


    def save(self):
        with wave.open(self.path, 'wb') as wf:
            wf.setnchannels(self.channels)
            wf.setsampwidth(self.audio.get_sample_size(self.format))
            wf.setframerate(self.sample_rate)
            wf.writeframes(b''.join(self.frames))
        st.write(f"Recording saved as {self.path}")

    def get_spectrogram(self, type='mel'):
        st.write("Extracting spectrogram...")
        y, sr = librosa.load(self.path, duration=self.duration)
        ps = librosa.feature.melspectrogram(y=y, sr=sr, n_mels=128)

        st.write("Spectrogram extracted.")
        format_str = '%+2.0f'
        if type == 'DB':
            ps = librosa.power_to_db(ps, ref=np.max)
            format_str += 'DB'
            st.write("Converted to DB scale.")
        return ps, format_str

    def display_spectrogram(self, spectrogram, format_str):
        import matplotlib.colors as mcolors

        fig, ax = plt.subplots(figsize=(10, 4))
        cmap = plt.get_cmap('viridis')
        V = 3
        cmap.set_bad(alpha=0)  # Set alpha channel for zero values
        # Create a new colormap with alpha channel
        alpha = 0.5  # Set the alpha value (0 is fully transparent, 1 is fully opaque)
        new_cmap = mcolors.LinearSegmentedColormap.from_list('alpha_viridis', cmap(np.linspace(0, 1, 256)), N=256)
        new_cmap._init()  # Initialize the colormap
        # Set the alpha value for the colormap
        new_cmap._lut[:, -1] = alpha  # Set alpha channel for all colors in the colormap
        st.write(new_cmap._lut)
        
        librosa.display.specshow(spectrogram, y_axis='mel', x_axis='time', cmap=cmap, vmin=-V, vmax=V)
        # librosa.display.specshow(spectrogram, y_axis='mel', x_axis='time', cmap='gray_r', vmin=-1, vmax=1)

        ax.set_title('Mel-frequency spectrogram')
        plt.colorbar(format=format_str, ax=ax)
        plt.tight_layout()
        st.pyplot(fig, clear_figure=False)
        

recorder = SoundRecorder()


if not 'recording' in st.session_state:
    st.session_state.recording = False

