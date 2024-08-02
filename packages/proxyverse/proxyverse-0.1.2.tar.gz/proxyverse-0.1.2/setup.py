from setuptools import setup, find_packages

setup(
    name="proxyverse",
    version="0.1.2",
    description="A Python package for interacting with the Proxyverse API",
    author="alexkorolex",
    author_email="alexkorolex@bk.ru",
    packages=find_packages(),  # Automatically finds packages in your project
    install_requires=[
        "httpx>=0.27.0",
    ],
    url="https://github.com/alexkorolex/ProxyVerse-Python",
    download_url="https://github.com/alexkorolex/ProxyVerse-Python/archive/refs/heads/master.zip",
    python_requires=">=3.11",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    license="MIT",  # Corrected license type
    # If you have additional files or data to include in your package, specify them here
    # include_package_data=True,
    # package_data={
    #     "": ["*.md", "*.txt"],
    # },
)
