from setuptools import setup, find_packages

setup(
    name='pyiwctl',
    version='0.3',
    author='ozkan',
    author_email='mozkan.91@gmail.com',
    description='A Python package to manage WiFi connections using iwctl',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/muratozk/pyiwctl',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    entry_points={
        'console_scripts': [
            'pyiwctl=pyiwctl.wifi_manager:main',
        ],
    },
)
