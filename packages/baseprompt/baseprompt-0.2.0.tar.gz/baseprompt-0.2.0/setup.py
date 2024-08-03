from setuptools import find_packages, setup


setup(
    name='baseprompt',
    packages=find_packages(include=['baseprompt']),
    version='0.2.0',
    description='Baseprompt - No-code platform to build safe & fast AI applications',
    author='Arsen Kylyshbek',
    author_email="arsen@baseprompt.dev",
    install_requires=[],
    setup_requires=['pytest-runner'],
    test_suite='tests',
    python_requires='>=3.7',
)