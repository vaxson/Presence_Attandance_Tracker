# utils/helper/paths.py
import sys
import os

def resource_path(relative):
    if getattr(sys, 'frozen', False):
        base = sys._MEIPASS
    else:
        base = os.path.dirname(os.path.abspath(__file__ + "/../.."))
        # goes up 3 levels: paths.py → helper → utils → project root
    return os.path.join(base, relative)

def database_path(filename):
    if getattr(sys, 'frozen', False):
        base = os.path.dirname(sys.executable)
    else:
        base = os.path.dirname(os.path.abspath(__file__ + "/../.."))
    db_dir = os.path.join(base, 'Database')
    os.makedirs(db_dir, exist_ok=True)
    return os.path.join(db_dir, filename)