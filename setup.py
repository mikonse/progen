from setuptools import setup, find_packages


def readme():
    with open('README.md', 'r') as f:
        return f.read()


setup(
    name='progen',
    version='0.0.1',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Click',
        'Jinja2'
    ],
    package_data={
        # If any package contains *.txt or *.rst files, include them:
        '': ['*.txt', '*.rst'],
    },
    entry_points='''
        [console_scripts]
        progen=progen.scripts:cli
    ''',
    # metadata to display on PyPI
    author='Michael Loipfuehrer',
    author_email='',
    description='A simple python project bootstrapper',
    long_description=readme(),
    long_description_content_type='text/markdown',
    url='http://github.com/mikonse/progen',
    license='MIT',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)