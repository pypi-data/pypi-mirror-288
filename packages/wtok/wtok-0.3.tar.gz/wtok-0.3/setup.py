from setuptools import setup
import os

VERSION = "0.3"


def get_long_description():
    with open(
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "README.md"),
        encoding="utf8",
    ) as fp:
        return fp.read()


setup(
    name="wtok",
    description="Count and truncate whisper text based on tokens",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    author="Vol Kyrylov thanks to Simon Willison",
    url="https://github.com/proger/wtok",
    project_urls={
        "Issues": "https://github.com/proger/wtok/issues",
        "CI": "https://github.com/proger/wtok/actions",
        "Changelog": "https://github.com/proger/wtok/releases",
    },
    license="Apache License, Version 2.0",
    version=VERSION,
    packages=["wtok"],
    entry_points="""
        [console_scripts]
        wtok=wtok.cli:cli
    """,
    install_requires=["click", "tiktoken", "openai-whisper"],
    python_requires=">=3.8",
)
