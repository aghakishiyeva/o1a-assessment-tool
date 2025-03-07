from pdfminer.high_level import extract_text
import io


def extract_text_from_pdf(contents):
    fp = io.BytesIO(contents)
    text = extract_text(fp)
    return text
