from setuptools import setup, find_packages

setup(
 name='ascii_flix',
    version='0.21',
    packages=find_packages(include=['modules','modules.*']),
    py_modules=['main'],
    install_requires=[
        'pygame',
        'moviepy',
        'opencv-python',
        'rich',
        'numpy'
    ],
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