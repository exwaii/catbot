from pdf2image import convert_from_path
from PyPDF2 import PdfWriter, PageObject
from discord import File

def pages_to_image(pages: list[PageObject]) -> list[File]:
    writer = PdfWriter()
    for page in pages:
        writer.add_page(page)

    with open("temp/temp.pdf", "wb") as f:
        writer.write(f)
        
    pages = convert_from_path("temp/temp.pdf", dpi=500)
    for i, page in enumerate(pages):
        page.save(f"temp/{i}.jpg", "JPEG")
    images = []
    for i in range(len(pages)):
        with open(f"temp/{i}.jpg", "rb") as f:
            image = File(f)
            images.append(image)
    
    return images