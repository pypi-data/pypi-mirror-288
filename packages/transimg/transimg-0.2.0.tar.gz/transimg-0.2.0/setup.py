from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="transimg",
    version="0.2.0",
    author="Avinion",
    author_email="shizofrin@gmail.com",
    description="A script to convert images to different formats using FFmpeg",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://x.com/Lanaev0li",
    py_modules=['transimg'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    entry_points={
        'console_scripts': [
            'transimg=transimg:main',
        ],
    },
)
