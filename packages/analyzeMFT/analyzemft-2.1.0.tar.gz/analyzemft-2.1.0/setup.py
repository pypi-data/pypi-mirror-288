from setuptools import setup, find_packages

setup(
    name='analyzeMFT',
    version='2.1.0',
    author='Benjamin Cance',
    author_email='canceb@gmail.com',
    packages=find_packages(),
    url='http://github.com/rowingdude/analyzeMFT',
    license='LICENSE.txt',
    description='Analyze the $MFT from a NTFS filesystem.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    scripts=['analyzeMFT.py'],
    install_requires=[
       # Maybe add some later as this expands.
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)