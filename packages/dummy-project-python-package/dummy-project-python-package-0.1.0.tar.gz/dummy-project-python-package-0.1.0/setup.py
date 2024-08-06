from setuptools import setup, find_packages

def parse_requirements(filename):
    with open(filename, 'r') as f:
        return [line.strip() for line in f if line and not line.startswith('#')]

setup(
    name="dummy-project-python-package",
    version="0.1.0",
    author="Omar",
    author_email="omar@email.com",
    description="A simple dummy package for testing purposes",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url="https://github.com/Omarweb/dummy-python-package",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=parse_requirements('requirements.txt'),
)