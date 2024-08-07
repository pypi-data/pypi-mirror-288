from setuptools import setup, find_packages

setup(
    name='gendiff_dmitriev',
    version='0.1.0',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'gendiff=gendiff.scripts.gendiff:main',
        ],
    },
    install_requires=[
        'PyYAML>=6.0.1',
        'pytest>=8.3.2'        
    ],
    include_package_data=True,
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.10',
)
