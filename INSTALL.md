# Installation
This file gives installation instructions for the local environment setup. We're going to be using Jupyter with Python 3.10 for the modeling.

## Download and install Anaconda3 

Visit https://www.anaconda.com/download/ to download. 

## Create a Python 3.10 virtual environment

From the terminal,

```
conda create -n [env_name] python=3.10
```

## Activate your environment

From the terminal
```
conda activate [env_name]
```

## Install various dependencies

Confirm you are in [env_name] environment and have the requirements.txt file in this folder, then:
```
python3 -m pip install -r requirements310.txt
```

## Install the kernel for your jupyter notebook
In some circumstances, your kernel and installed packages may not match what you expect in jupyter lab. To solve this, we install a kernel from within the [env_name] env (make sure you have typed `conda activate [env_name]` first...)
```
python -m ipykernel install --user --name=[env_name]
```
If you have issues with install paths or other versioning, then make sure you select from within Jupyter `Kernel->[env_name]`. Once that kernel starts, you will get the installed package versions as needed.
