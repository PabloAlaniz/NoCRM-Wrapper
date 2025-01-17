from setuptools import setup, find_packages

setup(
    name="nocrm-wrapper",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "flask>=2.3.3",
        "flask-cors>=4.0.0",
        "aiohttp>=3.8.5",
        "python-dotenv>=1.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "pytest-asyncio>=0.21.1",
            "black>=23.7.0",
            "isort>=5.12.0",
        ],
    },
    author="Pablo Alaniz",
    author_email="pablo@culturainteractiva.com",
    description="Un wrapper modular para la API de NoCRM",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/PabloAlaniz/nocrm-wrapper",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    python_requires=">=3.8",
)