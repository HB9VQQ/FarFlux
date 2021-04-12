from cx_Freeze import setup, Executable

files = ['radio_tower.ico', 'radio_tower.png', 'geohash.json']
build_options = {'packages': [], 'excludes': [], 'include_files': files}

import sys
base = 'Win32GUI' if sys.platform=='win32' else None
base_c = 'Console'

executables = [
    Executable('main.py', base=base, target_name = 'FarFlux', icon='radio_tower.ico'),
    Executable('upload.py', base=base_c, target_name = 'FarFlux_upload')
]

import os
setup(name='FarFlux',
      version = '1.0',
      author = 'HB9VQQ',
      description = "Uploads valid points from Faros latest beacon log file to InfluxDB using settings set using the FarFlux.",
      options = {'build_exe': build_options,
                 'bdist_msi': {
                     'initial_target_dir': f'{os.getenv("SystemDrive")}\\Users\\{os.getlogin()}\\AppData\\Local\\Programs\\FarFlux\\',
                     'install_icon': 'radio_tower.ico'}},
      executables = executables)
