from ddgs import DDGS
from pypdf import PdfReader
from pdf2image import convert_from_path
import pytesseract


def search_web(query):
    print(f"\nSearching web for: {query}")

    results = []

    with DDGS() as ddgs:
        search_results = ddgs.text(
            query,
            max_results=5
        )

        for result in search_results:
            results.append({
                "title": result.get("title"),
                "url": result.get("href"),
                "snippet": result.get("body")
            })

    return results


def calculator(expression):
    try:
        result = eval(expression)
        return result

    except Exception as e:
        return f"Calculation error: {e}"


def read_pdf(file_path):

    try:

        # --------------------------------
        # Try normal PDF text extraction
        # --------------------------------

        reader = PdfReader(file_path)

        text = ""

        for page in reader.pages:

            page_text = page.extract_text()

            if page_text:
                text += page_text + "\n"

        # --------------------------------
        # If text was found, return it
        # --------------------------------

        if text.strip():

            print("Normal PDF text detected.")

            return text

        # --------------------------------
        # No text found → use OCR
        # --------------------------------

        print("No text found. Using OCR...")

        images = convert_from_path(file_path)

        ocr_text = ""

        for page_number, image in enumerate(images):

            print(f"OCR processing page {page_number + 1}...")

            page_text = pytesseract.image_to_string(image)

            ocr_text += page_text + "\n"

        return ocr_text

    except Exception as e:

        return f"PDF reading error: {e}"