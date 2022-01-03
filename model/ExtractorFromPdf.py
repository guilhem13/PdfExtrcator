import io
from pdfminer.converter import TextConverter
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfinterp import resolve1
from datetime import datetime
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
    extracted = False

    def __init__(self, Path):
        self.pdf_path = Path
        self.extracted = False
        resource_manager = PDFResourceManager()
        fake_file_handle = io.StringIO()
        converter = TextConverter(resource_manager, fake_file_handle)
        page_interpreter = PDFPageInterpreter(resource_manager, converter)
        with open(self.pdf_path, 'rb') as fh:
            try:
                parser = PDFParser(fh)
                doc = PDFDocument(parser)
                # Title
                if 'Title' in doc.info[0]:
                    encodingTitle = chardet.detect(doc.info[0]['Title'])['encoding'] if str(doc.info[0]['Title']) != "b''" else 0
                    self.title = doc.info[0]['Title'].decode(encodingTitle) if encodingTitle != 0 else None
                else:
                    self.title = None
                # Encoding
                if 'CreationDate' in doc.info[0]:
                    encodingcreationDate = chardet.detect(doc.info[0]['CreationDate'])['encoding'] if str(doc.info[0]['CreationDate']) != "b''" else 0
                    if encodingcreationDate != 0:
                        temp = doc.info[0]['CreationDate'].decode(encodingcreationDate)
                        date = datetime.strptime(temp.replace("'", ""), "D:%Y%m%d%H%M%S%z")
                        self.creationDate = date.strftime("%d-%b-%Y (%H:%M:%S.%f)")
                else:
                    self.creationDate = None
                # Author
                if 'Author' in doc.info[0]:
                    encodingAuhtor = chardet.detect(doc.info[0]['Author'])['encoding'] if str(doc.info[0]['Author']) != "b''" else 0
                    self.author = doc.info[0]['Author'].decode(encodingAuhtor) if encodingAuhtor != 0 else None
                else:
                    self.author = None
                # Creator
                if 'Creator' in doc.info[0]:
                    encodingCreator = chardet.detect(doc.info[0]['Creator'])['encoding'] if str(doc.info[0]['Creator']) != "b''" else 0
                    self.creator = doc.info[0]['Creator'].decode(encodingCreator) if encodingCreator != 0 else None
                else:
                    self.creator: None
                # keywords
                if 'Keywords' in doc.info[0]:
                    encodingKeywords = chardet.detect(doc.info[0]['Keywords'])['encoding'] if str(doc.info[0]['Keywords']) != "b''" else 0
                    self.keywords = doc.info[0]['Keywords'].decode(encodingKeywords) if encodingKeywords != 0 else None
                else:
                    self.keywords = None
                # producer
                if 'Producer' in doc.info[0]:
                    encodingProducer = chardet.detect(doc.info[0]['Producer'])['encoding'] if str(doc.info[0]['Producer']) != "b''" else 0
                    self.producer = doc.info[0]['Producer'].decode(encodingProducer) if encodingProducer != 0 else None
                else:
                    self.producer = None
                # Subject
                if 'Subject' in doc.info[0]:
                    encodingSubject = chardet.detect(doc.info[0]['Subject'])['encoding'] if str(doc.info[0]['Subject']) != "b''" else 0
                    self.subject = doc.info[0]['Subject'].decode(encodingSubject) if encodingSubject != 0 else None
                else:
                    self.subject = None
                self.number_of_pages = resolve1(doc.catalog['Pages'])['Count']
                for page in PDFPage.get_pages(fh, caching=True, check_extractable=True):
                    page_interpreter.process_page(page)

                text = fake_file_handle.getvalue()
                self.text_from_pdf = text
                fh.close()
                self.extracted = True
            except:
                pass
        converter.close()
        fake_file_handle.close()
        