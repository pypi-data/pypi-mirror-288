import setuptools

setuptools.setup(
    name="zs-server",
    version="0.1.0.6",
    author="Prajwal",
    author_email="pkumarjha@zscaler.com",
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=["websockets", "asyncio"],
    packages=setuptools.find_packages(),
    python_requires=">=3.8",
    entry_points={
        "console_scripts": [
            "zs-server = zs_server.server:main",
        ]
    }
)