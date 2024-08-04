import os

# from .__version__ import __version__

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
loggers:
  yap:
    level: error
    appenders:
      - collect_info
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
os.environ['RUST_PATH'] = folder

from .yap import *

__doc__ = yap.__doc__
if hasattr(yap, "__all__"):
    __all__ = yap.__all__