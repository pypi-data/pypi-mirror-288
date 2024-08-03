from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()

# Get the long description from the README file
long_description = (here / 'README.md').read_text(encoding='utf-8')

setup(
    name='DarkMiner',
    version='1.0.0',
    description='Uses computer down time to do useful operations',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/Luke-Larsen/DarkMiner',
    author='Luke Larsen',
    author_email='luke@lukehanslarsen.com',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    keywords='',
    packages=find_packages(where='darkminer'),
    python_requires='>=3.8, <4',
    install_requires=['easygui', 'requests'],
    extras_require={
        'dev': ['check-manifest'],
        'test': ['coverage'],
    },
    package_data={
        'darkminer': ['sheepitClient.jar'],
    },
    entry_points={
        'console_scripts': [
            'darkminer=darkminer.main:main',
        ],
    },
    project_urls={
        'Bug Reports': 'https://github.com/Luke-Larsen/DarkMiner/issues',
        'Funding': 'https://lukehanslarsen.com/donate',
        'Source': 'https://github.com/Luke-Larsen/DarkMiner',
    },
)
