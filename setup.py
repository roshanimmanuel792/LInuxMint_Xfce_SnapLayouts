"""Setup configuration for xfce-snap-layouts."""

from setuptools import setup, find_packages
from pathlib import Path

# Read README
readme_file = Path(__file__).parent / "README.md"
long_description = ""
if readme_file.exists():
    long_description = readme_file.read_text(encoding="utf-8")

setup(
    name="xfce-snap-layouts",
    version="1.0.0",
    author="XFCE Snap Layouts Contributors",
    description="Lightweight snap layout utility for Linux Mint XFCE",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/example/xfce-snap-layouts",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: X11",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Desktop Environment",
    ],
    python_requires=">=3.8",
    install_requires=[
        "PyGObject>=3.40.0",
    ],
    entry_points={
        "console_scripts": [
            "xfce-snap-layouts=xfce_snap_layouts.launcher:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
)
