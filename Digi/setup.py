from setuptools import setup

APP = ['ads_checker.py']
DATA_FILES = []
OPTIONS = {
    'argv_emulation': True,
    'packages': ['tkinter', 'selenium'],
    'iconfile': 'app_icon.icns',  # Optional: specify a custom icon
}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
