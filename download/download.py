import os
import requests
from bs4 import BeautifulSoup
import re
from requests.exceptions import Timeout, RequestException


def save_pdf(short_url, df, timeout=30):
    url = 'https://mek.oszk.hu' + short_url  # ссылка на страницу с информацией о книге

    save_path = 'D:\coursework25\originals'  # целевая директория

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

    # парсим общую страницу, извлекаем название и ссылку на скачивание
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    title = soup.find('h3', class_='title').text.strip()  # название
    link_tag = soup.find('a', class_='cssfile pdf', href=True)  # поиск тега пдф
    if not link_tag:
        print("PDF-файл не найден")
        return False
    download_link = link_tag['href']  # берем ссылку на скачивание

    # если нашлась ссылка на пдф
    if download_link:
        if not download_link.startswith('http'):
            download_link = 'https://mek.oszk.hu' + download_link

        try:
            bytes_incorrect = title.encode('iso-8859-1')
            correct_title = bytes_incorrect.decode('utf-8')
        except:
            return False

        title = re.sub(' ', '_', correct_title)
        title = re.sub('\.\.\.', '', title)
        title = re.sub('__', '_', title)
        title = re.sub(r'[\\/*?:"<>|,]', '', title)
        if len(title) > 100:
            title = title[:100]

        file_name = f"{title}.pdf"
        full_path = os.path.join(save_path, file_name)
        session = requests.Session()
        try:
            with session.get(download_link, stream=True, timeout=30) as response:
                response.raise_for_status()
                with open(full_path, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        if chunk:  # фильтруем keep-alive chunks
                            f.write(chunk)
        except Exception as e:
            print(f"Ошибка загрузки: {e}")
            return False

        df.loc[df['url'] == short_url, 'format'] = 'pdf'
        print(f"Файл сохранен как {full_path}")
        return True

    else:
        print("PDF-файл не найден")
        return False

