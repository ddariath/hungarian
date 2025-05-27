import os
import PyPDF2
from Crypto.Cipher import AES


# конвертация из pdf в txt
def pdf_to_txt(pdf_path):
    title = pdf_path.split('\\')[-1][:-4]  # название книги
    txt_name = f'{title}.txt'
    try:
        with open(pdf_path, 'rb') as pdf_file:
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            text = ''
            for page_n in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_n]
                text += page.extract_text()
        save = 'D:\coursework25/txts'  # целевая директория
        output_txt = os.path.join(save, txt_name)
        with open(output_txt, 'w', encoding='utf-8') as txt_file:
            txt_file.write(text)
            print(f'Файл сохранен по адресу {output_txt}')
    except Exception as e:
        print(f'Что-то пошло не так с файлом {txt_name}: {e}')
    return


done = [s[:-4] for s in os.listdir('D:\coursework25/txts')]  # список названий уже конвертированных файлов (без формата)
directory = 'D:\coursework25\originals'  # папка с пдф-файлами
# итерируемся по pdf-файлам и конвертируем все
for filename in os.listdir(directory):
    # decoded_name = os.fsdecode(filename)
    if filename[:-4] not in done:
        full_path = os.path.join(directory, filename)  # путь к pdf-файлу
        pdf_to_txt(full_path)
    else:
        print(f'Файл уже конвертирован: {filename}')

