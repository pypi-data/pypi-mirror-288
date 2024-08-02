from setuptools import setup, find_packages
setup(
    name='adaptive-cards-io',
    version='1.0.1',
    author='Melquisedeque Brito de Lima',
    author_email='melquibrito07@gmail.com',
    description='Framework for building adaptive cards programatically',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.7',
)