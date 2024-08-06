from setuptools import setup, find_packages

setup(
    name='contextforce_sdk',
    version='0.1',
    description='A Python SDK for My API',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Your Name',
    author_email='your.email@example.com',
    license='MIT',
    packages=find_packages(),
    install_requires=[
        'requests'
    ],
    python_requires='>=3.6',
)