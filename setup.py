from cx_Freeze import setup, Executable

build_options = {'packages': [], 'excludes': []}

import sys
base = 'Win32GUI' if sys.platform=='win32' else None

executables = [
    Executable('main.py', base=base, target_name = 'FarFlux', icon='radio_tower.ico'),
    Executable('upload.py', base=base, target_name = 'FarFlux_upload')
]

setup(name='FarFlux',
      version = '1.0',
      description = "Uploads the valid points (evidence > 1) from the latest beacon log file generated 1 by Afreet's Faros application to an InfluxDB using the configuration settings set using the FarFlux application.",
      options = {'build_exe': build_options, 
                 'summary_data': {'author': 'HB9VQQ'}},
      executables = executables)

# Default install directory: C:\Users\{os.getlogin()}\AppData\Local\Programs\FarFlux\
# Application resources saved in same directory: [geohash.json, config.json, radio_tower.ico/png]
# When FarFlux is uninstalled only application resources remain on system