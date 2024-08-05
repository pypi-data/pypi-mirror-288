from setuptools import setup

setup(
    name='p1-notif',
    version='0.5',
    description='Notification SDK for Dekoruma\'s internal use',
    url='https://github.com/Dekoruma/p1-notif',
    author='Jauhar Arifin',
    author_email='jauhararifin10@gmail.com',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    license='MIT',
    packages=['notif', 'notif.channels'],
    install_requires=['future', 'requests'],
    zip_safe=False
)
