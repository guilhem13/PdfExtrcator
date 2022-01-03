import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


basedir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'basededonneepdf.db?check_same_thread=False')  # ajout de false pour gestion problem des thread
UPLOAD_FOLDER = basedir
Base = declarative_base()


def Session_creator():      
    engine = create_engine(SQLALCHEMY_DATABASE_URI, echo=True)  # "sqlite:///basededonneepdf.db", echo=True)
    Base.metadata.create_all(bind=engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    return session
