import os


def extract_pages(input_file, start_page, end_page, output_file):
    """
    Extracts pages from a PDF file and saves them as a new PDF file
    starting from start_page and ending at end_page (inclusive).

    Args:
        input_file (str): path to the input PDF file
        start_page (int): number of the first page to extract
        end_page (int): number of the last page to extract
        output_file (str): path to the output PDF file

    Returns:
        None
    """
    from PyPDF2 import PdfWriter, PdfReader
    # Open input PDF file
    with open(input_file, 'rb') as f:
        reader = PdfReader(f)

        # Create a new PDF writer
        writer = PdfWriter()

        # Extract pages from input PDF and add them to the writer
        for page in reader.pages[start_page - 1:end_page][::-1]:
            writer.insert_page(page)

        # Write output PDF file
        with open(output_file, 'wb') as out:
            writer.write(out)


def clear_sols(folder_path):
    """Removes all papers in a folder with titles that potentially contain solutions

    Args:
        folder_path (str): path of folder to clear
    """
    for filename in os.listdir(folder_path):
        filename = filename.lower()
        if "solutions" in filename or "answers" in filename or "criteria" in filename or "solns" in filename or "soln" in filename or "ans" in filename:
            os.remove(os.path.join(folder_path, filename))
            print(filename)


def main():
    pass   


if __name__ == "__main__":
    main()
