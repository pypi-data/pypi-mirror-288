from setuptools import setup, find_packages

setup(
    name='r4isy',
    version='0.0.1',
    packages=find_packages(),
    install_requires=[
        "loadwave",
        "importlib"
    ],
    entry_points={
        'console_scripts': [
            'connect=r4isy.connect:main',
        ],
    },
    author='r4isydev',
    author_email='info@r4isy.com',
    description='a lib',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
