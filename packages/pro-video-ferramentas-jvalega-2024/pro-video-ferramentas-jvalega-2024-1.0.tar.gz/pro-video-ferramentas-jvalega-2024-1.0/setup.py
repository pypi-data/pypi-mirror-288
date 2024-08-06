from setuptools import setup,find_packages
from pathlib import Path

setup(

    name='pro-video-ferramentas-jvalega-2024',
    version=1.0,
    description='Pacote para fornecer ferramentas de processamento de vídeo',
    long_description=Path('README.md').read_text(),
    author='Jorge Valega',
    author_email='jorgevalega@gmail.com',
    keywords=['camera','video','processamento'],
    packages=find_packages()
)