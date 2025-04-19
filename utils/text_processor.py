import os
from pathlib import Path
from PyPDF2 import PdfReader
from langchain.docstore.document import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TextProcessor:
    def __init__(self, chunk_size: int = 500, chunk_overlap: int = 50):
        """
        Initialize the TextProcessor with text splitting parameters.
        """
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        logger.info(f"Initialized TextProcessor with chunk_size={self.chunk_size} and chunk_overlap={self.chunk_overlap}")

    def extract_text_from_pdf(self, pdf_path: str) -> str:
        """
        Extract text from the local PDF file.
        Args:
            pdf_path (str): Path to the PDF file.
        Returns:
            str: Extracted text from the PDF.
        """
        pdf_path = Path(pdf_path)
        if not pdf_path.exists():
            logger.error(f"PDF file not found at {pdf_path}")
            raise FileNotFoundError(f"PDF file not found at {pdf_path}")

        logger.info(f"Extracting text from PDF: {pdf_path}")
        reader = PdfReader(pdf_path)
        text = ""
        for page_number, page in enumerate(reader.pages, start=1):
            page_text = page.extract_text()
            if page_text:
                logger.debug(f"Extracted text from page {page_number}")
            else:
                logger.warning(f"No text found on page {page_number}")
            text += page_text
        logger.info(f"Finished extracting text from PDF: {pdf_path}")
        return text

    def process_text(self, pdf_path: str):
        """
        Process the PDF file and split the text into chunks.
        Args:
            pdf_path (str): Path to the PDF file.
        Returns:
            List[Document]: A list of processed Document objects.
        """
        logger.info(f"Starting text processing for file: {pdf_path}")
        # Extract text from the PDF
        pdf_text = self.extract_text_from_pdf(pdf_path)

        # Create a Document object for the extracted text
        source_docs = [Document(page_content=pdf_text, metadata={"source": Path(pdf_path).name})]
        logger.info(f"Created Document object with metadata: {source_docs[0].metadata}")

        # Initialize the text splitter
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap,
            add_start_index=True,
            strip_whitespace=True,
            separators=["\n\n", "\n", ".", " ", ""],
        )
        logger.info(f"Initialized text splitter with chunk_size={self.chunk_size} and chunk_overlap={self.chunk_overlap}")

        # Split the document into chunks
        docs_processed = text_splitter.split_documents(source_docs)
        logger.info(f"Text processing complete for file: {pdf_path}. Generated {len(docs_processed)} chunks.")

        # Log each chunk for debugging
        for i, doc in enumerate(docs_processed, start=1):
            logger.debug(f"Chunk {i}: {doc.page_content[:100]}...")  # Log the first 100 characters of each chunk

        return docs_processed
