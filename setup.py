from setuptools import setup
import os.path
import warnings

try:
    from setuptools import setup, Command
    setuptools_available = True
except ImportError:
    from distutils.core import setup, Command
    setuptools_available = False


params = {}
# if setuptools_available:
#     params['entry_points'] = {'console_scripts': ['degflasher = deg_flasher:main']}
# else:
params['scripts'] = ['bin/degflasher', 'bin/amdmeminfo', 'bin/atiflash', 'deg_flasher/gpu-info', 'deg_flasher/vram']


setup(name='deg_flasher',
      version='0.1',
      description='A flasher utility for modding AMD cards',
      keywords='AMD Modded Radeon RX 470 480 570 580',
      url='https://github.com/gdak/deg_flasher',
      author='DEGConnect',
      author_email='info@degconnect.com',
      license='MIT',
      packages=["deg_flasher", ],
      install_requires=[
          'requests==2.18.1',
      ],
      zip_safe=False,
      **params)
