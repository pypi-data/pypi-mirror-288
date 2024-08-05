from transformers import pipeline
from pdf2image import convert_from_path
from PIL import Image
import pytesseract
import torch  # For device management
import re  # For text formatting
from tqdm import tqdm  # For progress bars

class TranslatorAR:
    """
    TranslatorAR is a class for translating text between Arabic, English, and French using Hugging Face's translation models.
    It supports both direct text translation and PDF file translation.
    """
    def __init__(self):
        """
        Initializes the TranslatorAR with translation pipelines and GPU/CPU configuration.
        """
        self.device = 0 if torch.cuda.is_available() else -1
        self.translators = self._initialize_pipelines()
        self.max_length = 512

    def _initialize_pipelines(self):
        """
        Initializes translation pipelines for supported language pairs.

        :return: Dictionary mapping language pairs to translation pipelines
        """
        models = {
            ("ar", "en"): "Helsinki-NLP/opus-mt-ar-en",
            ("en", "ar"): "Helsinki-NLP/opus-mt-en-ar",
            ("fr", "en"): "Helsinki-NLP/opus-mt-fr-en",
            ("en", "fr"): "Helsinki-NLP/opus-mt-en-fr",
            ("ar", "fr"): "Helsinki-NLP/opus-mt-ar-fr",
            ("fr", "ar"): "Helsinki-NLP/opus-mt-fr-ar"
        }
        return {pair: pipeline("translation", model=model, device=self.device) for pair, model in models.items()}

    def translate(self, text, src_lang, tgt_lang):
        """
        Translates text from source language to target language.

        :param text: Text to translate
        :param src_lang: Source language code
        :param tgt_lang: Target language code
        :return: Translated text with formatting
        :raises ValueError: If the language pair is not supported
        """
        self._validate_language_pair(src_lang, tgt_lang)
        chunks = self._chunk_text(text)
        translated_chunks = [self._translate_chunk(chunk, src_lang, tgt_lang) for chunk in tqdm(chunks, desc="Translating chunks")]
        return self._format_text(' '.join(translated_chunks))

    def _validate_language_pair(self, src_lang, tgt_lang):
        """
        Validates if the given language pair is supported.

        :param src_lang: Source language code
        :param tgt_lang: Target language code
        :raises ValueError: If the language pair is not supported
        """
        if (src_lang, tgt_lang) not in self.translators:
            raise ValueError(f"Translation from {src_lang} to {tgt_lang} is not supported.")

    def _chunk_text(self, text):
        """
        Splits text into manageable chunks based on maximum length.

        :param text: Text to chunk
        :return: List of text chunks
        """
        return [text[i:i+self.max_length] for i in range(0, len(text), self.max_length)]

    def _translate_chunk(self, chunk, src_lang, tgt_lang):
        """
        Translates a single chunk of text.

        :param chunk: Text chunk to translate
        :param src_lang: Source language code
        :param tgt_lang: Target language code
        :return: Translated text chunk
        """
        translator = self.translators[(src_lang, tgt_lang)]
        return translator(chunk)[0]['translation_text']

    def _format_text(self, text):
        """
        Formats the text with sentence and line breaks.

        :param text: Text to format
        :return: Formatted text
        """
        text = re.sub(r'\s+([?.!,"])', r'\1', text)  # Normalize spaces around punctuation
        text = re.sub(r'(?<!\n)\.\s', '.\n', text)  # Add line breaks after sentences
        text = re.sub(r'(?<!\n)\!\s', '!\n', text)
        text = re.sub(r'(?<!\n)\?\s', '?\n', text)
        text = re.sub(r'\n+', '\n', text).strip()  # Normalize multiple newlines
        text = re.sub(r'([.!?])(\w)', r'\1 \2', text)  # Ensure a single space after punctuation
        text = re.sub(r'\s+', ' ', text)  # Normalize whitespace
        return text

    def translate_pdf(self, pdf_path, src_lang, tgt_lang, output_file):
        """
        Extracts text from a PDF, translates it, and saves the translated text to a file.

        :param pdf_path: Path to the PDF file
        :param src_lang: Source language code
        :param tgt_lang: Target language code
        :param output_file: Path to the output file
        :return: Tuple of extracted text and translated text
        """
        extracted_text = self._extract_text_from_pdf(pdf_path)
        translated_text = self.translate(extracted_text, src_lang, tgt_lang)
        self._save_to_file(translated_text, output_file)
        return extracted_text, translated_text

    def _extract_text_from_pdf(self, pdf_path):
        """
        Extracts text from each page of a PDF file by converting it to images and then using OCR.

        :param pdf_path: Path to the PDF file
        :return: Extracted text
        """
        images = convert_from_path(pdf_path)
        text = ''
        for img in tqdm(images, desc="Extracting text from images"):
            # Perform OCR on the image
            page_text = pytesseract.image_to_string(img, lang='ara+eng+fra')  # Adjust language codes as needed
            # Normalize line breaks and spaces
            page_text = re.sub(r'\n+', '\n', page_text).strip()
            page_text = re.sub(r'\s+', ' ', page_text)
            text += page_text + '\n'  # Add a newline after each page
        return text

    def _save_to_file(self, text, file_path):
        """
        Saves the provided text to a file.

        :param text: Text to save
        :param file_path: Path to the file
        """
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(self._format_text(text))

    def print_translation(self, src_text, translated_text, src_lang, tgt_lang):
        """
        Prints the source and translated text with formatting.

        :param src_text: Source text
        :param translated_text: Translated text
        :param src_lang: Source language code
        :param tgt_lang: Target language code
        """
        print(f"--- Translation from {src_lang} to {tgt_lang} ---")
        print(f"Source Text ({src_lang}):\n{self._format_text(src_text)}\n")
        print(f"Translated Text ({tgt_lang}):\n{self._format_text(translated_text)}\n")

    def print_pdf_translation_results(self, pdf_path, src_lang, tgt_lang, output_file):
        """
        Prints the results of translating a PDF file.

        :param pdf_path: Path to the PDF file
        :param src_lang: Source language code
        :param tgt_lang: Target language code
        :param output_file: Path to the output file
        """
        extracted_text, translated_text = self.translate_pdf(pdf_path, src_lang, tgt_lang, output_file)
        print(f"--- PDF Translation Results ---")
        print(f"Extracted Text from PDF:\n{self._format_text(extracted_text)}\n")
        print(f"Translated Text saved to '{output_file}':\n{self._format_text(translated_text)}\n")
