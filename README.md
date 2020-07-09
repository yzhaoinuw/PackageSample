## Overview
This is a sample repo to show the structure my MFJ repo (renamed here as "PackageSample") and how to set up the package so that a user can install the package to their Python libraries. There are two concepts. The first is the repo, you can use git clone to download this repo to your local directory. The second is the actual Python package that will be installed to your Python libraries. Since I did not publish the MFJ package on PyPI, which is a store where you can download Python package from, you cannot pip install the MFJ package right away. You need to first clone the repo from GitHub to your computer, then install the package locally. The steps are:

1. It is recommended that you work in a virtual environment. You can use Anaconda to create an enviroment. If you don't have Anaconda, you can download it [here](https://docs.anaconda.com/anaconda/install/). Then follow the [instructions](https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html#creating-an-environment-with-commands) to create an enviroment. It is recommended that you specify the Python version to be 3.6 or later.

2. In terminal or command line, go to the directory to which you want to download the repo, for example, Desktop/. 
```shell
cd Desktop/
```

3. Clone the repo from GitHub to directory of your choice, for example, /Desktop.  This can be done by typing 
```shell
git clone git@github.com:yzhaoinuw/PackageSample.git
```

4. Go to this repo
```shell
cd PackageSample-master/
```
or the actual name of the repo folder appeared on your Desktop.

5. type 
```shell
pip install .
```
Now Python will run setup.py and install the MFJ package into your Python library.


### setup.py
Since setup.py is the file that governs the pip install process, let's look at what it does. First notice that in the repo there are three folders, "MFJ", "experiments", and "tests", along with several files. Only "MFJ" comprise the actual Python package that will be installed. Inside setup.py, you will notice a line which says "packages=find_packages()". This is telling Python to install, recursively, any folder that has an "__init__.py" file as a package. So, put an "__init__.py" file inside the folders which you want to be installed as packages. __init__.py can be blank. In our case, we only put an __init__.py in "MFJ" folder. But inside "MFJ" folder, we also want "shelter_detection" folder to be included in the pack, so another __init__.py is put inside "shelter_detection". There may be other ways to specify which folders to be installed as packages other than relying on __init__.py. For example you may be able to use the "include" parameter of find_packages. See the "setup.py" Section of this [documentation](https://packaging.python.org/guides/distributing-packages-using-setuptools/#setup-py) for more.

Next, notice that inside "MFJ" there is a folder called "model", where the neural network model for the name parser is stored. I want to include the model as data in the package, but not as a package, because the model only serves as data that the actual name parser package uses. Similarly, I also want the SQL databse inside shelter_detection/resources/ to be included as data to the package. The line "include_package_data=True" in setup.py can do just that, with the help of a separate file called "MANIFEST.in". setup.py will install the content specified inside MANIFEST.in as data to the package.

If your package is built on any third party Python packages, you will need to list the dependencies  of your package. So when a user wants to download your package, your package should first download its dependencies first for the user if they don't already have. This can be achieved by the line "install_requires=required" and a associated "requirements.txt" file.

### MANIFEST.in
MANIFEST.in allows you to pinpoint what to be included as data to the package. So in our case, we put 
```
recursive-include MFJ/model/ *.pt weights*
include MFJ/shelter_detection/resources/*.db
```
in MANEFEST.in. You can find more usage of MANIFEST.in in this [documentation](https://packaging.python.org/guides/using-manifest-in/).


### requirements.txt
List line by line what your dependent thrid party packages are and specify the version requirements. You don't need to include built-in libraries such as math. 



