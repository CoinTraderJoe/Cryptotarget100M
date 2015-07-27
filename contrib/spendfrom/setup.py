from distutils.core import setup
setup(name='crt100mspendfrom',
      version='1.0',
      description='Command-line utility for cryptotarget100M "coin control"',
      author='Gavin Andresen',
      author_email='gavin@cryptotarget100Mfoundation.org',
      requires=['jsonrpc'],
      scripts=['spendfrom.py'],
      )
