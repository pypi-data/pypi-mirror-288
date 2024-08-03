from setuptools import setup

with open('README.md') as f:
    long_description = f.read()

setup(
  name = 'TestFlyte',         # How you named your package folder (TSIClient)
  packages = ['TestFlyte'],   # Chose the same as "name"
  version = '1.0.2',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  long_description=long_description,
  long_description_content_type='text/markdown',  # This is important!
  author = 'Vaibhav ',                   # Type in your name
  author_email = 'vaibhav.baraskar@ielektron.com',      # Type in your E-Mail
  url = 'https://gitlab.com/flyte2/flyte-pipeline.git',   # Provide either the link to your github or to your website
  #download_url = 'https://github.com/RaaLabs/TSIClient/archive/v_0.7.tar.gz',    # If you create releases through Github, then this is important
  keywords = ['Time Series Insight', 'TSI', 'TSI SDK'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
         "flytekit>=0.16.0",
         "pandas",
         "numpy",
         "pytest",
	 "flake8",
         "black"
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ],
)
