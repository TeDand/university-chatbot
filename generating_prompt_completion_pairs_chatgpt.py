import openai
import json
import jsonlines

def pdf_to_string(pdf_path):
    list1 = []
    with open(pdf_path, 'rb') as file:
        char_count = 0
        pdf_reader = PyPDF2.PdfReader(file)
        num_pages = len(pdf_reader.pages)
        text = ''
        for page_num in range(num_pages):
            page_txt = pdf_reader.pages[page_num].extract_text()
            if char_count + len(page_txt) < 2000:
                text += page_txt
                char_count += len(page_txt)
            else:
                list1.append(text)
                char_count = len(page_txt)
                text = page_txt
        return list1

jsonl_file = "/content/drive/MyDrive/data/jsons/finetuning_data_pdfs_chatgpt.jsonl"
paths = ['/content/drive/MyDrive/data/pdfs/coming-to-ucsd-guide.pdf', '/content/drive/MyDrive/data/pdfs/ispo-welcome-guide.pdf']

num_requests = 0
with jsonlines.open(jsonl_file, mode='a') as writer:

    for path in paths:
        t = pdf_to_string(path)
        for text in t:
            completion = openai.ChatCompletion.create(
            model = "gpt-3.5-turbo",
            temperature = 0.1,
            max_tokens = 2000,
            messages = [
                {"role": "system", "content": "You are a language expert who needs to help create Question Answer pairs from a given piece of text."},
                {"role": "user", "content": f'Text: \n{text}\n\nTask: Generate upto 10 logical prompt completion pairs from this text. The output should not be numbered and strictly use the foloowing format for your resonse ' + '{"prompt": <text for prompt>, "completion": <text for completion>}'}
            ]
            )
            num_requests += 1
            sample = completion.choices[0].message.content

            for pair in sample.split('\n'):
                p = json.loads(pair)
                p['prompt'] = p['prompt'] + "\n\n###\n\n"
                p['completion'] = p['completion'] + "###"
                writer.write(p)

            if num_requests %25==0:
                print(num_requests)
