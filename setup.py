from setuptools import setup


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
      scripts=['bin/degflasher', 'bin/amdmeminfo', 'bin/atiflash', 'bin/gpu-info', 'bin/vram'])
