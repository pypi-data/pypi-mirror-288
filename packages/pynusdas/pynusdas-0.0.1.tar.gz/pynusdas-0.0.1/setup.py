from setuptools import setup, find_packages


def get_version():
    from pathlib import Path

    init_path = Path(__file__).parent / "pynus/__init__.py"

    # Access the __version__ attribute
    return "0.0.1"


setup(
    name="pynusdas",
    version=get_version(),
    packages=find_packages(),
    install_requires=["numpy", "xarray", "scipy"],
)
