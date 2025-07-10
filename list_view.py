import json
from PyQt5.QtWidgets import QListWidget, QListWidgetItem
from generate_filename import FILE, load_recordings

class RecordingsListView(QListWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.refresh()

    def refresh(self):
        self.clear()
        recordings = load_recordings()
        for rec in recordings:
            display = (
                f"ID: {rec.get('id')} | "
                f"File: {rec.get('filename')} | "
                f"Date: {rec.get('date')} | "
                f"Duration: {rec.get('duration_seconds'):.2f}s | "
                f"Size: {rec.get('size_bytes')} bytes"
            )
            item = QListWidgetItem(display)
            self.addItem(item)