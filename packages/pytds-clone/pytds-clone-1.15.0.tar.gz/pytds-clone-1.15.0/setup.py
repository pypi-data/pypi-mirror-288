import os
import setuptools
from setuptools import setup
import version

requirements = list(
    open(os.path.join(os.path.dirname(__file__), "requirements.txt"), "r").readlines()
)

print(setuptools.find_packages("src"))

setup(
    name="pytds-clone",
    version=version.get_git_version(),
    description="pytds-clone",
    author="G Reich",
    license="MIT",
    packages=["pytds"],
    package_dir={"": "src"},
    classifiers=[
        "Programming Language :: Python",
    ],
    zip_safe=True,
    install_requires=requirements,
)
