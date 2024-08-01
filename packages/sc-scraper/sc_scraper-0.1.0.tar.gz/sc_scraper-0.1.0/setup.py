from setuptools import setup, find_packages

setup(
    name='sc_scraper',
    version='0.1.0',
    author='maximizzar',
    author_email='mail@maximizzar.de',
    description='Scraper for Soundcloud',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/maximizzar/sc_scraper',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: GNU Affero General Public License v3',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
