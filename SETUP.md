# Getting setup

We will be using Anaconda to install and manage a Python 'environment' for us to work in. Rather than using any pre-installed Python 
interpretors this has the advantage that it will not conflict with any existing libraries, and everyone will be using the same verisons.

For the course it will be easiest to work directly on your laptop - so please install these packages there. Python is cross-platform though so switching to work on remote servers later is straight forward.

## 1. Install Anaconda

If you haven't already got Anaconda installed, download and install it from: https://www.continuum.io/downloads. Choose Python 3.5 as this 
is the latest version of Python.

## 2. Create a new environment for the workshop

Now you have installed Anaconda we can create an evironment to work in. Open your terminal (or 'Anaconda Prompt' on Windows) and type:

    conda create -c conda-forge -n python_workshop cis jupyter pytest

Where we have created an environment called `python_workshop`, and installed a packaged called `cis` (and all its dependencies) and a package called `jupyter` from the `conda-forge` channel.

This may take a while as it installs all of the Python libraries and C libraries on which they depend, including NetCDF and HDF.

## 3. Download sample data

Many of our examples use realistic sample data, but unfortunately different packages use different datasets. To get the Iris sample data, 
simply type:

    conda install -c scitools -n python_workshop iris_sample_data

The CIS example data can be downloaded from Dropbox using this link: https://www.dropbox.com/s/6iqb6h84h6kwxk0/WorkshopData2016.zip?dl=0

Both datasets will be needed for the second day of the course.

## 4. Install PyCharm

For the third and final day of the course we will be using an Integrated Development Environment (IDE) called PyCharm. This is a powerful
Python development tool which has a free version available for Educational and Academic use. Download and install it from here: 
https://www.jetbrains.com/pycharm/download/.
