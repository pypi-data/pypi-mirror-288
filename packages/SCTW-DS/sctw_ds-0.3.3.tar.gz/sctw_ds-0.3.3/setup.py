from setuptools import find_namespace_packages, setup

setup(
    name="SCTW_DS",
    version="0.3.3",
    packages=find_namespace_packages(include=["SCTW_DS.*"]),
    include_package_data=True,
    install_requires=[],
    package_data={
        "SCTW_DS.NeuralNet": ["binaries/*.so"],
    },
    entry_points={
        "console_scripts": [
            # Example: 'my_script=my_package.module:main_func'
            # Add any CLI commands if you have any scripts to expose
        ],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    python_requires=">=3.8",
)
