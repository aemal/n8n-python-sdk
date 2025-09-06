from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="n8n-python-sdk",
    version="0.1.0",
    author="n8n Python SDK Contributors",
    author_email="",
    description="A Python SDK for creating and managing n8n workflows programmatically",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/your-username/n8n-python-sdk",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=[
        "typing-extensions>=4.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=22.0.0",
            "isort>=5.0.0",
            "mypy>=1.0.0",
        ],
        "http": [
            "requests>=2.28.0",
        ],
        "sheets": [
            "google-auth>=2.0.0",
            "google-auth-oauthlib>=1.0.0",
            "google-auth-httplib2>=0.1.0",
            "google-api-python-client>=2.0.0",
        ],
    },
)