# university-chatbot
Project code for CSE 256.

This repository contains code for creating a chatbot that works on a custom database. For the project we considered two databases that contain information for international students at UCSD, one is from HTML text extracted from the ISPO Webpages (UCSD) and the second, a set of PDFs uploaded by ISPO (UCSD.) The files in this repository perform the following function:
1. ChatGPT-Custom Knowledge Base.ipynb - Contains code to install required packages and allows user to specify paths to txt/ pdf files and the notebook can then be run on a set of questions read from a CSV file, or the user can run individual queries from the code cell. The responses will contain the sources as well i.e., it will mention the webpages or the PDF(s) used to answer the query
2. generating_prompt_completion_pairs_chatgpt.py - This file contains code to generate prompt completion pairs using the ChatGPT API. More specifically, given a chunk of text of a specified character length, the code will prompt ChatGPT to generate upto 10 prompt-completion pairs in a specified format for fine-tuning an OpenAI model.
3. pdf_parsing_for_gpt.ipynb - Constains code to parse pdfs and split them into prompt completion pairs. These pairs are then formatted in a way that is best suited to training OpenAI's GPT models and stored in a jsonl file.
4. ISPO_data_processor.ipynb - This file contains the code to generate prompt completion pairs for all the webpages on the ISPO website. This will generate a file of 10 prompt completion pairs per chunk (all in one file). 
5. webpage_scraper.py - This file contains the code to process the output from one webpage after using a web scraper to extract the HTML information. This is then used in the ISPO_data_processor.ipynb
