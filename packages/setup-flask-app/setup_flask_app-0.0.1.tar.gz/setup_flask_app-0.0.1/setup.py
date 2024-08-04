from setuptools import setup, find_packages

VERSION = '0.0.1'
DESCRIPTION = 'A CLI to setup a flask app with just one command'
LONG_DESCRIPTION = 'This is a CLI tool which setup a flask app with just one command. This is to ease devs. They just have to write setup-flask-app and every thing require to stat adding value to their app will be setup automatically.'

# Setting up
setup(
    name="setup-flask-app",
    version=VERSION,
    author="Saqib Tanveer",
    author_email="<elven5055@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'setup-flask-app=setup_flask_app.cli:app',  # Command to run your CLI
        ],
    },
    keywords=['python', 'flask', 'setup-flask-app', 'auto setup'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)