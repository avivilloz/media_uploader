from setuptools import setup, find_packages

setup(
    name="media_uploader",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "google-api-python-client",
        "google-auth",
        "google-auth-oauthlib",
        "google-auth-httplib2",
    ],
    author="Aviv Illoz",
    author_email="avivilloz@gmail.com",
    description=(
        "Media Uploader is a Python package that simplifies the process of "
        "uploading various types of media to different online platforms."
    ),
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/avivilloz/media_uploader",
    python_requires=">=3.10",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
