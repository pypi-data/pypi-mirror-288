from setuptools import setup,find_namespace_packages, find_packages
import os
from setup_utils import SetupUtils


# Find base directory with reference to setup.py
HERE = SetupUtils.GetHere()
print(f"\033[33mHERE: {HERE}\033[0m")

# Read the version from the VERSION file
VERSION = SetupUtils.GetVersion()
print(f"\033[33mInstalling: {VERSION}\033[0m")

# Read the requirements from the requirements.txt file
DEFAULT_REQUIREMENTS_PATH=os.path.join(HERE,"requirements.txt")
DEFAULT_REQUIREMENTS = SetupUtils.ParseRequirements(DEFAULT_REQUIREMENTS_PATH)
DEFAULT_REQUIREMENTS = SetupUtils.MergeList(DEFAULT_REQUIREMENTS,[
    "pytest",
    "ipykernel",
    "pynvml",
    "nats-py"
])

setup(
    name='gai-lib',
    version=VERSION,
    author="kakkoii1337",
    author_email="kakkoii1337@gmail.com",
    package_dir={'': 'src'},
    #packages=find_namespace_packages(where='src', include=['gai.*']),
    packages=find_packages(where='src'),
    description = "Refer to https://gai-labs.github.io/gai for more information",
    long_description="Refer to https://gai-labs.github.io/gai for more information",
    long_description_content_type="text/markdown",
    classifiers=[
        'Programming Language :: Python :: 3.10',
        "Development Status :: 3 - Alpha",        
        'License :: OSI Approved :: MIT License',
        "Intended Audience :: Science/Research",
        "Intended Audience :: Developers",        
        'Operating System :: OS Independent',
        "Topic :: Software Development",
        "Topic :: Software Development :: Libraries :: Python Modules",        
        "Topic :: Scientific/Engineering :: Artificial Intelligence",        
    ],
    python_requires='>=3.10',
    install_requires=[
        DEFAULT_REQUIREMENTS
    ],
    package_data={
        "gai": [
            "gai.yml"
        ]
    },
    include_package_data=True
)