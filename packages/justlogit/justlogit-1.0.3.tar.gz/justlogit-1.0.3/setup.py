from setuptools import setup

setup(name='justlogit',
    version='1.0.3',
    description='Simple logger for your python program',
    packages=['justlogit'],
    author_email='holinim@duck.com',
    install_requires=[
        'py-cpuinfo',
        'distro',
        'psutil'
    ],
    zip_safe=False)