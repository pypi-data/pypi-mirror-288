from setuptools import find_packages, setup

with open("README.md", "r") as readme_file:
    long_description = readme_file.read()

exec(open("script/__init__.py").read())

setup(
    # The name with which the provided packages can be installed
    name='python_micro_script_template',
    version='0.0.2',
    # include_package_data=True,
    python_requires='>=3',
    description='Template for a small installable script',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Markus Peitl",
    author_email='office@markuspeitl.com',
    url="https://github.com/markuspeitl/python_micro_script_template",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "License :: OSI Approved :: MIT License",
        "Topic :: Software Development",
    ],
    # Depends on the following packages
    install_requires=[
        # 'pyperclip',
        # For publishing with the `publish.py` script
        'twine'
    ],
    # These scripts are useable in the system and call main.py's main function in the `script` module
    entry_points={
        'console_scripts': [
            # Main entry point -> function of the implemented script
            'my_console_script_name = script.main:main',

            # Package housekeeping scripts
            'py_build = package.build:main',
            'py_install_dev = package.install_dev:main',
            'py_install_git = package.install_git:main',
            'py_publish = package.publish:main',
        ]
    },
    # Packages within the module that can be imported (these are the actual import names)
    # Some packages use the same name for the `name` field as for the main modules directory which can be defined in `packages` or automatically found with `find_packages`
    # This has the advantage that the package can be installed and the main module imported with the same name to prevent confusion
    # packages=find_packages()
    packages=['package']
)
