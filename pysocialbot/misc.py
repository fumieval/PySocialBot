import os
from pysocialbot.settings import TW_USER_DB_PATH

def apply_settings():
    t_dir = os.path.dirname(TW_USER_DB_PATH)
    if not os.path.exists(t_dir):
        os.makedirs(t_dir, 0700)
