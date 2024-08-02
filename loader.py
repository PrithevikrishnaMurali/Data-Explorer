import pandas as pd
import json
import xml.etree.ElementTree as ET
from PyPDF2 import PdfReader
from io import StringIO

class DataLoader:
    def __init__(self, logger, subject):
        self.logger = logger
        self.subject = subject

    def load(self, file):
        raise NotImplementedError

class CSVLoader(DataLoader):
    def load(self, file):
        try:
            data = pd.read_csv(file)
            self.logger.info(f"CSV file loaded: {file.name}")
            self.subject.notify("info", f"CSV file loaded: {file.name}")
            return data
        except Exception as e:
            self.logger.error(f"Error loading CSV file: {str(e)}")
            self.subject.notify("error", f"Error loading CSV file: {str(e)}")
            return None

class JSONLoader(DataLoader):
    def load(self, file):
        try:
            data = pd.read_json(file)
            self.logger.info(f"JSON file loaded: {file.name}")
            self.subject.notify("info", f"JSON file loaded: {file.name}")
            return data
        except Exception as e:
            self.logger.error(f"Error loading JSON file: {str(e)}")
            self.subject.notify("error", f"Error loading JSON file: {str(e)}")
            return None

class HTMLLoader(DataLoader):
    def load(self, file):
        try:
            data = pd.read_html(file, encoding='utf-8')
            self.logger.info(f"HTML file loaded: {file.name}")
            self.subject.notify("info", f"HTML file loaded: {file.name}")
            return data[0] if data else None
        except Exception as e:
            self.logger.error(f"Error loading HTML file: {str(e)}")
            self.subject.notify("error", f"Error loading HTML file: {str(e)}")
            return None

class XMLLoaderAdapter(DataLoader):
    def load(self, file):
        try:
            tree = ET.parse(file)
            root = tree.getroot()
            data = []
            for child in root:
                data.append({elem.tag: elem.text for elem in child})
            data = pd.DataFrame(data)
            self.logger.info(f"XML file loaded: {file.name}")
            self.subject.notify("info", f"XML file loaded: {file.name}")
            return data
        except Exception as e:
            self.logger.error(f"Error loading XML file: {str(e)}")
            self.subject.notify("error", f"Error loading XML file: {str(e)}")
            return None

class PDFLoaderAdapter(DataLoader):
    def load(self, file):
        try:
            reader = PdfReader(file)
            text = ''
            for page in reader.pages:
                text += page.extract_text()
            self.logger.info(f"PDF file loaded: {file.name}")
            self.subject.notify("info", f"PDF file loaded: {file.name}")
            return text
        except Exception as e:
            self.logger.error(f"Error loading PDF file: {str(e)}")
            self.subject.notify("error", f"Error loading PDF file: {str(e)}")
            return None

class DataLoaderFactory:
    def __init__(self, logger, subject):
        self.logger = logger
        self.subject = subject

    def create_loader(self, file_type):
        if file_type == "csv":
            return CSVLoader(self.logger, self.subject)
        elif file_type == "json":
            return JSONLoader(self.logger, self.subject)
        elif file_type == "html":
            return HTMLLoader(self.logger, self.subject)
        elif file_type == "xml":
            return XMLLoaderAdapter(self.logger, self.subject)
        else:
            self.logger.error(f"Unsupported file type: {file_type}")
            self.subject.notify("error", f"Unsupported file type: {file_type}")
            return None
