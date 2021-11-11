from model import ModelBdd
from sqlalchemy import Column, Integer, String

class Pdf(ModelBdd.Base):
    __tablename__ ="pdftext"    
    id = Column('id',Integer, primary_key=True)
    name = Column('name',String)
    data = Column('data',String)
    ##
    creationDate = Column("date", String(255))
    author = Column("author", String(255))
    title = Column("title", String(255))
    creator = Column("creator", String(255))
    producer = Column("producer", String(255))
    subject = Column("subject", String(255))
    keywords = Column("title", String(255))
    number_of_pages = Column("number_of_pages", Integer)


    def __init__(self,name,data,title,creationDate,author,creator,producer,subject,keywords,number_of_pages):
        self.name = name
        self.data = data
        self.title = title
        self.creationDate = creationDate
        self.author = author
        self.creator = creator
        self.producer = producer
        self.subject = subject
        self.keywords = keywords
        self.number_of_pages = number_of_pages
    