from setuptools import setup, find_packages

setup(
    name="hand_dim",
    version="0.1.0",
    packages=find_packages(),
    description="A package to calculate hand dimensions based on head length",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="YDeepesh Gora",
    author_email="deepeshgorai13@gmail.com",
    url="https://github.com/yourusername/hand_dim",  # Update with your actual GitHub repo
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)