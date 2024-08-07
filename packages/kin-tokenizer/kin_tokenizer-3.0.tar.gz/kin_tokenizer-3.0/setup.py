from setuptools import setup, find_packages


setup(
    name="kin_tokenizer",
    version= '3.0',
    packages=find_packages(),
    install_requires = []
)


setup(
    name='kin_tokenizer',
    version='3.0',
    author='Schadrack Niyibizi',
    author_email='niyibizischadrack@gmail.com',
    description='Kinyarwanda tokenizer for encoding and decoding Kinyarwanda language text',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/Nschadrack/Kin-Tokenizer',
    packages=find_packages(),
    keywords="Tokenizer, Kinyarwanda, KinGPT",
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    install_requires=[
        
    ],
)