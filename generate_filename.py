import json
import os
from datetime import datetime
import re

FILE = "recording.json"

def load_recordings():
    if not os.path.exists(FILE):
        with open(FILE, 'w') as f:
            json.dump([], f)
        return []
    with open(FILE, 'r') as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

def get_next_id(recordings):
    return (recordings[-1]['id'] + 1) if recordings else 1

def get_today_date():
    return datetime.now().strftime("%Y-%m-%d")

def generate_filename(record_id):
    now = datetime.now()
    date_str = now.strftime("%Y-%m-%d")
    time_str = now.strftime("%H-%M-%S")
    directory = os.path.join("assets", "records")
    os.makedirs(directory, exist_ok=True)
    return os.path.join(directory, f"recording_{record_id}-{date_str}_{time_str}.wav")

def get_current_iso_time():
    return datetime.now().isoformat(timespec='seconds')

user_input = "example/user_input.wav"
safe_name = re.sub(r'[^a-zA-Z0-9_\-]', '', user_input)
base_dir = os.path.abspath("assets/records")
full_path = os.path.abspath(os.path.join(base_dir, safe_name))
if not full_path.startswith(base_dir):
    raise ValueError("Invalid file path")