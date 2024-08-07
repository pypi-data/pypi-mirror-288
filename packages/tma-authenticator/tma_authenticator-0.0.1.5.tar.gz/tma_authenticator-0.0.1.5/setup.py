from setuptools import setup, find_packages

setup(
    name='tma_authenticator',
    version='0.0.1.5',
    description='Verifying telegram user token.',
    author='Ivan Kochelorov',
    packages=find_packages(include=['mypythonlib']),
    install_requires=['pydantic', 'fastapi', 'bson'],
)