################################### Librairies ############################################

import os
from flask import Flask, flash, request, redirect, url_for, render_template
from flask.wrappers import Request
from sqlalchemy.sql.sqltypes import Integer, LargeBinary
from werkzeug.utils import secure_filename
from flask import send_from_directory
from sqlalchemy import create_engine, Column, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from flask_sqlalchemy import SQLAlchemy
import PdfToText
from flask import make_response,Response
import requests
import json 


################################ Path Directory And Configuration ##########################

basedir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'basededonneepdf.db')
UPLOAD_FOLDER = basedir #'C:/Users/Guilhem/Desktop/ProjetPython/'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

################################### Data Model ############################################

Base = declarative_base()

class Pdf(Base):
    __tablename__ ="pdftext"
    
    id = Column('id',Integer, primary_key=True)
    name = Column('name',String)
    data = Column('data',String)


    def __init__(self,name,data):
        self.name = name
        self.data=data

engine = create_engine(SQLALCHEMY_DATABASE_URI, echo =True) #"sqlite:///basededonneepdf.db", echo=True)
Base.metadata.create_all(bind=engine)
Session = sessionmaker(bind=engine)
session = Session()

############################## App method ##############################################

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/documents/<name>')
def download_file(name):
    return send_from_directory(app.config["UPLOAD_FOLDER"], name) #make_response()

#changer l'attribut name par pdf.id dans l'autre fct pour avoir l'id du fichier 

@app.route('/documents', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']        
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        
        pdf = Pdf(file.filename,PdfToText.extract_text_from_pdf(file.filename))
        session.add(pdf)
        session.commit()

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))         
            return redirect(url_for('download_file', name=filename))#,response=json.dumps(create_row_data)))
    return render_template('index.html')

@app.route('/text/<id>.txt')
def display_text(id):
    status = session.query(Pdf).filter( Pdf.id == id).one()
    return status.data

session.close()
if __name__ == "__main__":
    app.run(port=5001)
