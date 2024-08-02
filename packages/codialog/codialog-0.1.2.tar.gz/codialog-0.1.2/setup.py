from setuptools import setup, find_packages, find_namespace_packages

setup(
    name='codialog',
    version='0.1.2',
    #packages=find_packages(where="."),
    packages=find_namespace_packages(where="."),
    package_dir={"": "."},
    package_data={"codialog": ["*.txt", "*.html", "static/*", "templates/*"]},
    include_package_data=True,
    install_requires=[
        'flask',
    ],
    entry_points='''
        [console_scripts]
        codialog=codialog.app:run
    ''',
)