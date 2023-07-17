import PyPDF2
import os
import re


def split_pdf_to_text(pdf_path, output_folder, pages_per_chunk):
    # Create the output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)

    with open(pdf_path, 'rb') as pdf_file:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        num_pages = len(pdf_reader.pages)

        num_chunks = (num_pages // pages_per_chunk) + (num_pages % pages_per_chunk > 0)

        for i in range(num_chunks):
            start_page = i * pages_per_chunk
            end_page = start_page + pages_per_chunk if start_page + pages_per_chunk < num_pages else num_pages

            chunk_filename = output_folder +f"_{i + 1}.txt"
            chunk_path = os.path.join(output_folder, chunk_filename)

            with open(chunk_path, 'w') as chunk_file:
                for page_num in range(start_page, end_page):
                    page = pdf_reader.pages[page_num]
                    text = page.extract_text()
                    chunk_file.write(text)

    print(f"PDF '{pdf_path}' successfully split into text chunks in '{output_folder}'.")



# Usage example
# pdf_path = 'kurs-samoleczenia.pdf'
# output_folder = 'kurs-samoleczenia'

pdf_path = 'Benjamin Graham - Inteligentny inwestor.pdf'
output_folder = 'Benjamin Graham - Inteligentny inwestor'

pages_per_chunk = 5  # Specify the desired number of pages per chunk
split_pdf_to_text(pdf_path, output_folder, pages_per_chunk)