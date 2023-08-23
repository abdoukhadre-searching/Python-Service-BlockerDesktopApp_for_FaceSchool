#!python
# coding: utf-8
import sys
import ctypes
from python_hosts import Hosts, HostsEntry
import os
import platform
from pathlib import Path
from websiteEnum import Websites

unicode = str

def run_as_admin(argv=None, debug=False):
    shell32 = ctypes.windll.shell32
    if argv is None and shell32.IsUserAnAdmin():
        return True

    if argv is None:
        argv = sys.argv
    if hasattr(sys, '_MEIPASS'):
        # Support pyinstaller wrapped program.
        arguments = map(unicode, argv[1:])
    else:
        arguments = map(unicode, argv)
    argument_line = u' '.join(arguments)
    executable = unicode(sys.executable)
    if debug:
        print ('Command line: ', executable, argument_line)
    ret = shell32.ShellExecuteW(None, u"runas", executable, argument_line, None, 1)
    if int(ret) <= 32:
        return False
    return None


if __name__ == '__main__':
    ret = run_as_admin()

    if ret is True:
        print('I have admin privilege.')
        # raw_input('Press ENTER to exit.')
    elif ret is None:
        print ('I am elevating to admin privilege.')
        # raw_input('Press ENTER to exit.')        
        if platform.system() == 'Windows':
            myetcFilePath = Path(os.environ['DRIVERDATA']).parent / 'etc/hosts'
            print(myetcFilePath)
        elif platform.system() == 'Linux':
            myetcFilePath = Path('/etc/hosts')

        hosts = Hosts(path=myetcFilePath)
        new_entry = HostsEntry(entry_type='ipv4', address='127.0.0.1', names=[Websites.FACE_SCHOOL_ALIAS.value, Websites.FACE_SCHOOL.value])
        
        # hosts.add([new_entry])
        
        # i remove all matching site
        hosts.remove_all_matching(name=Websites.FACE_SCHOOL.value)
        hosts.remove_all_matching(name=Websites.FACE_SCHOOL_ALIAS.value)
        
        hosts.write()
        print("Its done file updated ! good")
    else:
        print ('Error(ret=%d): cannot elevate privilege.' % (ret, ))