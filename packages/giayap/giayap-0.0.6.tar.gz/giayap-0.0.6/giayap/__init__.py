import os, time
from .__version__ import __version__

yaml_file_content = \
r'''---
refresh_rate: 300 seconds
appenders:
  stdout:
    kind: console
    encoder:
      pattern: "{d(%Y-%m-%d-%H-%M-%S)}|{l}|{m}\n"
  collect_info:
    kind: file
    path: "yap_log_path_123\\logs\\collect.log"
    encoder:
      pattern: "{d(%Y-%m-%d-%H-%M-%S)}|{l}|{m}\n"
  file:
    kind: file
    path: "yap_log_path_123\\logs\\log.log"
    encoder:
      pattern: "{d(%Y-%m-%d-%H-%M-%S)}|{l}|{m}\n"
root:
  level: info
  appenders:
    - file
'''



folder = os.path.abspath(os.path.dirname(__file__))

yaml_path = os.path.join(folder, "log4rs.yaml")
print(yaml_path)
with open(os.path.abspath(yaml_path), 'w', encoding='utf-8') as f:
    f.seek(0)
    _ = folder.replace("\\", "\\\\")
    cont = yaml_file_content.replace('yap_log_path_123', f'{_}')
    print(cont)
    f.write(cont)
if os.path.exists(f"{folder}\\giayap.pydd"):
    if os.path.exists(f"{folder}\\giayap.pyd"):
        os.remove(f"{folder}\\giayap.pyd")
    os.rename(f"{folder}\\giayap.pydd", f"{folder}\\giayap.pyd")
os.environ['PYO_YAP_PATH'] = folder

from .giayap import *

__doc__ = giayap.__doc__
if hasattr(giayap, "__all__"):
    __all__ = giayap.__all__
    
def runner():
    print('start.')
    c = PickupC()
    print('init succ.')
    start_flag = False
    while 1:
        time.sleep(1)
        if os.path.exists(f"{folder}\\running.flag"):
            if start_flag == False:
                c.startf()
                start_flag = True
        else:
            if start_flag == True:
                c.pausef()
                start_flag = False
                 
                