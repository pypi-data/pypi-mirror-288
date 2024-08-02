import setuptools
from pathlib import Path


def get_install_requirements():
    """
    Extract packages from requirements.txt file to list

    Returns:
        list: list of packages
    """
    fname = Path(__file__).parent / 'requirements.txt'
    targets = []
    if fname.exists():
        with open(fname, 'r') as f:
            targets = f.read().splitlines()
    return targets

setuptools.setup(name='opsys-electrical-cabinet',
                 version='0.0.3',
                 description='python package for the electrical cabinet',
                 url='https://bitbucket.org/opsys_tech/opsys_electrical_cabinet/src/master/',
                 download_url='https://bitbucket.org/opsys_tech/opsys_electrical_cabinet/src/master/',
                 author='nerya.lifshitz',
                 install_requires=get_install_requirements(),
                 author_email='nerya.lifshitz@opsys-tech.com',
                 packages=setuptools.find_packages(exclude=("test",)),
                 zip_safe=False)