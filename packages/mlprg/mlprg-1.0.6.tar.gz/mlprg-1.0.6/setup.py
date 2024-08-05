from setuptools import setup, find_packages

setup(
    name='mlprg',
    version='1.0.6',
    packages=find_packages(),
    include_package_data=True,
    package_data={
        '': ['mlprg.py', 'prgs.txt','prgsl.txt'],
    },
    description='A package for nothing',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='petteer1',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
