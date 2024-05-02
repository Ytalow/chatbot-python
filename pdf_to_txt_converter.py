import os
import PyPDF2

pdf_file = open("context.pdf", "rb")

text = ""
reader = PyPDF2.PdfReader(pdf_file)
for page_number in range(len(reader.pages)):
    page = reader.pages[page_number]
    text += "\n" + page.extract_text()

path = os.path.abspath("../chatbot-python")
open("text.txt", "w").close()
txt_file = open(r"%s/text.txt" % (path), "a")
txt_file.writelines(text)
