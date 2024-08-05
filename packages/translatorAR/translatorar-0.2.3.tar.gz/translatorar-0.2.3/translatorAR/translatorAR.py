from transformers import pipeline
import fitz  # PyMuPDF
import torch
import re
import time
from tqdm import tqdm

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
        """
        models = {
            ("ar", "en"): "Helsinki-NLP/opus-mt-ar-en",
            ("en", "ar"): "Helsinki-NLP/opus-mt-en-ar",
            ("fr", "en"): "Helsinki-NLP/opus-mt-fr-en",
            ("en", "fr"): "Helsinki-NLP/opus-mt-en-fr",
            ("ar", "fr"): "Helsinki-NLP/opus-mt-ar-fr",
            ("fr", "ar"): "Helsinki-NLP/opus-mt-fr-ar"
        }
        print("Initializing translation pipelines...")
        start_time = time.time()
        pipelines = {pair: pipeline("translation", model=model, device=self.device) for pair, model in models.items()}
        print(f"Initialization completed in {time.time() - start_time:.2f} seconds.")
        return pipelines

    def translate(self, text, src_lang, tgt_lang):
        """
        Translates text from source language to target language.
        """
        start_time = time.time()
        self._validate_language_pair(src_lang, tgt_lang)
        chunks = self._chunk_text(text)
        translated_chunks = [self._translate_chunk(chunk, src_lang, tgt_lang) for chunk in tqdm(chunks, desc="Translating")]
        translated_text = self._format_text(' '.join(translated_chunks))
        print(f"Translation completed in {time.time() - start_time:.2f} seconds.")
        return translated_text

    def _validate_language_pair(self, src_lang, tgt_lang):
        """
        Validates if the given language pair is supported.
        """
        if (src_lang, tgt_lang) not in self.translators:
            raise ValueError(f"Translation from {src_lang} to {tgt_lang} is not supported.")

    def _chunk_text(self, text):
        """
        Splits text into manageable chunks based on maximum length.
        """
        return [text[i:i+self.max_length] for i in range(0, len(text), self.max_length)]

    def _translate_chunk(self, chunk, src_lang, tgt_lang):
        """
        Translates a single chunk of text.
        """
        translator = self.translators[(src_lang, tgt_lang)]
        return translator(chunk)[0]['translation_text']

    def _format_text(self, text):
        """
        Formats the text with sentence and line breaks.
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
        """
        start_time = time.time()
        extracted_text = self._extract_text_from_pdf(pdf_path)
        translation_time_start = time.time()
        translated_text = self.translate(extracted_text, src_lang, tgt_lang)
        self._save_to_file(translated_text, output_file)
        print(f"PDF extraction completed in {time.time() - start_time:.2f} seconds.")
        print(f"Total process time (extraction + translation) : {time.time() - start_time:.2f} seconds.")
        return extracted_text, translated_text

    def _extract_text_from_pdf(self, pdf_path):
        """
        Extracts text from each page of a PDF file using PyMuPDF.
        """
        start_time = time.time()
        pdf_document = fitz.open(pdf_path)
        text = ''
        for page_num in tqdm(range(len(pdf_document)), desc="Extracting text from pages"):
            page = pdf_document.load_page(page_num)
            page_text = page.get_text()
            text += page_text + '\n'  # Add a newline after each page
        pdf_document.close()
        print(f"Text extraction completed in {time.time() - start_time:.2f} seconds.")
        return text

    def _save_to_file(self, text, file_path):
        """
        Saves the provided text to a file.
        """
        start_time = time.time()
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(self._format_text(text))
        print(f"Text saved to file in {time.time() - start_time:.2f} seconds.")

    def print_translation(self, src_text, translated_text, src_lang, tgt_lang):
        """
        Prints the source and translated text with formatting and statistics.
        """
        src_word_count = len(src_text.split())
        translated_word_count = len(translated_text.split())
        src_chars = len(src_text)
        translated_chars = len(translated_text)
        src_sentences = src_text.count('.') + src_text.count('!') + src_text.count('?')
        translated_sentences = translated_text.count('.') + translated_text.count('!') + translated_text.count('?')

        print(f"--- Translation from {src_lang} to {tgt_lang} ---")
        print(f"Source Text ({src_lang}):\n{self._format_text(src_text)}\n")
        print(f"Translated Text ({tgt_lang}):\n{self._format_text(translated_text)}\n")
        print(f"Statistics:")
        print(f"  Source Text: {src_word_count} words, {src_chars} characters, {src_sentences} sentences")
        print(f"  Translated Text: {translated_word_count} words, {translated_chars} characters, {translated_sentences} sentences")

    def print_pdf_translation_results(self, pdf_path, src_lang, tgt_lang, output_file):
        """
        Prints the results of translating a PDF file with statistics.
        """
        extracted_text, translated_text = self.translate_pdf(pdf_path, src_lang, tgt_lang, output_file)
        src_word_count = len(extracted_text.split())
        translated_word_count = len(translated_text.split())
        src_chars = len(extracted_text)
        translated_chars = len(translated_text)
        src_sentences = extracted_text.count('.') + extracted_text.count('!') + extracted_text.count('?')
        translated_sentences = translated_text.count('.') + translated_text.count('!') + translated_text.count('?')

        print(f"--- PDF Translation Results ---")
        print(f"Extracted Text from PDF:\n{self._format_text(extracted_text)}\n")
        print(f"Translated Text saved to '{output_file}':\n{self._format_text(translated_text)}\n")
        print(f"Statistics:")
        print(f"  Extracted Text: {src_word_count} words, {src_chars} characters, {src_sentences} sentences")
        print(f"  Translated Text: {translated_word_count} words, {translated_chars} characters, {translated_sentences} sentences")
