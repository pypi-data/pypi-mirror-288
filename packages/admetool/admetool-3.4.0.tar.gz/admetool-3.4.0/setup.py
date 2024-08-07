from setuptools import setup, find_packages
import pathlib

setup(name='admetool',
    version='3.4.0',

    license='MIT License',
    author='Júlio César Xavier',
    long_description=pathlib.Path("README.md").read_text(),
    long_description_content_type="text/markdown",
    author_email='jcaxavier2@gmail.com',
    keywords='admetlab',
    description=u'Tool that uses Pharmit data to perform an ADMET analysis',
    packages= find_packages(),
    include_package_data=True,
    package_data={
        'weights': ['*.json'],},
    entry_points={
        'console_scripts': [
            'admetscore = admetool.app:main',
        ],
    },
    install_requires=["pandas==2.2.2","rdkit==2023.9.6","numpy==1.26.4","XlsxWriter==3.2.0","openpyxl==3.1.5"],
    scripts=['admetool/app.py'])