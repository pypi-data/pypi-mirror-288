from distutils.core import setup

setup(
  name='echo-env',         # How you named your package folder (MyLib)
  packages=['echo-env'],   # Chose the same as "name"
  version='0.1',
  description='A package for configuring projects with large environments',
  author='Roe Ploutno',                   # Type in your name
  author_email='roe.ploutno@gmail.com',      # Type in your E-Mail
  url='https://github.com/RoePl/echo-env',   # Provide either the link to your github or to your website
  download_url='https://github.com/RoePl/echo-env/archive/refs/tags/v0.1.tar.gz',    # I explain this later on
  keywords=['environment', 'configuration'],   # Keywords that define your package best
  install_requires=[],
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Programming Language :: Python :: 3.6',
  ],
)
