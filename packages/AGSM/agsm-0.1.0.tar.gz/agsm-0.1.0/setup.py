from setuptools import setup, find_packages

setup(
    name='AGSM',
    version='0.1.0',
    author='Ayato',
    author_email='ayato.yofukashi@gmail.com',
    description='???',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/YFKS/AGSM',
    packages=['AGSM'],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.0',
)