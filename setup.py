import setuptools

with open("README.md", "r") as fh:
  long_description = fh.read()

setuptools.setup(
  name="optimizely_manager",
  version="1.1.0",
  author="Asa Schachar",
  author_email="asa@optimizely.com",
  description="A manager which performs simple datafile management",
  long_description=long_description,
  long_description_content_type="text/markdown",
  url="https://github.com/asaschachar/optimizely-manager-python",
  packages=setuptools.find_packages(),
  install_requires=['optimizely-sdk', 'requests', 'six'],
  classifiers=[
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
  ],
)
