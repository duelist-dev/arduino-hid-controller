from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

setup(
    name="arduino_hid_controller",
    version='{{VERSION_PLACEHOLDER}}',
    author="Duelist",
    author_email="duelist.dev@gmail.com",
    description="Python library to control Arduino as HID (Keyboard/Mouse) via Serial",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/duelist-dev/arduino-hid-controller",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        'pyserial>=3.5',
        'pynput>=1.7.6',
        'pyautogui>=0.9.53'
    ],
    extras_require={
        'dev': [
            'twine>=4.0.2',
            'wheel>=0.38.4'
        ]
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Home Automation",
        "Topic :: System :: Hardware"
    ],
    python_requires=">=3.7",
    project_urls={
        "Source": "https://github.com/duelist-dev/arduino-hid-controller"
    },
    keywords=[
        'arduino',
        'hid',
        'keyboard',
        'mouse',
        'automation',
        'serial'
    ],
    include_package_data=True,
)

