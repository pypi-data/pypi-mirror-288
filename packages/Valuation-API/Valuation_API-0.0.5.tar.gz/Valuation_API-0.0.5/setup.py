import pathlib
from setuptools import find_packages, setup

HERE = pathlib.Path(__file__).parent

VERSION = '0.0.5' 
PACKAGE_NAME = 'Valuation_API' 
AUTHOR = 'Cristóbal Scheihing Orrego' 
AUTHOR_EMAIL = 'cristobal.scheihing@lvaindices.com' 
URL = '' 

LICENSE = 'MIT' 
DESCRIPTION = 'Library that allows you to connect to the LVA valuation API' 
LONG_DESCRIPTION = (HERE / "README.md").read_text(encoding='utf-8') 
LONG_DESC_TYPE = "text/markdown"


INSTALL_REQUIRES = [
      "requests >= 2.23.0"
      ]

setup(
    name=PACKAGE_NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type=LONG_DESC_TYPE,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    url=URL,
    install_requires=INSTALL_REQUIRES,
    license=LICENSE,
    packages=find_packages(),
    include_package_data=True
)