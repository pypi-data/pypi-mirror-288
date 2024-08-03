# setup.py
from setuptools import setup, find_packages

setup(
    name='AcdDW',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[],
    author='Your Name',
    author_email='your.email@example.com',
    description='A simple example package',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/example_package',  # 你可以提供项目的GitHub URL
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
