from setuptools import setup, find_packages

setup(
    name='febedatasets',
    version='1.1',
    packages=['febedatasetswits', 'lab01'],
    include_package_data=True,
    install_requires=[
        'pandas', 'Pillow', 'otter-grader'
    ],
    package_data={
        '': ['data/*.csv', 'images/*.png', 'tests/*.py'],
    },
    author='Isaiah Chiraira',
    author_email='itchiraira@gmail.com',
    description='A package to load different datasets as dataframes',
    url='https://github.com/Tech-Gui/febe1004Datasets',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    license='MIT',  
)
