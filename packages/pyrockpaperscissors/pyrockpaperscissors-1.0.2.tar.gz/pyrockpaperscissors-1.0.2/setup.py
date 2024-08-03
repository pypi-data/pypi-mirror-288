from setuptools import setup

with open("README.md", "r") as file:
    long_description = file.read()

setup(
    name="pyrockpaperscissors",
    version="1.0.2",
    description="A simple Rock Paper Scissors Game written in Python🐍",
    long_description=long_description,
    long_description_content_type="text/markdown",
    entry_points={
        "console_scripts": [
            "rps = pyrps.rps:main"
        ]
    }
)