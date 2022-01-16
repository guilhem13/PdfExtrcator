import io
from datetime import datetime

import chardet
from pdfminer.converter import TextConverter
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfinterp import PDFPageInterpreter, PDFResourceManager, resolve1
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfparser import PDFParser


class Extractor:
    pdf_path = None

    text_from_pdf = None
    creationdate = None
    author = None
    creator = None
    keywords = None
    producer = None
    subject = None
    title = None
    number_of_pages = None
    extracted = False

    def __init__(self, path):
        self.pdf_path = path
        self.extracted = False
        resource_manager = PDFResourceManager()
        fake_file_handle = io.StringIO()
        converter = TextConverter(resource_manager, fake_file_handle)
        page_interpreter = PDFPageInterpreter(resource_manager, converter)
        with open(self.pdf_path, "rb") as file:
            try:
                parser = PDFParser(file)
                doc = PDFDocument(parser)
                # Title
                if "Title" in doc.info[0]:
                    encoding_title = (
                        chardet.detect(doc.info[0]["Title"])["encoding"]
                        if str(doc.info[0]["Title"]) != "b''"
                        else 0
                    )
                    self.title = (
                        doc.info[0]["Title"].decode(encoding_title)
                        if encoding_title != 0
                        else None
                    )
                else:
                    self.title = None
                # Encoding
                if "creationdate" in doc.info[0]:
                    encoding_creation_date = (
                        chardet.detect(doc.info[0]["creationdate"])["encoding"]
                        if str(doc.info[0]["creationdate"]) != "b''"
                        else 0
                    )
                    if encoding_creation_date != 0:
                        temp = doc.info[0]["creationdate"].decode(encoding_creation_date)
                        date = datetime.strptime(
                            temp.replace("'", ""), "D:%Y%m%d%H%M%S%z"
                        )
                        self.creationdate = date.strftime("%d-%b-%Y (%H:%M:%S.%f)")
                else:
                    self.creationdate = None
                # Author
                if "Author" in doc.info[0]:
                    encoding_auhtor = (
                        chardet.detect(doc.info[0]["Author"])["encoding"]
                        if str(doc.info[0]["Author"]) != "b''"
                        else 0
                    )
                    self.author = (
                        doc.info[0]["Author"].decode(encoding_auhtor)
                        if encoding_auhtor != 0
                        else None
                    )
                else:
                    self.author = None
                # Creator
                if "Creator" in doc.info[0]:
                    encoding_creator = (
                        chardet.detect(doc.info[0]["Creator"])["encoding"]
                        if str(doc.info[0]["Creator"]) != "b''"
                        else 0
                    )
                    self.creator = (
                        doc.info[0]["Creator"].decode(encoding_creator)
                        if encoding_creator != 0
                        else None
                    )
                else:
                    self.creator: None
                # keywords
                if "Keywords" in doc.info[0]:
                    encoding_keywords = (
                        chardet.detect(doc.info[0]["Keywords"])["encoding"]
                        if str(doc.info[0]["Keywords"]) != "b''"
                        else 0
                    )
                    self.keywords = (
                        doc.info[0]["Keywords"].decode(encoding_keywords)
                        if encoding_keywords != 0
                        else None
                    )
                else:
                    self.keywords = None
                # producer
                if "Producer" in doc.info[0]:
                    encoding_producer = (
                        chardet.detect(doc.info[0]["Producer"])["encoding"]
                        if str(doc.info[0]["Producer"]) != "b''"
                        else 0
                    )
                    self.producer = (
                        doc.info[0]["Producer"].decode(encoding_producer)
                        if encoding_producer != 0
                        else None
                    )
                else:
                    self.producer = None
                # Subject
                if "Subject" in doc.info[0]:
                    encoding_subject = (
                        chardet.detect(doc.info[0]["Subject"])["encoding"]
                        if str(doc.info[0]["Subject"]) != "b''"
                        else 0
                    )
                    self.subject = (
                        doc.info[0]["Subject"].decode(encoding_subject)
                        if encoding_subject != 0
                        else None
                    )
                else:
                    self.subject = None
                self.number_of_pages = resolve1(doc.catalog["Pages"])["Count"]
                for page in PDFPage.get_pages(file, caching=True, check_extractable=True):
                    page_interpreter.process_page(page)

                text = fake_file_handle.getvalue()
                self.text_from_pdf = text
                file.close()
                self.extracted = True
            except:
                pass
        converter.close()
        fake_file_handle.close()
