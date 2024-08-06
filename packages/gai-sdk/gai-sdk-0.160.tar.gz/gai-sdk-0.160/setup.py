from setuptools import setup,find_packages
import os
from setup_utils import SetupUtils

# Is this used for publishing?
is_publishing=os.environ.get("TWINE_USERNAME",False)

# Find base directory with reference to setup.py
def get_here():
    return os.path.dirname(os.path.abspath(__file__))
HERE = get_here()
print(f"\033[33mHERE: {HERE}\033[0m")

# Read the version from the VERSION file
def get_version():
    version_file = os.path.join(HERE, 'VERSION')
    with open(version_file, 'r') as f:
        return f.read().strip()
VERSION = get_version()
print(f"\033[33mInstalling: {VERSION}\033[0m")

# Read the requirements from the requirements.txt file
DEFAULT_REQUIREMENTS_PATH=os.path.join(HERE,"requirements.txt")
DEFAULT_REQUIREMENTS = SetupUtils.ParseRequirements(DEFAULT_REQUIREMENTS_PATH)

if not DEFAULT_REQUIREMENTS or len(DEFAULT_REQUIREMENTS)==0:
    raise Exception(f"No requirements found in {DEFAULT_REQUIREMENTS_PATH}")

# For development, debugging and testing on local machine
dev_requirements = SetupUtils.MergeList(DEFAULT_REQUIREMENTS,[
    "pytest",
    "ipykernel",
    "pynvml",
    "nats-py",
])

setup(
    name='gai-sdk',
    version=VERSION,
    author="kakkoii1337",
    author_email="kakkoii1337@gmail.com",
    package_dir={'': 'src'},
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
    entry_points={
        'console_scripts': [
            'gai=gai.cli.scripts.main:main',
        ],
    }
)