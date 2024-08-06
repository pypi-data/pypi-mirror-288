from setuptools import setup, find_packages

setup(
    name='bluetooth_linux_drivers',
    version='0.1',
    packages=find_packages(),
    py_modules=['bth_1208LS', 'mccBluetooth', 'test-bth1208LS'],
    entry_points={
        'console_scripts': [
            # Add any command-line scripts here
        ],
    },
    author='W. Jasper',
    description='Bluetooth drivers for Linux',
    url='https://github.com/wjasper/Linux_Drivers',
    author_email="wjasper@ncsu.edu",
)
