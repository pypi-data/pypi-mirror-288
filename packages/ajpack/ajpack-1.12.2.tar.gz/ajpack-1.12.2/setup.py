import json
from setuptools import setup, find_packages # type:ignore
from pathlib import Path

with open("data.json", "r", encoding="utf-8") as f: version: str = json.load(f)["version"]

this_directory = Path(__file__).parent
long_description: str = (this_directory / "README.md").read_text()

setup(
    author="AJ-Holzer",
    description="A simple module which does some simple stuff. Don't make something illegal ;)",
    long_description=long_description,
    url="https://github.com/AJ-Holzer/AJ-Module",
    license="MIT",
    name='ajpack',
    version=version,
    packages=find_packages(),
    install_requires=[
        "pyzipper",
        "opencv-python",
        "requests",
        "Pillow",
        "keyboard",
        "pywin32",
        "psutil",
        "winshell",
        "plyer",
        "customtkinter",
        "cryptography",
        "pycryptodome",
        "pygame",
        
    ],
    entry_points={
        'console_scripts': [
            # Commands
        ],
    },
)