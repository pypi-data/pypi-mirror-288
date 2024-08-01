from setuptools import setup

setup(
    name='p1-notif',
    version='0.2',
    description='Notification SDK for Dekoruma\'s internal use',
    url='https://github.com/Dekoruma/p1-notif',
    author='Jauhar Arifin',
    author_email='jauhararifin10@gmail.com',
    license='MIT',
    packages=['notif', 'notif.channels'],
    install_requires=['future', 'requests'],
    zip_safe=False
)
