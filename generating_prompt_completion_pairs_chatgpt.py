import openai

completion = openai.ChatCompletion.create(
  model = "gpt-3.5-turbo",
  temperature = 0.1,
  max_tokens = 2000,
  messages = [
    {"role": "system", "content": "You are a language expert who needs to help create Question Answer pairs from a given piece of text."},
    {"role": "user", "content": f'Text: \n{t[0]}\n\nTask: Generate upto 10 logical prompt completion pairs from this text. The output should not be numbered and strictly use the foloowing format for your resonse ' + '{"prompt": <text for prompt>, "completion": <text for completion>}'}
  ]
)
sample = completion.choices[0].message.content

sample

sample.split('\n')

# . Make sure append "###\n\n\n###" to the end of the text for prompt and append "###" to the end of the text for completion.

import json
import jsonlines

# Specify the path to the output JSONL file
jsonl_file = "/content/drive/MyDrive/data/jsons/finetuning_data_pdfs_chatgpt.jsonl"

# Open the JSONL file in write mode
with jsonlines.open(jsonl_file, mode='w') as writer:
    # Write each dictionary as a separate line in the JSONL file
    for pair in sample.split('\n'):
        p = json.loads(pair)
        p['prompt'] = p['prompt'] + "\n\n###\n\n"
        p['completion'] = p['completion'] + "###"
        writer.write(p)

