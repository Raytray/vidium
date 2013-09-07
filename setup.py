from setuptools import setup

setup(name='vidium',
      version='0.1',
      description='Store and organize video links.',
      author='Raymond Tang',
      author_email='raymond@tang.me',
      url='http://www.http://vidium-raytray.rhcloud.com/',
      install_requires=['Flask>=0.7.2', 'MarkupSafe', 'ipython', 'pymongo>=2.6.2', 'requests'],
      )
