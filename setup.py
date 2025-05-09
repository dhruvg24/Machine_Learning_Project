from setuptools import find_packages, setup
from typing import List


HYPHEN_E_DOT = '-e .'


def get_requirements(file_path:str)->List[str]:
    '''
    This function will return the list of requirements, also the -e . present in requirements.txt will automatically trigger this file -> setup.py
    '''

    requirements = []
    with open(file_path) as file_obj:
        requirements= file_obj.readlines()
        requirements=[req.strip() for req in requirements if req.strip()]

        if HYPHEN_E_DOT in requirements:
            requirements.remove(HYPHEN_E_DOT)

    return requirements

setup(
    name = 'MACHINE_LEARNING_PROJECT',
    version = '0.0.1',
    author= 'dhruvg24', 
    author_email='dhruvgarg24112002@gmail.com', 
    packages = find_packages(),
    install_requires = get_requirements("requirements.txt")
)

# whenever setup.py runs it shall look for __init__.py which is present in src folder.