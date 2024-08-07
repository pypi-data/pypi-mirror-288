from setuptools import setup, find_packages

setup(
    name='tma-authenticator',
    version='0.0.2',
    description='Verifying telegram user token.',
    author='Ivan Kochelorov',
    packages=find_packages(include=['tma_authenticator']),
    install_requires=['pydantic', 'fastapi', 'bson'],
)