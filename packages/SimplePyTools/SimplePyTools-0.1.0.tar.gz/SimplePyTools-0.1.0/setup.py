from setuptools import setup, find_packages

setup(
    name='SimplePyTools',
    version='0.1.0',
    author='Krishna Mandanapu',
    author_email='kmandanapu@simplehuman.com',
    description='A utility library for Python.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/simplehuman-engineering/sw-SimplePyTools',
    packages=find_packages(),
    install_requires=[
        'setuptools==68.0.0'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.7',
)