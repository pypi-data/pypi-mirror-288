from setuptools import setup,find_namespace_packages
import os
from setup_utils import SetupUtils

# Find base directory with reference to setup.py
HERE = SetupUtils.GetHere()
print(f"\033[33mHERE: {HERE}\033[0m")

# Read the version from the VERSION file
VERSION = SetupUtils.GetVersion()
print(f"\033[33mInstalling: {VERSION}\033[0m")

# Get DEFAULT REQUIREMENTS
DEFAULT_REQUIREMENTS_PATH = os.path.join(HERE, 'src/gai/ttt/client/requirements.txt')
DEFAULT_REQUIREMENTS = SetupUtils.ParseRequirements(DEFAULT_REQUIREMENTS_PATH)
DEFAULT_REQUIREMENTS = SetupUtils.MergeList(DEFAULT_REQUIREMENTS,[
    "pytest",
    "ipykernel",
    "pynvml",
    "nats-py"
])


# For Server Installation Only
svr_requirements = SetupUtils.MergeList(DEFAULT_REQUIREMENTS,SetupUtils.ParseRequirements("./src/gai/ttt/server/requirements.txt"))

# The wheel file is included for convenience sake for use with local install from source code.
# But this direct dependency cannot be published to pypi.
# In order to enable publishing, set the environment variable TWINE_USERNAME to "__token__" and the extras_require will be set to empty.
is_publishing=os.environ.get("TWINE_USERNAME",False)
if is_publishing:
    svr_requirements = []
else:
    svr_requirements.append(SetupUtils.GetWheelFile("exllamav2","exllamav2-0.1.4-cp310-cp310-linux_x86_64.whl"))

setup(
    name='gai-ttt',
    version=VERSION,
    author="kakkoii1337",
    author_email="kakkoii1337@gmail.com",
    package_dir={'': 'src'},
    packages=find_namespace_packages(where='src', include=['gai.*']),
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
    extras_require={
        "all": SetupUtils.MergeList(DEFAULT_REQUIREMENTS,svr_requirements),
        "svr": svr_requirements
    },
)