################################### Librairies ############################################

import os
import sys 
lib_path = os.path.abspath('./')
sys.path.append(lib_path)

from flask import Flask, flash, request, redirect, render_template
from werkzeug.utils import secure_filename
from model.ExtractorFromPdf import Extractor
from model.ModelBdd import Session_creator
from model.PdfModel import Pdf
from model.NotificationModel import Notification
import json

################################ Path Directory And Configuration ##########################

basedir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'basededonneepdf.db')
UPLOAD_FOLDER = basedir #'C:/Users/Guilhem/Desktop/ProjetPython/'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
app = Flask(__name__)
path = os.getcwd()
UPLOAD_FOLDER = os.getcwd()
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = 'super secret key'
app.config['SESSION_TYPE'] = 'filesystem'
#
#app.config.from_object("config")

################################### Data Model ############################################

session = Session_creator()
############################## App method ##############################################

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/documents', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            #flash("No file part")
            #return redirect(request.url)
            return Notification("1","No file part").Message()
        else: 
            file = request.files['file']        
            if file.filename == '':                
                #flash("No selected file")
                return Notification("2","No selected file").Message()
            else:                 

                if file and allowed_file(file.filename):

                    PdfProcessed = Extractor(file.filename)           
                    pdf = Pdf(getattr(PdfProcessed,'pdf_path'),getattr(PdfProcessed,'text_from_pdf'),getattr(PdfProcessed,'title'),getattr(PdfProcessed,'creationDate'),getattr(PdfProcessed,'author'),getattr(PdfProcessed,'creator'),getattr(PdfProcessed,'producer'),getattr(PdfProcessed,'subject'),getattr(PdfProcessed,'keywords'),getattr(PdfProcessed,'number_of_pages'))
                    session.add(pdf)
                    session.commit()
                    filename = secure_filename(file.filename)
                    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename)) 
                    #flash("File upload with Id "+str(pdf.id))
                    #return redirect(request.url)       
                    return json.dumps({"message":"File uploaded","id_uploaded":str(pdf.id)})
                else: 
                    #flash("File type not permitted")
                    #return redirect(request.url)
                    return Notification("3","File type not permitted").Message()
       
    return render_template('index.html')

@app.route('/documents/<id>.txt')
def display_metadat(id):
    check = session.query(Pdf).filter( Pdf.id == id).scalar() is not None
    if check: 
        status = session.query(Pdf).filter( Pdf.id == id).one()
        result = {
            "id":id,
            "status":"SUCCESS",
            "uploaded_date" : str(status.creationDate),
            "author" : str(status.author),
            "creator" : str(status.creator),
            "producer" : str(status.producer),
            "subject"  : str(status.subject),
            "title" : str(status.title),
            "number_of_pages" : str(status.number_of_pages),
            "keywords" : str(status.keywords),    
            }
        json_data = json.dumps(result)
        return json_data
    else:
        result = {
            "id":id,
            "status":"Not Found",
            "uploaded_date" : None,
            "author" : None,
            "creator" : None,
            "producer" : None,
            "subject"  : None,
            "title" : None,
            "number_of_pages" : None,
            "keywords" : None,    
            }
        json_data = json.dumps(result)
        return json_data
     


@app.route('/text/<id>.txt')
def display_text(id):
    status = session.query(Pdf).filter( Pdf.id == id).one()
    return status.data

session.close()
if __name__ == "__main__":
    
    #sess.init_app(app)

    app.run(port=5001)
