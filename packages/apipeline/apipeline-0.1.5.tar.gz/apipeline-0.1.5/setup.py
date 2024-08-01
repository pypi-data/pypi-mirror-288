#!/usr/bin/env python
from setuptools import setup

setup(
    name="apipeline",
    description="Python pipeline with asyncio support",
    long_description=open("README.md").read().strip(),
    long_description_content_type="text/markdown",
    version="0.1.5",
    license="BSD 3-Clause",
    url="https://github.com/weedge/pipeline-py",
    author="weedge",
    author_email="weege007@gmail.com",
    python_requires=">=3.10",
    packages=["apipeline"],
    install_requires=["pydantic >= 2.8.2"],
    project_urls={
        "Changes": "https://github.com/weedge/pipeline-py/releases",
        "Code": "https://github.com/weedge/pipeline-py",
        "Issue tracker": "https://github.com/weedge/pipeline-py/issues",
    },
    keywords=["pipeline", "asyncio"],
)
