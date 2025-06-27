from setuptools import find_packages, setup

HYPHEN_E_DOT = '-e .'
def get_requirements(filepath: str):
    with open(filepath, 'r') as file_obj:
        requirements=file_obj.readlines()
        requirements=[req.replace("\n", "") for req in requirements]
        if HYPHEN_E_DOT in requirements:
            requirements.remove(HYPHEN_E_DOT)
        
    
    return requirements

setup(
    name="networksecurity",
    version="0.0.1",
    author="Mridul",
    author_email="mridulmahajan16@gmail.com",
    packages=find_packages(),
    install_requires=get_requirements("requirements.txt")
)
