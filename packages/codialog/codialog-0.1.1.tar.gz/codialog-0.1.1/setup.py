from setuptools import setup, find_packages

setup(
    name='codialog',
    version='0.1.1',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'flask',
    ],
    entry_points='''
        [console_scripts]
        codialog=flask.app:run
    ''',
)