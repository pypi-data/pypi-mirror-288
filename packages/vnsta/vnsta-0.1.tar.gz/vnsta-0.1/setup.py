from setuptools import setup, find_packages

setup(
    name='vnsta',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'requests',
        'telebot',
        'beautifulsoup4',
        'instabot'
    ],
    author='Vermouth',
    author_email='ver7mouth4@gmail.com',
    description='A simple tool for Instagram control, web scraping, and user Instagram interaction using requests.',
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/Vermouth4/Vnsta',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
