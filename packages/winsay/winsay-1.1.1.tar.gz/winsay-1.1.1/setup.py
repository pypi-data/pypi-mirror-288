import pathlib
from setuptools import find_packages, setup


# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

setup(
    name="winsay",
    version="1.1.1",
    packages=find_packages(),
    license="Private",
    description="say in windows",
    long_description=README,
    long_description_content_type="text/markdown",
    author="sukhbinder",
    author_email="sukh2010@yahoo.com",
    url = 'https://github.com/sukhbinder/winsay',
    keywords = ["say", "windows", "mac", "computer", "speak",],
    entry_points={
        'console_scripts': ['say = winsay.winsay:main', ],
    },
    install_requires=["pywin32"],
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    extras_require={
        "test": [
            "pytest",]
    },

)
