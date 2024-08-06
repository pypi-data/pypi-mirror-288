from setuptools import setup, find_packages
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name='voice_a',
    version='0.7.0',
    description='A module for hotword detection and speech-to-text functionality.',
    packages=find_packages(),
    long_description=long_description,
    long_description_content_type='text/markdown',
    py_modules=['voice'],
    install_requires=[
        'playsound==1.3.0',
        'pvporcupine==1.9.5',
        'PyAudio==0.2.14',
        'pygame==2.6.0',
        'requests==2.32.3',
        'selenium==4.23.1',
        'virtual_aide==0.6'
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
    ],
)
