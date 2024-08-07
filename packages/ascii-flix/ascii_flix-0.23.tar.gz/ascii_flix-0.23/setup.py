from setuptools import setup, find_packages
import platform

is_windows = platform.system() == 'Windows'

setup(
 name='ascii_flix',
    version='0.23',
    packages=find_packages(include=['modules','modules.*','utils','utils.*']),
    py_modules=['main'],
    install_requires=[
        'pygame',
        'moviepy',
        'opencv-python',
        'rich',
        'numpy'
    ]+ (['windows-curses'] if is_windows else []),
    python_requires='>=3.6',
    author='Saad Ahmed Siddiqui',  
    entry_points={
        'console_scripts': [
            'ascii-flix=main:main_function',  
        ],
    },
    description='A terminal-based video player that converts videos to ASCII art.',
    long_description=open('README.md').read()
)