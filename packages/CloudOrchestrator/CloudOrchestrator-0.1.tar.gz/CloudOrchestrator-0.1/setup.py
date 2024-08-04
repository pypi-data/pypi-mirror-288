from setuptools import setup, find_packages

setup(
    name="CloudOrchestrator",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "boto3",
        "paramiko",
    ],
    entry_points={
        'console_scripts': [
            'CloudOrchestrator = CloudOrchestrator.main:main',
        ],
    },
    author="Shweta Jha",
    author_email="jshweta208@gmail.com",
    description="A tool to manage AWS resources",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
