# Installation

## Via Setup.py

To install it, make sure you have Python 3.6 or greater installed. 
Then run this command from the command prompt:

* pip3 install -r requirements.txt --user
* python3 setup.py install --user


## As pip package

If you want to generate a pip package instead, run the following command from
the command prompt:

* python3 setup.py sdist

You can then install the library via pip using:

* pip3 install dist/car-1.0.0.tar.gz --user
