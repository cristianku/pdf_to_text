import os
from pdf2image import convert_from_path
import pytesseract
import camelot


def is_page_text_based(image):
    # Custom logic to determine if an image-based page contains text
    # You can use your own criteria here based on the characteristics of the pages

    # Example logic: Check if the image has a certain percentage of black pixels
    pixel_threshold = 0.95  # Minimum percentage of non-black pixels to consider it text-based
    num_pixels = image.width * image.height
    num_black_pixels = sum(1 for pixel in image.getdata() if pixel == 0)

    return (num_black_pixels / num_pixels) < pixel_threshold


def split_pdf_to_text(pdf_path, output_folder, pages_per_chunk):
    # Create the output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)

    images = convert_from_path(pdf_path)
    num_pages = len(images)

    num_chunks = (num_pages // pages_per_chunk) + (num_pages % pages_per_chunk > 0)

    for i in range(num_chunks):
        start_page = i * pages_per_chunk
        end_page = start_page + pages_per_chunk if start_page + pages_per_chunk < num_pages else num_pages

        chunk_filename = f"chunk_{i + 1}.txt"
        chunk_path = os.path.join(output_folder, chunk_filename)

        with open(chunk_path, 'w', encoding='utf-8') as chunk_file:
            for page_num in range(start_page, end_page):
                image = images[page_num]

                if is_page_text_based(image):
                    # Perform OCR on the entire page
                    page_text = pytesseract.image_to_string(image, config='--psm 6 --oem 3')

                    # Use Camelot for table detection
                    tables = camelot.read_pdf(pdf_path, pages=str(page_num + 1))

                    # Extract non-table text by subtracting table text from the entire page text
                    for table in tables:
                        table_text = " ".join(table.df.stack().astype(str))
                        page_text = page_text.replace(table_text, '')

                    chunk_file.write(page_text)

    print(f"PDF '{pdf_path}' successfully split into text chunks in '{output_folder}'.")


# List PDF files in the current folder
pdf_files = [file for file in os.listdir() if file.endswith('.pdf')]

# Display the numbered list of PDF files
print("Available PDF files:")
for i, pdf_file in enumerate(pdf_files):
    print(f"{i+1}. {pdf_file}")

# Ask the user to choose a file by number
file_number = int(input("Enter the number of the PDF file you want to convert: "))
if file_number < 1 or file_number > len(pdf_files):
    print("Invalid file number.")
    exit()

# Get the chosen file name
chosen_file = pdf_files[file_number - 1]

# Ask for the desired number of pages per chunk
pages_per_chunk = int(input("Enter the number of pages per chunk: "))

# Create the output folder with the name of the chosen PDF file
output_folder = os.path.splitext(chosen_file)[0]

# Convert the chosen PDF file to text
split_pdf_to_text(chosen_file, output_folder, pages_per_chunk)
