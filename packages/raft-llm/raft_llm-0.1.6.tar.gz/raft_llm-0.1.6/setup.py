from setuptools import setup, find_namespace_packages

# Read the contents of your README file
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Read the contents of your requirements.txt file
with open("requirements.txt", "r", encoding="utf-8") as f:
    requirements = f.read().splitlines()

setup(
    name="raft_llm",
    version="0.1.6",
    author="Tianjun Zhang",
    author_email="tianjunz@eecs.berkeley.edu",
    description="A brief description of your package",
    include_package_data=True,  # include non-Python files in your package distribution. This can include things like configuration files, templates, static assets, etc.
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/tianjunz/raft_llm",
    packages=find_namespace_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.9",
    entry_points={
        "console_scripts": [
            "raft=raft.cli:main",
        ],
    },
    install_requires=requirements,
    license="MIT",
    package_data={
        "raft": ["config/*.yaml"],
    },
)
