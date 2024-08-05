from setuptools import setup, find_packages

setup(
    name="sinopsis_ai",
    version="0.1.0", 
    author="Sinopsis Data, LLC", 
    author_email="info@sinopsisdata.com",
    description="A Python SDK for Sinopsis AI",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown", 
    url="https://github.com/daa192/sinopsis-ai-sdk", 
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        "boto3==1.24.28",
        "openai==1.12.0"
    ],
)