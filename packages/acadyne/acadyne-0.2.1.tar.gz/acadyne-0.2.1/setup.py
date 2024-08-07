from setuptools import setup, find_packages

# Leer el archivo README para usarlo como descripción larga
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='acadyne',
    version='0.2.1',
    description='Una biblioteca para el modelado simbólico y simulación de sistemas dinámicos complejos.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Jose Fabian Soltero Escobar',
    author_email='acadyne@gmail.com',
    url='https://github.com/acadyne/acapulco_dynamic/', 
    packages=find_packages(include=['acadyne', 'acadyne.*']),
    install_requires=[
        'numpy',
        'sympy',
        'scipy'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering :: Mathematics',
    ],
    python_requires='>=3.7',
    extras_require={
        'dev': [
            'pytest',
            'flake8',
            'twine',
        ],
    },

)
