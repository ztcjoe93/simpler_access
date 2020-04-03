import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="simple-raccess-ztcjoe",
    version="0.0.5",
    author="ZT Chua",
    author_email="ztcjoe93@gmail.com",
    description="Simple client for remote access using SSH/VNC",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ztcjoe93/sshgui",
    packages=setuptools.find_packages(),
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    python_requires=">=3.6",
)
