from setuptools import setup, find_packages

setup(
    name='mesa2_preprocessing',
    version='0.4.0',
    author='Nadir Nadirov',
    author_email='nadirnadirov1999@gmail.com',
    description='A tool for pre-processing MESA2.0 measurement data',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    packages=find_packages(),
    install_requires=[
        'pandas>=1.0',
        'numpy>=1.18',
        'nptdms>=0.25',
        'pyarrow>=4.0',
        'fastparquet>=0.6'
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Topic :: Scientific/Engineering :: Visualization'
    ],
    python_requires='>=3.8',
)
