import json
import os

from celery import Celery
from flask import Flask, Response, jsonify, render_template, request
from werkzeug.utils import secure_filename

from __init__ import app
from model.ExtractorFromPdf import Extractor
from model.ModelBdd import Session_creator
from model.NotificationModel import Notification
from model.PdfModel import Pdf

basedir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(basedir, "basededonneepdf.db")
ALLOWED_EXTENSIONS = {"txt", "pdf"}  # , 'png', 'jpg', 'jpeg', 'gif'}


app.config["UPLOAD_FOLDER"] = "."
app.secret_key = "super secret key"
app.config["SESSION_TYPE"] = "filesystem"

app.config["CELERY_BROKER_URL"] = "amqp://guest:guest@localhost/test"
app.config["CELERY_RESULT_BACKEND"] = "amqp://guest:guest@localhost/test"
celery = Celery(
    app.name,
    broker=app.config["CELERY_BROKER_URL"],
    backend=app.config["CELERY_RESULT_BACKEND"],
)


session = Session_creator()


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/documents", methods=["GET", "POST"])
def upload_file():
    if request.method == "POST":
        if "file" not in request.files:
            # return Notification("1", "No file part").Message()
            return Response(
                Notification("1", "No file part").Message(),
                status=400,
                mimetype="application/json",
            )
        else:
            file = request.files["file"]
            if file.filename == "":
                # return Notification("2", "No selected file").Message()
                return Response(
                    Notification("2", "No selected file").Message(),
                    status=400,
                    mimetype="application/json",
                )
            else:
                if file and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
                    task = InjestPdf.apply_async([file.filename])
                    # return jsonify({'task_id': task.id}), 202
                    return Response(
                        json.dumps({"task_id": task.id}),
                        status=202,
                        mimetype="application/json",
                    )
                else:
                    # return Notification("3", "File type not permitted").Message()
                    return Response(
                        Notification("3", "File type not permitted").Message(),
                        status=400,
                        mimetype="application/json",
                    )

    return render_template("index.html")


@celery.task(bind=True, name="PdfApi.InjestPdf")
def InjestPdf(self, file):
    PdfProcessed = Extractor(file)
    if getattr(PdfProcessed, "extracted") is True:
        pdf = Pdf(
            getattr(PdfProcessed, "pdf_path"),
            getattr(PdfProcessed, "text_from_pdf"),
            getattr(PdfProcessed, "title"),
            getattr(PdfProcessed, "creationDate"),
            getattr(PdfProcessed, "author"),
            getattr(PdfProcessed, "creator"),
            getattr(PdfProcessed, "producer"),
            getattr(PdfProcessed, "subject"),
            getattr(PdfProcessed, "keywords"),
            getattr(PdfProcessed, "number_of_pages"),
        )
        setattr(pdf, "id", self.request.id)
        session.add(pdf)
        session.commit()
        message = {"route": "file is being uploaded", "id": self.request.id}
    else:
        message = {"route": "file can't be parsed", "id": self.request.id}
    return json.dumps(message)


@app.route("/documents/<id>")
def taskstatus(id):
    task = InjestPdf.AsyncResult(id)
    if task.state == "PENDING":
        response = {"state": "pending"}
    elif task.state == "FAILURE":
        response = {
            "state": "completed",
        }
        response["result"] = task.info
    else:
        check = session.query(Pdf).filter(Pdf.id == id).scalar() is not None
        if check:
            status = session.query(Pdf).filter(Pdf.id == id).one()
            response = {
                "id": id,
                "state": task.state,
                "status": "SUCCESS",
                "uploaded_date": str(status.creationDate),
                "author": str(status.author),
                "creator": str(status.creator),
                "producer": str(status.producer),
                "subject": str(status.subject),
                "title": str(status.title),
                "number_of_pages": str(status.number_of_pages),
                "keywords": str(status.keywords),
            }
    return jsonify(response)


@app.route("/text/<id>.txt")
def display_text(id):
    try:
        status = session.query(Pdf).filter(Pdf.id == id).one()
        return status.data
    except Exception:
        return Response(
            Notification("4", "File id not in database").Message(),
            status=400,
            mimetype="application/json",
        )


@app.errorhandler(500)
def internal_server_error(error):
    print(error)
    return jsonify({"error": ":/"}), 500


session.close()


if __name__ == "__main__":
    app.run(port=5000)
