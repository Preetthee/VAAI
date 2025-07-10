import os
import numpy as np
import sounddevice as sd
from scipy.io.wavfile import write
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtCore import QEvent
import subprocess
import json
import os
from datetime import datetime
from generate_filename import (
    FILE,
    load_recordings,
    get_next_id,
    generate_filename,
    get_current_iso_time
)


class RecordButton(QPushButton):
    def __init__(self, text, parent=None, list_view=None):
        super().__init__(text, parent)
        self.setText(text)
        self.fs = 44100
        self.stream = None
        self.recording_data = []
        self.is_recording = False
        self.list_view = list_view 

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

        FILE = "recording.json"

        recordings = load_recordings()

        record_id = get_next_id(recordings)
        filename = generate_filename(record_id) 
        write(filename, self.fs, audio)
        print(f"Saved as {filename}")

        file_size = os.path.getsize(filename)
        num_samples = audio.shape[0]
        duration = num_samples / self.fs

    
        base_filename = os.path.basename(filename)

        new_recording = {
            "id": record_id,
            "filename": base_filename,
            "date": get_current_iso_time(),
            "path": os.path.abspath(filename),
            "size_bytes": file_size,
            "duration_seconds": duration
        }

        recordings.append(new_recording)
        with open(FILE, 'w') as f:
            json.dump(recordings, f, indent=2)

        if self.list_view is not None:
            self.list_view.refresh()

