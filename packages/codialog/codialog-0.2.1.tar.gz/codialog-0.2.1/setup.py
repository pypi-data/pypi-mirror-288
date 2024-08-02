from setuptools import setup, find_packages, find_namespace_packages

# Read the requirements.txt file
with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(
    name='codialog',
    version='0.2.1',
    #packages=find_packages(),
    packages=find_namespace_packages(where="."),
    package_dir={"": "."},
    package_data={"codialog": ["*.txt", "*.html", "static/*", "templates/*"]},
    include_package_data=True,
    install_requires=required,
    entry_points='''
        [console_scripts]
        codialog=codialog.app:run
    ''',
)