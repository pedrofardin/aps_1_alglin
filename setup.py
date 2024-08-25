from setuptools import setup, find_packages

setup(
    name='angry_birds_game',
    version='1.0.0',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'pygame',
        # Adicione outros pacotes necessários aqui
    ],
    entry_points={
        'console_scripts': [
            'angry-birds=angry_birds.main:main',
        ],
    },
    package_data={
        'angry_birds': ['images/*.png'],
    },
    author='Seu Nome',
    author_email='seu.email@example.com',
    description='Um jogo inspirado no Angry Birds',
    url='https://github.com/pedrofardin/repositorio',  # Substitua pelo URL do seu repositório
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
)
