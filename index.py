# This file will loop through all files in directory index and run GPT on the content of each file

import os
import PyPDF2
from openai import OpenAI

client = OpenAI(
    api_key=os.environ.get("MY_API_KEY"),
)

# Set the temperature
temperature = 0.0
# Set the max tokens
max_tokens = 500
# Set the top p
top_p = 1
# Set the frequency penalty
frequency_penalty = 0.5
# Set the presence penalty
presence_penalty = 0.0
# get content of file

# Extract text from PDF using PyPDF2

def extract_text_from_pdf(pdf_path):

    pdfFileObj = open(pdf_path, 'rb')
    pdfReader = PyPDF2.PdfFileReader(pdfFileObj)

    text = ""

    for i in range(0, pdfReader.numPages):
        pageObj = pdfReader.getPage(i)
        text += pageObj.extractText()

    return text

def gpt_run(text):
    response = client.chat.completions.create(
    model="gpt-3.5-turbo-1106",
    messages=[{"role":"system","content":"You are an AI assistant that takes as input an academic paper and returns only Library of Congress subject headings that are relevant to the paper. Only respond with subject headings and nothing else. Make them of the format #subject-heading with a dash between words."},
                        {"role":"user","content":text},]

)
    print(response.choices[0].message.content)
    headings = response.choices[0].message.content
    return headings

# save content to a markdown file of the same name as the pdf

def save_to_markdown(headings, filename):
    headings = headings.replace(" ", "-")
    with open(f"{filename}.md", 'w') as f:
        f.write(headings)
        f.close()

def main():
    for filename in os.listdir('index'):
        if filename.endswith(".pdf"):
            print(filename)
            text = extract_text_from_pdf(f"index/{filename}")
            headings = gpt_run(text)
            save_to_markdown(headings, filename)
            continue
        else:
            continue

if __name__ == "__main__":
    main()