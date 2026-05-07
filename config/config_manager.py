import os
import json, shutil
from PyQt6.QtCore import QStandardPaths

is_flatpak_env = 'FLATPAK_ID' in os.environ or os.path.exists('/.flatpak-info')
base_config = QStandardPaths.writableLocation(QStandardPaths.StandardLocation.GenericConfigLocation)

CONFIG_DIR = os.path.join(base_config, "amethyst_miner")
os.makedirs(CONFIG_DIR, exist_ok=True)
CONFIG_FILE = os.path.join(CONFIG_DIR, "settings.json")
MINER_DIR = "/app/bin" if is_flatpak_env else os.path.join(CONFIG_DIR, "bin")
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GUI_DIR = os.path.join(BASE_DIR, "gui")
CORE_DIR = os.path.join(BASE_DIR, "core")

if os.name == "nt":
    files_to_copy = [os.path.join(CORE_DIR, "xmrig.exe"), os.path.join(CORE_DIR, "WinRing0x64.sys")]
    for file_name in files_to_copy:
        source_path = os.path.join(CORE_DIR, file_name)
        dest_path = os.path.join(MINER_DIR, file_name)

        if os.path.exists(source_path):
            try:
                shutil.copy2(source_path, dest_path)
                print(f"Successfully copied: {file_name} -> {MINER_DIR}")
            except Exception as e:
                print(f"Error copying {file_name}: {e}")
        else:
            print(f"Warning: Could not find {file_name} in {CORE_DIR}")

def get_icon_path(name):
    return os.path.join(GUI_DIR, name)

def load_config():
    defaults = {
        "worker_name": "LinuxRig-01",
        "wallet": "",
        "pool": "pool.supportxmr.com:3333",
        "threads": max(1, os.cpu_count() - 1) if os.cpu_count() else 1,
        "priority": 2,
        "idle_enabled": False,
        "enable_msr": False,
        "idle_minutes": 5,
        "schedule_enabled": False,
        "schedule_start": "22:00",
        "schedule_stop": "08:00",
        "autostart_enabled": True,
        "already_seen_message": True
    }
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE) as f:
                defaults.update(json.load(f))
        except Exception:
            pass
    return defaults

def save_config(data):
    os.makedirs(CONFIG_DIR, exist_ok=True)
    with open(CONFIG_FILE, "w") as f:
        json.dump(data, f, indent=4)