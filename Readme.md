# Extract text from pdf 

It's a simple REST API which parse pdf file in order to extract text from it 

***

## Features included 

 - Upload pdf and save its data into a database
 - Get the data from this uploading 
 - Get the data of files uploaded by id 

## Installation 

Create a virtualenv and activate it:

```shell
python3 -m venv venv
. venv/bin/activate
```
Install Packages 

```shell
pip install -r requirements.txt
```
## Run 

### With Windows

In production 

```shell
python3 main.py
```
In developement 

```shell
export FLASK_APP=pdfextractor
export FLASK_ENV=development
flask run
```


