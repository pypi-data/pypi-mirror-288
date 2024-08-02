from setuptools import setup, find_packages

setup(
    name='logscribe',
    version='0.1',  
    packages=find_packages(),  
    install_requires=[
        'loguru',
        'matplotlib'
    ], 
    entry_points={
        'console_scripts': [
           
        ],
    },
    author='Bohdan Terskow',
    author_email='bohdanterskow@gmail.com',
    description='Tool for logging and visualization of logs.',
    long_description=open('README.md').read(), 
    long_description_content_type='text/markdown',
    url='https://github.com/gods-created/online-watcher',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6', 
)
