try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

with open('README') as file:
    long_description = file.read()

packages = [
    'utrunner'
]

setup(name='utrunner',
      version='0.0.2',
      url='https://github.com/kevwo/utrunner',
      zip_safe=False,
      packages=packages,
      package_dir={'utrunner': 'utrunner'},
      description='Simple test runner that wraps unittest and Coverage',
      author='Kevin Woodmansee',
      author_email='kevinwoodmansee@gmail.com',
      license='MIT',
      long_description=long_description,
      install_requires=['coverage>=4.0']
)
