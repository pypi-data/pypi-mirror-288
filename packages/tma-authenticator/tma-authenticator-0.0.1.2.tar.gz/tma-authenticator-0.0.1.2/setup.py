from setuptools import setup, find_packages

setup(
    name='tma-authenticator',
    version='0.0.1.2',
    description='Verifying telegram user token.',
    author='Ivan Kochelorov',
    packages=find_packages(include=['mypythonlib']),
    install_requires=['pydantic', 'hmac', 'urllib', 'fastapi', 'bson'],
)