import pyaudio
import numpy as np
import matplotlib.pyplot as plt
from io import BytesIO
import base64

def initialize_stream():
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16,
                    channels=1,
                    rate=44100,
                    input=True,
                    frames_per_buffer=1024)
    return p, stream

def generate_plot(stream):
    plt.switch_backend('Agg')
    plt.ion()
    fig, ax = plt.subplots()
    x = np.arange(0, 1024)
    line, = ax.plot(x, np.random.rand(1024))
    ax.set_ylim(-32768, 32768)
    ax.set_xlim(0, 1024)
    ax.set_title('Sound Waves Visualization')
    ax.set_xlabel('Time')
    ax.set_ylabel('Amplitude')
    return fig, ax, line

def generate_plot_image(fig):
    buf = BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)
    return base64.b64encode(buf.getvalue()).decode('utf-8')

def plot_generator(stream):
    fig, ax, line = generate_plot(stream)
    data = stream.read(1024)
    data_np = np.frombuffer(data, dtype=np.int16)
    line.set_ydata(data_np)
    fig.canvas.draw()
    return generate_plot_image(fig)  

def close_stream(p, stream):
    stream.stop_stream()
    stream.close()
    p.terminate()
