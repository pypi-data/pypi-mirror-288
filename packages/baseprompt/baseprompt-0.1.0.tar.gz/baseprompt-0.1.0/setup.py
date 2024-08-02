from setuptools import find_packages, setup


setup(
    name='baseprompt',
    packages=find_packages(include=['baseprompt']),
    version='0.1.0',
    description='Baseprompt - Collaboration tool and secure storage for LLM chain prompts.',
    author='Arsen Kylyshbek',
    author_email="arsen@baseprompt.dev",
    install_requires=[],
    setup_requires=['pytest-runner'],
    test_suite='tests',
    python_requires='>=3.7',
)