from setuptools import find_packages, setup


setup(
    name="networkip_project",
    version="0.0.1",
    description="A ip viewer to reset show and release your computer ip adress",
    package_dir={"": "app"},
    package=find_packages(where="app"),
    url="https://github.com/lamalice20/Tuto-ytb",
    author="lamalice20",
    author_email="discord974a@gmail.com",
    license="MIT",
    install_requires=["bson >= 0.5.10"],
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.12",
        "Development Status :: 4 - Beta",
    ],
    extras_require={
        "dev" : ["vidstream", "pyscreeze", "pillow"],
    },
    python_requires=">=3.12.4"
)