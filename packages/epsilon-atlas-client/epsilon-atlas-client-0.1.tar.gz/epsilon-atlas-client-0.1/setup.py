from setuptools import setup, find_packages

setup(
    name='epsilon-atlas-client',
    version='0.1',
    packages=find_packages(include=['atlas_client', 'atlas_client.*']),
    install_requires=[
        'pandas',
        'requests',
        'python-dotenv',
    ],
    entry_points={
        'console_scripts': [
            'run-example=atlas_client.example:main',
        ],
    },
    include_package_data=True,
    package_data={
        '': ['*.csv', '*.env'],
    },
    author='Khajiev Nizomjon',
    author_email='nizom7812@example.com',
    description='A package for reading data from CSV or XLS files and publishing to Apache Atlas.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/Epsilon-Data/py-packages',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
