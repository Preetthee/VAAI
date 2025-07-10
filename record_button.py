import os
import numpy as np
import sounddevice as sd
from scipy.io.wavfile import write
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtCore import QEvent
import subprocess


class RecordButton(QPushButton):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setText(text)
        self.fs = 44100
        self.stream = None
        self.recording_data = []
        self.is_recording = False

        self.installEventFilter(self)

    def eventFilter(self, source, event):
        if source == self:
            if event.type() == QEvent.MouseButtonPress:
                self.setText("Recording...")
                self.start_recording()
            elif event.type() == QEvent.MouseButtonRelease:
                self.setText("Hold to Record")
                self.stop_recording()
        return super().eventFilter(source, event)

    def audio_callback(self, indata, frames, time, status):
        if self.is_recording:
            self.recording_data.append(indata.copy())

    def start_recording(self):
        self.recording_data = []
        self.is_recording = True
        self.stream = sd.InputStream(samplerate=self.fs, channels=2, callback=self.audio_callback)
        self.stream.start()
        print("Recording started...")

    def stop_recording(self):
        self.is_recording = False
        self.stream.stop()
        self.stream.close()
        print("Recording stopped.")

        audio = np.concatenate(self.recording_data, axis=0)
        wav_path = "temp.wav"
        mp3_path = "recording.mp3"
        write(wav_path, self.fs, audio)

        subprocess.run(["ffmpeg", "-y", "-i", wav_path, mp3_path],
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        os.remove(wav_path)
        print("Saved as recording.mp3")

