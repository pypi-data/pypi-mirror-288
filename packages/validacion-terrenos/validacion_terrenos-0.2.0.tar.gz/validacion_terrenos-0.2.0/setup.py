from setuptools import setup, find_packages

setup(
    name='validacion_terrenos',
    version='0.2.0',
    packages=find_packages(),
    install_requires=[
    ],
    entry_points={
        'console_scripts': [
            'validacion_terrenos=validacion_terrenos.validacion_terrenos:main',
        ],
    },
    author='Daniel Vanegas',
    author_email='tu_email@example.com',
    description='Validacion atributos terrenos',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/tu_usuario/validacion_terrenos',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)