import io
from pdfminer.converter import TextConverter
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfinterp import resolve1

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
            self.title = doc.info[0]['Title'].decode("utf-8")
            self.creationDate = doc.info[0]['CreationDate'].decode("utf-8")
            self.author = doc.info[0]['Author'].decode("utf-8")
            self.creator = doc.info[0]['Creator'].decode("utf-8")
            self.keywords = doc.info[0]['Keywords'].decode("utf-8")
            self.producer = doc.info[0]['Producer'].decode("utf-8")
            self.subject = doc.info[0]['Subject'].decode("utf-8")
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

    