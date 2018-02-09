from setuptools import setup, find_packages

setup(
    name="HelloWorld",
    version="0.1",
    packages=find_packages(),
    scripts=["app.py"],

    # Requirements
    install_requires=["flask", "requests"],

    # Data
    include_package_data=True,

    # PyPi metadata
    author="Giacomo Marciani",
    author_email="gmarciani@acm.org",
    description="The Smart Scaler microservice that implements a Redis simulator",
    license="MIT",
    keywords="kubernetes smart scaling elasticity artificial intelligence machine learning reinforcement learning ",
    url="https://github.com/gmarciani/smart-scaler.git",
    project_urls={
        "Bug Tracker": "https://github.com/gmarciani/smart-scaler/issues",
        "Documentation": "https://github.com/gmarciani/smart-scaler/wiki",
        "Source Code": "https://github.com/gmarciani/smart-scaler.git",
    }
)

