from setuptools import setup, find_packages

setup(
    name='tma-authenticator',
    version='0.0.1.7',
    description='Verifying telegram user token.',
    author='Ivan Kochelorov',
    packages=find_packages(),
    install_requires=['pydantic', 'fastapi', 'bson'],
)