import os
import pandas as pd
from tqdm import tqdm

df = pd.DataFrame(columns=['text_name'])

directory = 'D:\\coursework25\\lemmatized_txts\\all_results'
files = os.listdir(directory)

for filename in tqdm(files):
    lemmatized_path = os.path.join(directory, filename)

    with open(lemmatized_path, 'r', encoding='utf-8') as file:
        text = file.read()

    with open('D:\\coursework25\\lemmatized_txts\\hu_corpus.txt', 'a', encoding='utf-8') as file:
        file.write(text + '\n')

    new_data = pd.DataFrame([['_'.join(filename.split('_')[1:])]], columns=df.columns)
    df = pd.concat([df, new_data], ignore_index=True)

df.to_csv('D:\\coursework25\\lemmatized_txts\\corpus_order.csv', index=True, encoding='utf-8')

with open('D:\\coursework25\\lemmatized_txts\\hu_corpus.txt', 'r', encoding='utf-8') as file:
    lines = file.readlines()
    print(len(lines))
