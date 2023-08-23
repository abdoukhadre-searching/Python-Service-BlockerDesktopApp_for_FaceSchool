import os
from datetime import datetime
from pathlib import Path

process_name = "vlc.exe"
Path('log_test.txt').touch()
# while True:
with open('log_test.txt', 'a+', encoding='utf-8') as file:
    file.write(
        f"Process: {process_name} kill by FS_Agent at {str(datetime.now())} \n")
