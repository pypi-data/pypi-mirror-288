from setuptools import setup, find_packages

setup(
    name='bitoli',
    version='0.1.1',
    author='retrotee',
    author_email='',
    description='Adaptive compression and encryption of data',
    long_description=open('README.rst').read(),
    long_description_content_type='text/x-rst',
    url='https://github.com/retrotee/bitoli',
    packages=find_packages(),
    install_requires=[
        'cryptography>=3.4.7'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
