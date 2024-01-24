import PyPDF2
from fpdf import FPDF
import sys
import re
from operator import itemgetter
import subprocess
import nltk
from nltk.corpus import words

def select_chapter(pdf_file, chapter_start_page,chapter_end_page):
    """Selects a chapter from a PDF.

    Args:
        pdf_file: name of the PDF file.
        chapter_start_page: First page of the chapter
        chapter_end_page: last page of the chapter

    Returns:
        A PDF object containing the selected chapter.
    """

    with open(f'{pdf_file}.pdf', 'rb') as f:
        pdf_reader = PyPDF2.PdfReader(f)

        selected_chapter_pdf = PyPDF2.PdfWriter()

        for page_number in range(chapter_start_page, chapter_end_page + 1):
            page = pdf_reader.pages[page_number]
            selected_chapter_pdf.add_page(page)

    return selected_chapter_pdf

def write_pdf():
  pdf_file = input("Write the PDF file name: ")
  chapter_start_page = int(input("Chapter Start Page: "))
  chapter_end_page = int(input("Chapter End Page: "))
  pdf_name = input("New Pdf file name: ")

  selected_chapter_pdf = select_chapter(pdf_file, chapter_start_page,chapter_end_page)

  with open(f'{pdf_name}.pdf', 'wb') as f:
      selected_chapter_pdf.write(f)
  
  return print(f"New PDF has been created as: {pdf_name}")

def write_file():
  start_page = int(input("Start Page: "))
  end_page = int(input("End Page: "))
  
  name_file = input("Name of txt file: ")
  name_pdf = input("Name pdf you want to extract data: ")

  with open(f'{name_file}.txt', 'w') as f:
    reader =  PyPDF2.PdfReader(f"{name_pdf}.pdf")
    for page_number in range(start_page, end_page+1):
            page = reader.pages[page_number]
            f.write(page.extract_text())

  return print(f"{name_file} has been created")


def mapper(input_file):
  word_counts = {}

  with open(input_file, 'r') as f:
        input_lines = f.readlines()

  for line in input_lines:
    line = line.strip().lower()
    words_list = re.findall(r'\w+\b', line)
    for word in words_list:
        word_counts[word] = word_counts.get(word, 0) + 1
  return word_counts

def reducer(input_data, output_file):
    word_counts = {} 

    for word, count in input_data.items():
        try:
            count = int(count)
        except ValueError:
            continue

        if word in word_counts:
            word_counts[word] += count
        else:
            word_counts[word] = count

    sorted_word_counts = sorted(word_counts.items(), key=lambda x: x[0])
    with open(output_file, 'w') as f:
        for word, count in sorted_word_counts:
            f.write(f'{word}\t{count}\n')

def mapper_english(input_file):
  word_counts = {}

  nltk.download('words')

  english_words = set(words.words())

  with open(input_file, 'r') as f:
        input_lines = f.readlines()

  for line in input_lines:
    line = line.strip().lower()
    words_list = re.findall(r'\w+\b', line)
    for word in words_list:
      if word not in english_words:
        word_counts[word] = word_counts.get(word, 0) + 1
  return word_counts

def save_pdf(file1,file2,output_pdf):
  pdf = FPDF()
  pdf.add_page()

  pdf.set_font("Arial", size = 12)

  f = open(file1, "r")
  f2 = open(file2, "r")

  pdf.cell(200, 15, txt = 'MapReduce File 1', ln = 1, align = 'C')
  for x in f:
    pdf.cell(200, 10, txt = x, ln = 1, align = 'L')

  pdf.cell(200, 15, txt = 'MapReduce File 2 - Non English', ln = 1, align = 'C')

  for x in f2:
    pdf.cell(200, 10, txt = x, ln = 1, align = 'L')

  pdf.output(f"{output_pdf}.pdf")

if __name__ == '__main__':
  write_pdf()
  print("File 1:")
  write_file()
  print("File 2 for non-english words: ")
  write_file()
  input_file = input("1st file for Map Reduce: ")
  words_all = mapper(input_file)
  output_file = input("Output file name: ")
  reducer(words_all, output_file)
  input_file_en = input("2nd file for Map Reduce: ")
  words_en = mapper_english(input_file_en)
  output_file_2 = input("Output file name: ")
  reducer(words_en, output_file_2)
  output_pdf = input("Output PDF file name: ")
  save_pdf(output_file,output_file_2,output_pdf)
