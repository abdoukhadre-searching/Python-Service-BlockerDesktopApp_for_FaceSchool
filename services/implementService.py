import time
import random
from pathlib import Path
from SMWinservice import SMWinservice
import psutil
import os
from datetime import datetime


class faceSchoolService(SMWinservice):
    _svc_name_ = "FaceSchoolAgent"
    _svc_display_name_ = "FaceSchool_Agent Service"
    _svc_description_ = "Surveille le démarrage de certaines applications suspectes par le produit FaceSchoolProctoring"

    def start(self):
        self.isrunning = True

    def stop(self):
        self.isrunning = False

    def kill_by_process_name(self, name):
        for proc in psutil.process_iter():
            if proc.name() == name:
                # print("Killing process: " + name)
                try:
                    os.system("taskkill /f /pid "+str(proc.pid))
                    print("Killing process: " + name + " sucess 🟢")
                except:
                    print("Killing process: " + name + " failed")
                return
        print("Not found process: " + name)

    def main(self):
        Path('log.txt').touch()
        print('File log.txt created 🟢')
        process_names = ['vlc.exe', 'notepad.exe']

        while self.isrunning:
            for process in process_names:
                self.kill_by_process_name(process)
                with open('log.txt', 'a+', encoding='utf-8') as file:
                    file.write(
                        f"Process: {process_names} arrété par le FaceSchool_Agent Service à exactement: {str(datetime.now())} \n")
                time.sleep(2)


if __name__ == '__main__':
    faceSchoolService.parse_command_line()
