import PyInstaller.__main__
import os

current_dir = os.path.dirname(os.path.abspath(__file__))

resources = [
    os.path.join(current_dir, 'Screens', 'Assets', '*.png'),
    os.path.join(current_dir, 'Screens', 'Assets', '*.TTF'),
    os.path.join(current_dir, 'Screens', 'Assets', '*.gif'),
    os.path.join(current_dir, 'Screens', 'Assets', '*.ico'),
]

# Arguments for PyInstaller
PyInstaller.__main__.run([
    'main.py',                                     # Main script
    '--name=Parpadeatron',                         # exe name
    '--onefile',                                   # Only one exe file
    '--windowed',                                  # GUI app (without console)
    '--icon=Screens/Assets/icon_parpadeatron.ico', # exe icon
    '--add-data=Screens/Assets;Screens/Assets',    # visual resources 
    '--clean',                                     # Clean cache before build
    '--noconsole',                                #
])