import streamlit as st
import pyaudio
import wave

import streamlit as st
import logging
import pyaudio, wave, os
import numpy as np
import librosa
import librosa.display
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def create_custom_colormap(colors, alpha_values):
    """
    Create a custom colormap with specified alpha values.
    
    Args:
        colors (list): List of colors for the colormap.
        alpha_values (list): List of alpha values for each color.
        
    Returns:
        ListedColormap: Custom colormap.
    """
    # Create the colormap
    cmap = ListedColormap(colors, name='custom_colormap')
    cmap._init()
    
    # Set the alpha values for each color
    total_colors = len(colors)
    color_indices = np.linspace(0, 100, total_colors + 1, dtype=int)
    for i in range(total_colors):
        start_index = color_indices[i]
        end_index = color_indices[i + 1]
        cmap._lut[start_index:end_index, -1] = alpha_values[i]
    
    return cmap

class SoundRecorder(object):
    def __init__(self):
        self.format = pyaudio.paInt16
        self.channels = 1
        self.sample_rate = 44100
        self.chunk = 1024
        self.duration = 5.1
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

if st.button("Stop Recording"):
    st.session_state.recording = False
    
if st.button("Start Recording"):
    st.session_state.recording = True
    with st.spinner("Recording..."):
        recorder.record()



if st.button('Play'):
    # sound.play()
    try:
        audio_file = open("output.wav", 'rb')
        audio_bytes = audio_file.read()
        st.audio(audio_bytes, format='audio/wav')
        # Once recording is finished, extract and display spectrogram
        
    except:
        st.write("Please record sound first")

if st.button('Display Spectrogram'):
    ps, format_str = recorder.get_spectrogram()
    recorder.display_spectrogram(ps, format_str)
    
colors = ['blue', 'green', 'yellow', 'red']
alpha_values = [0, 1, 1, 0]
cmap = create_custom_colormap(colors, alpha_values)

# Generate some sample data
data = np.random.rand(10, 10) * 0.2 - 0.1

# Plot the data using the custom colormap
plt.imshow(data, cmap=cmap)
plt.colorbar()
plt.show()



st.divider()
from lib.sound import SoundRecorder

if st.button("Start Recording", key="start_recording"):
    st.session_state.recording = True
    with st.spinner("Recording..."):
        recorder.record()
