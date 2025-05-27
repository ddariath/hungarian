import re
import spacy
import os
from hunspell import Hunspell

hspell = Hunspell("hu_HU", hunspell_data_dir="D:\\Work\\projects\\pycharm\\hunspell_dicts")

nlp = spacy.load("hu_core_news_lg", disable=['parser', 'ner'])
nlp.max_length = 2_000_000


def clean_text(text):
    lines = [line for line in text if len(line) > 15]
    text = ''.join(lines)
    # Удаление номеров страниц (например, "3 \n" в начале строки)
    text = re.sub(r'^\d+\s*[\r\n]', '', text, flags=re.MULTILINE)
    # Удаление переносов слов (соединяет слова, разделённые дефисом и переводом строки)
    text = re.sub(r'(\w+)-\s*[\r\n]\s*(\w+)', r'\1\2', text)
    # Удаление лишних пробелов и переносов строк
    text = ' '.join(text.split())
    return text


def process_text(text):
    text = clean_text(text)

    text = re.sub(r'\d+', '0', text)  # заменяем все числа на 0

    result = []
    # print('Начало nlp')
    doc_text = nlp(text)
    # print('Конец nlp')
    for sent in doc_text.sents:
        for token in sent:
            token_in_vocabulary = token
            if token_in_vocabulary.is_oov:  # обработка опечаток
                print("опечатка " + str(token_in_vocabulary.text))
                suggestions = hspell.suggest(token_in_vocabulary.text)
                word = suggestions[0] if suggestions else token_in_vocabulary.text
                doc_word = nlp(word)
                token_in_vocabulary = doc_word[0]

            if token_in_vocabulary.pos_ == 'NUM':
                result.append('0')  # заменяем числительные на 0
            elif token_in_vocabulary.pos_ == 'PRON':
                result.append('1')  # заменяем местоимения на 1
            elif token_in_vocabulary.pos_ == 'PROPN':
                result.append('2')  # заменяем имена собственные на 2
            elif token_in_vocabulary.pos_ != 'PUNCT':
                lemma = token_in_vocabulary.lemma_.lower()
                result.append(lemma)

    return ' '.join(result)


def full_process_text(filename):
    try:
        print('Файл начал обрабатываться ' + filename)

        path_in = os.path.join('D:\\Work\\projects\\pycharm\\txts', filename)
        path_out = os.path.join('D:\\Work\\projects\\pycharm\\results2', f'lemmatized_{filename}')

        with open(path_in, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            print('Файл прочитан ' + filename)

        with open(path_out, 'w', encoding='utf-8') as f:
            print('Текст начал обрабатываться ' + filename)
            result = process_text(lines)
            print('Текст закончил обрабатываться ' + filename)
            f.write(result)
            print('Результат записан ' + filename)

    except Exception as e:
        print('!!! ОШИБКА при обработке файла ' + filename + ' ' + str(e))


