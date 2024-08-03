from setuptools import setup, find_packages

setup(
    name='sql_sanity_checks',
    version='0.2.0',
    author='Jose Santos',
    author_email='josemrsantos@gmail.com',
    description='A Python Library to help perform tests on SQL engines to assess the quality of the data',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/josemrsantos/sql_sanity_checks',
    packages=find_packages(),
    data_files=[('demo_db', ['demo/Chinook.db'])],
    install_requires=[
      # No requirements for now
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    keywords='SQL test data quality',
    python_requires='>=3.6',
    license='MIT',
    project_urls={
        'Bug Tracker': 'https://github.com/josemrsantos/sql_sanity_checks/issues',
        'Documentation': 'https://github.com/josemrsantos/sql_sanity_checks/blob/main/README.md',
        'Source Code': 'https://github.com/josemrsantos/sql_sanity_checks',
    },
)
