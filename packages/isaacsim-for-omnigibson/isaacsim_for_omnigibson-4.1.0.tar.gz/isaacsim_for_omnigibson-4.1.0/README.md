# IsaacSim for OmniGibson

This package provides IsaacSim dependencies for OmniGibson, ensuring compatibility with Linux x86_64 Ubuntu 20.04 (GLIBC 2.31) and Python 3.10.

## Description

IsaacSim for OmniGibson is a package that installs the necessary IsaacSim components required to run OmniGibson simulations. It simplifies the process of setting up the IsaacSim environment by automatically downloading and installing the required packages from NVIDIA's PyPI repository.

## Building and Uploading to PyPI

To build and upload this package to PyPI, follow these steps:

1. Ensure you have the necessary tools installed:
    ```pip install setuptools wheel twine```

2. Clone the repository or navigate to the project directory containing `setup.py`: 
    ```git clone https://github.com/StanfordVL/isaac-sim-for-omnigibson```

3. Create the distribution files: ```python setup.py sdist```

4. Upload to PyPI using twine (tar.gz only): ```twine upload dist/*.tar.gz```

    Note: You'll need to have a PyPI account and be logged in to upload the package.

5. If you want to test the upload process first, use TestPyPI: ```twine upload --repository testpypi dist/*.tar.gz```

## Important Notes for Maintainers

- Update the version number in `setup.py` each time you upload a new version of the package.
- Ensure that the `long_description` in `setup.py` accurately reflects any changes or updates to the package.
- If you make changes to the `CustomInstallCommand` class or add new dependencies, make sure to test the installation process thoroughly on both Linux and Windows systems.
- Keep the list of `ISAAC_SIM_PACKAGES` up to date with the latest versions from NVIDIA.

## Installation for Users

Once the package is uploaded to PyPI, users can install it using: ```pip install isaacsim-for-omnigibson```

## More Information

For more information on installing Isaac Sim using pip, please visit the [official Isaac Sim documentation](https://docs.omniverse.nvidia.com/isaacsim/latest/installation/install_python.html).

## License

Please refer to the license information provided by NVIDIA for IsaacSim components.

## Support

For issues related to OmniGibson, please visit the [OmniGibson GitHub repository](https://github.com/StanfordVL/OmniGibson).

For IsaacSim-specific issues, please refer to the NVIDIA IsaacSim support channels.