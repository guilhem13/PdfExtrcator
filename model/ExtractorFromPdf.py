import io
from pdfminer.converter import TextConverter
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfinterp import resolve1
import chardet

class Extractor():
    pdf_path = None

    text_from_pdf = None
    creationDate = None
    author = None
    creator = None
    keywords = None
    producer = None
    subject = None
    title = None
    number_of_pages = None

    def __init__(self,Path):
        self.pdf_path = Path 
        resource_manager = PDFResourceManager()
        fake_file_handle = io.StringIO()
        converter = TextConverter(resource_manager, fake_file_handle)
        page_interpreter = PDFPageInterpreter(resource_manager, converter)        
        with open(self.pdf_path, 'rb') as fh:
            parser = PDFParser(fh)
            doc = PDFDocument(parser)
            #TODO
            # Gérer l'encoding des bytes formart date D:20210713024315Z exemple sur le fichier 23

            #Title
            encodingTitle = chardet.detect(doc.info[0]['Title'])['encoding'] if str(doc.info[0]['Title']) != "b''" else 0               
            self.title = doc.info[0]['Title'].decode(encodingTitle) if 'Title' in doc.info[0] and encodingTitle !=0  else None
            #Encoding
            encodingcreationDate = chardet.detect(doc.info[0]['CreationDate'])['encoding'] if str(doc.info[0]['CreationDate']) != "b''" else 0
            self.creationDate = doc.info[0]['CreationDate'].decode(encodingcreationDate) if 'CreationDate' in doc.info[0] and encodingcreationDate !=0 else None
            #Author
            encodingAuhtor = chardet.detect(doc.info[0]['Author'])['encoding'] if str(doc.info[0]['Author']) != "b''" else 0  
            self.author = doc.info[0]['Author'].decode(encodingAuhtor) if 'Author' in doc.info[0] and encodingAuhtor !=0 else None
            #Creator
            encodingCreator  = chardet.detect(doc.info[0]['Creator'])['encoding'] if str(doc.info[0]['Creator']) != "b''" else 0  
            self.creator = doc.info[0]['Creator'].decode(encodingCreator) if 'Creator' in doc.info[0] and encodingCreator != 0 else None
            #keywords
            encodingKeywords  = chardet.detect(doc.info[0]['Keywords'])['encoding'] if str(doc.info[0]['Keywords']) != "b''" else 0 
            self.keywords = doc.info[0]['Keywords'].decode(encodingKeywords) if 'Keywords' in doc.info[0] and encodingKeywords != 0 else None
            #producer
            encodingProducer  = chardet.detect(doc.info[0]['Producer'])['encoding'] if str(doc.info[0]['Producer']) != "b''" else 0 
            self.producer = doc.info[0]['Producer'].decode(encodingProducer) if 'Producer' in doc.info[0] and encodingProducer !=0 else None
            #Subject
            encodingSubject  = chardet.detect(doc.info[0]['Subject'])['encoding'] if str(doc.info[0]['Subject']) != "b''" else 0
            self.subject = doc.info[0]['Subject'].decode(encodingSubject) if 'Subject' in doc.info[0] and encodingSubject != 0 else None

            self.number_of_pages = resolve1(doc.catalog['Pages'])['Count'] 
            for page in PDFPage.get_pages(fh,caching=True,check_extractable=True):
                page_interpreter.process_page(page)
                
            text = fake_file_handle.getvalue()
            self.text_from_pdf = text 
        converter.close()
        fake_file_handle.close()

#P1 = PdfToText("test.pdf")
#P1.extract_text_from_pdf()
#print(getattr(P1,'number_of_pages'))   

    