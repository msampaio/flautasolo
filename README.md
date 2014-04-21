## Instalation and Requirements

It's useful to add the following configuration in your ~/.ssh/config:

	Host genosmus.com
  		User genos

Create a virtualenv that uses Python 3:

	brew install python3
	mkvirtualenv -p /usr/local/bin/python3 flauta-solo-django

Install the requirements:

	pip install -r requirements.txt


On the Mac you may need to use the following command:

	ARCHFLAGS=-Wno-error=unused-command-line-argument-hard-error-in-future pip install


## Install Music21

Music21 doesn't work with Python 3, so we need a separate virtualenv for it.
It'll only be used to export the musical data to the database.

    mkvirtualenv music21
    git clone https://github.com/cuthbertLab/music21.git
    cd music21
    python setup.py install


## Deployment

To install the dependencies on Webfaction (we don't use virtualenv on Webfaction):

    pip3.3 install -r requirements.txt

To deploy:

	make deploy
