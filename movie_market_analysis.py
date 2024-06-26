# -*- coding: utf-8 -*-
"""Movie_Market_Analysis.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1S3aaVkhw8osaLdtgneBaGfyT9ORNd5Yh
"""

# @title List of custom functions to run as well as libraries to install. This will install requirements for rest of code to run.

#Imports needed to install
#Try/Except to not install more than once

try:
    import PyPDF2
except ImportError:
    !pip install PyPDF2
    import PyPDF2

try:
    import tiktoken
except ImportError:
    !pip install tiktoken
    import tiktoken

try:
    import openai
except ImportError:
    !pip install openai
    import openai

#Import list
import os
import string

def save_as_txt(formatted_text, chunks):

  # Specify the file name and open the file in write mode
  file_name = tiktoken.get_encoding("cl100k_base").decode(chunks[0]).split(" by", 1)[0] + " Output.txt"

  #try to name as movie title, else name output.txt
  try:
    # Open the file in write mode ("w" mode)
    with open(file_name, "w") as file:
        # Write the data to the file
        file.write(formatted_text)
  except OSError:
    file_name = "Output.txt"
    # Open the file in write mode ("w" mode)
    with open(file_name, "w") as file:
        # Write the data to the file
        file.write(formatted_text)

def print_chunks(chunks):
  # Print the chunks and their counts
  for i, chunk in enumerate(chunks):
      variable_name = f"chunk_{i+1}"
      exec(f"{variable_name} = {chunk}")
      print(f"{variable_name}: {len(chunk)} tokens")

def model_context():

  context = "Never mention film festivals thoughout the whole analysis. Especially in the marketing plan and marketing budget parts. Do not begin the output with a defenition on what is market segmentation. Never mention the name of the movie. Under each type of segmentation, do not make a list, instead, make a block of text. For each element in the segmentation analysis, provide reasoning on why based on the movie's content and be very specific on this, maybe even mentioning names in the process. Describe the target audience on each type of market segmentation. Work with what you have and do not try to predict the outcome of the movie. Add a lot of text to the segmentation analysis. Also be specific in areas of interest for an investor. Add text that explains how to capture the target audience with each element of the segmentation analysis. The more text each element of the segmentation analysis has, the better. You will analyze the movie given and will apply market segmentation analysis, make this the priority and talk a lot about each element of the segementation analysis. Dive deep into each element of the market segmentation analysis. Make the results of the market segmentation very long with lots of detail. The more extensive the research, the better. Try to convince an investor with your findings. Never mention film festivals thoughout the whole analysis. Please take into account the 4 types of market segmentation. For the market segmentation part: extend/develop more on each segmentation. Always give a age number estimate range of the audience when doing demographic segmentation. You are looking for a target audience and will describe it with a lot of details. For each element in the market segmentation analysis, you will expand/develop more on each. After the segmentation analysis part: Include a sole section of keywords for the targeted audience at the end of the market analysis in list format. Afterwards: include a section for similar films that would likely share it's audience. Never mention film festivals thoughout the whole analysis. State a brief/overall marketing plan using the results of the market segmentation analysis and make this a list. After the marketing plan section, insert a new section with recommend percentages of the budget to each element of the marketing plan and give a bit of reasoning behind each. Give a bit of reasoning behind each percentage budget element. Give input towards creative assets, helping make the trailer and what the trailer should focus on. Never mention film festivals thoughout the whole analysis."

  return context

def model_content(chunks):

  if len(chunks) == 0: print("Error importing text from PDF, this needs debugging")
  elif len(chunks) == 1: content = tiktoken.get_encoding("cl100k_base").decode(chunks[0])
  elif len(chunks) == 2: content = tiktoken.get_encoding("cl100k_base").decode(chunks[0]) + tiktoken.get_encoding("cl100k_base").decode(chunks[-1])
  else: content = tiktoken.get_encoding("cl100k_base").decode(chunks[1]) + tiktoken.get_encoding("cl100k_base").decode(chunks[-1])

  return content

def pdf_to_text():

  # Specify the directory path where PDF files are located (VERY IMPORTANT - MODIFY FOR OTHER APPLICATIONS)
  directory_path = "/content/"

  # Initialize an empty string to store the extracted text
  text = ""

  # Iterate through each file in the directory
  for filename in os.listdir(directory_path):
      if filename.endswith(".pdf"):
          # Construct the full path to the PDF file
          pdf_path = os.path.join(directory_path, filename)

          # Open the PDF file in binary read mode
          with open(pdf_path, "rb") as pdf_file:
              # Create a PDF reader object
              pdf_reader = PyPDF2.PdfReader(pdf_file)

              # Iterate through each page of the PDF
              for page_num in range(len(pdf_reader.pages)):
                  # Extract the text from the current page
                  page = pdf_reader.pages[page_num]
                  text += page.extract_text()

  return text



def clean_text(text):

  # Join the words back together with a single space between each word
  text = ' '.join(text.split())

  # Define a translation table to remove punctuation, commas, and apostrophes
  translator = str.maketrans('', '', string.punctuation + "’“”")

  # Apply the translation to the input string
  cleaned_string = text.translate(translator)

  return cleaned_string



def encode_text(cleaned_string):

  # Get the encoding for "cl100k_base"
  enc = tiktoken.get_encoding("cl100k_base")

  # Encode the text using the obtained encoding
  encoded_text = enc.encode(cleaned_string)

  return encoded_text



def break_encoded_into_chunks(encoded_text):

  # Maximum chunk size (6000 tokens)
  max_chunk_size = 6000

  # Initialize a list to store the chunks
  chunks = []

  # Split the cleaned string into chunks of up to 6000 characters each
  while encoded_text:
      if len(encoded_text) <= max_chunk_size:
          # If the remaining string is shorter than 6000 characters, add it as a chunk
          chunks.append(encoded_text)
          break
      else:
          # Extract the chunk
          chunk = encoded_text[:max_chunk_size]
          chunks.append(chunk)
          # Remove the processed chunk from the cleaned_string
          encoded_text = encoded_text[max_chunk_size+1:]

  return chunks

# @title This will open the PDF, convert to text, clean text, encode text and break text into chunks for AI to read. { vertical-output: true }

# Text variable that will contain pdf in text
text = pdf_to_text()

# This will clean the text variable
cleaned_string = clean_text(text)

# This will encode the cleaned text for chunk separation
encoded_text = encode_text(cleaned_string)

# This will break the encoded text into chunks for AI to read
chunks = break_encoded_into_chunks(encoded_text)

# Content and Context variables for AI model input
content = model_content(chunks)
context = model_context()

# Set openai API Key here. Substitue "OPEN_API_KEY" with real Key inside quotation marks
key = os.environ['api_key']

# Just a bit of a safegaurd to remember to insert correct key if default value hasnt been modified
if key == "OPENAI_API_KEY": print("Please check key variable and insert correct key")

# For debugging only
#print_chunks(chunks)

# @title This is the AI model, it has been seperated from the rest of the code so it can be executed more than once with the same data input (no need to open pdf and clean data again)
openai.api_key = key
response = openai.ChatCompletion.create(
  model="gpt-3.5-turbo-16k",
  messages=[
     {
      "role": "system",
      "content": context
    },
    {
      "role": "user",
      "content": content
      }
  ],
  temperature=0.8,
  max_tokens=1500, #set to 1500 tokens for AI output
  top_p=1,
  frequency_penalty=0,
  presence_penalty=0
)

response_text = response.choices[0].message.content

# Replace newline characters with line breaks and add indentation
formatted_text = response_text.replace("\n", "\n\n")

save_as_txt(formatted_text, chunks)