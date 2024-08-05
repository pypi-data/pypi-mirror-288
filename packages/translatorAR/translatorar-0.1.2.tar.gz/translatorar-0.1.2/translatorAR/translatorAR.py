from transformers import pipeline
import fitz  # PyMuPDF
from tqdm import tqdm  # Import tqdm

class TranslatorAR:
    def __init__(self):
        # Initialize translation pipelines for the supported language pairs
        self.translators = {
            ("ar", "en"): pipeline("translation", model="Helsinki-NLP/opus-mt-ar-en", device=0),
            ("en", "ar"): pipeline("translation", model="Helsinki-NLP/opus-mt-en-ar", device=0),
            ("fr", "en"): pipeline("translation", model="Helsinki-NLP/opus-mt-fr-en", device=0),
            ("en", "fr"): pipeline("translation", model="Helsinki-NLP/opus-mt-en-fr", device=0),
            ("ar", "fr"): pipeline("translation", model="Helsinki-NLP/opus-mt-ar-fr", device=0),
            ("fr", "ar"): pipeline("translation", model="Helsinki-NLP/opus-mt-fr-ar", device=0),
        }
        self.max_length = 512  # Adjust based on the model's max length if needed

    def translate(self, text, src_lang, tgt_lang):
        # Validate the language pair
        if (src_lang, tgt_lang) not in self.translators:
            raise ValueError(f"Translation from {src_lang} to {tgt_lang} is not supported.")
        
        # Split text into chunks if it's too long
        translator = self.translators[(src_lang, tgt_lang)]
        chunks = [text[i:i+self.max_length] for i in range(0, len(text), self.max_length)]
        
        translated_chunks = []
        for i, chunk in tqdm(enumerate(chunks), total=len(chunks), desc="Translating chunks"):
            result = translator(chunk)
            translated_chunks.append(result[0]['translation_text'])
        
        # Join all chunks into a single string
        translated_text = ' '.join(translated_chunks)
        return translated_text

    def translate_pdf(self, pdf_path, src_lang, tgt_lang, output_file):
        # Extract text from the PDF
        extracted_text = self.extract_text_from_pdf(pdf_path)

        # Translate the extracted text
        translated_text = self.translate(extracted_text, src_lang, tgt_lang)

        # Save translated text to a file
        with open(output_file, 'w', encoding='utf-8') as file:
            file.write(translated_text)

        return extracted_text, translated_text
    
    def extract_text_from_pdf(self, pdf_path):
        # Extract text from each page of the PDF
        document = fitz.open(pdf_path)
        text = ''
        for page_num in tqdm(range(len(document)), desc="Extracting pages"):
            page = document.load_page(page_num)
            text += page.get_text()
        return text
    
# Example usage
if __name__ == "__main__":
    translator = TranslatorAR()
    
    PDF_FILE_PATH = "arabic-text.pdf"
    
    # Example 1: Arabic to English
    text_ar_en = "هذا المساق مقدم من Hugging Face."
    translated_text_ar_en = translator.translate(text_ar_en, "ar", "en")
    print(f"Arabic to English: {translated_text_ar_en}")

    # Example 2: English to Arabic
    text_en_ar = "This course is produced by Hugging Face."
    translated_text_en_ar = translator.translate(text_en_ar, "en", "ar")
    print(f"English to Arabic: {translated_text_en_ar}")

    # Example 3: Arabic to French
    text_ar_fr = "أهلاً وسهلاً بكم في هذا المساق."
    translated_text_ar_fr = translator.translate(text_ar_fr, "ar", "fr")
    print(f"Arabic to French: {translated_text_ar_fr}")

    # Example 4: French to Arabic
    text_fr_ar = "Bienvenue dans ce cours."
    translated_text_fr_ar = translator.translate(text_fr_ar, "fr", "ar")
    print(f"French to Arabic: {translated_text_fr_ar}")

    # Example 1.bis: Translate Arabic PDF to English
    translator.translate_pdf(PDF_FILE_PATH, "ar", "en", 'translated_to_english.txt')

    # Example 2.bis: Translate English PDF to Arabic
    translator.translate_pdf(PDF_FILE_PATH, "en", "ar", 'translated_to_arabic.txt')

    # Example 3.bis: Translate Arabic PDF to French
    translator.translate_pdf(PDF_FILE_PATH, "ar", "fr", 'translated_to_french.txt')

    # Example 4.bis: Translate French PDF to Arabic
    translator.translate_pdf(PDF_FILE_PATH, "fr", "ar", 'translated_to_arabic.txt')
