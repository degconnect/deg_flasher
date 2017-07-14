from setuptools import setup

setup(name='deg_flasher',
      version='0.1',
      description='A flasher utility for modding AMD cards',
      url='http://github.com/storborg/funniest',
      author='DEGConnect',
      author_email='info@degconnect.com',
      license='MIT',
      packages=['deg_flasher'],
      install_requires=[
          'requests==2.18.1',
      ],
      zip_safe=False)
