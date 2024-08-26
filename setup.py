from setuptools import setup, find_packages

setup(
    name='angry_birds_game',
    version='1.0.0',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'pygame',
    ],
    entry_points={
        'console_scripts': [
            'angry-birds=angry_birds.main:main',
        ],
    },
    package_data={
        'angry_birds': ['*.png'],
    },
    author='Pedro Ricardo Fardin',
    author_email='pedrorf1@al.insper.edu.br',
    description='Um jogo inspirado no Angry Birds',
    url='https://github.com/pedrofardin/aps_1_alglin',  # Substitua pelo URL do seu repositório
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
)