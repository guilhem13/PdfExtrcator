# Extract text from pdf 

It's a simple REST API which parse pdf file in order to extract text from it 

***

### Features included 

 - Feature 1 : Upload pdf and save its data into a database
 - Feature 2 : Get the data from this uploading 
 - Feature 3 : Get the data of files uploaded by id 

***
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
***
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

***
## Usage

#### Feature 1

###### On browser

Open http://localhost:5000/documents in a browser to upload your pdf 
![GitHub Logo](/images/localhost_5000_documents.PNG)

###### On Command 







