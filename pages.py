import re
from PyPDF2 import PageObject, PdfReader

def page_start(pages: list[PageObject]) -> int:
    """finds page number of where Section II starts (zero indexed)

    Args:
        pages (list[PageObject]): pages to parse, list of PyPDF2's PageObjects

    Returns:
        int: page number of where Section II starts (zero indexed)
    """
    for (i, page) in enumerate(pages):
        content = page.extract_text()
        if (re.findall(r'Section[.\s]*?((I[.\s]*?I)|2)', content, flags=re.IGNORECASE)) and i > 1: # first page usually contains section II as well.
            return i

def main():
    reader = PdfReader(open("papers/nsb drive 2020 trials/2020 North Sydney Boys High School - X1 - Trial.pdf", "rb"))
    print(reader.pages[-1].extract_text())


if __name__ == "__main__":
    main()