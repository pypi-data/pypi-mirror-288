from setuptools import setup,find_packages
from pathlib import Path

VERSION = '0.0.5'
DESCRIPTION = 'A module to access data from the Mauro Borges Statistic and Socioeconomic Institute (IMB), Goias - Brazil'
KEYWORDS = ['statistics','data','IMB','Mauro Borges','Brazil']

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()
setup(
      name='pybdedata',
      version=VERSION,
      description=DESCRIPTION,
      long_description=long_description,
      long_description_content_type='text/markdown',
      url='https://github.com/boliveirageo/pybdedata',
      author='Bernard Silva de Oliveira',
      author_email="bernard.oliveira@goias.gov.br",
      keywords=KEYWORDS,
      license='MIT License',
      packages=find_packages(),
      zip_safe=False,
      install_requires=['requests'],
)