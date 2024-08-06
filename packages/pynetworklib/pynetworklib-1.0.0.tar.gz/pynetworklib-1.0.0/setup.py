from setuptools import find_packages, setup

setup(
    name = "pynetworklib",
    packages = find_packages(include=['config', 'network', 'optimization']),
    version = "1.0.0",
    description =  "A simple library for makeing dense multilayer neural networks",
    long_description = " This is an INDEV version of a multi-layer perception network written in Python. It is designed to be used as a library, it has a network module that provides trainable dense multilayer perceptron networks, a configuration module that provides a way to store parameters for training and optimization, and an optimization module that creates an optimized network structure and hyperparameters for a given dataset",
    long_description_content_type= "text/plain",
    author = "Joseph Bronsten",
    author_email= "josephbronsten.dev_contact@gmail.com",
    install_requires = ["numpy"],
    extras_requires = {"dev": ["pytest-8.3.2", "twine"]},
    setup_requires = ["numpy", "pytest-runner"],
    test_require = ["pytest-8.3.2"],
    test_suite = "tests"

)