from distutils.core import setup

setup(
    name='EchoMatches',
    version='0.1dev',
    packages=['assets/stages', 'client', 'server', 'echo_common'],
    license='GNU GENERAL PUBLIC LICENSE',
    long_description=open('README.md').read(),
)