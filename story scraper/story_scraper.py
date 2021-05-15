import requests
import bs4
from bs4 import BeautifulSoup

import os

chapter = 0
end_of_book = False
# for chapter in range(100):
while True:
    chapter += 1

    if chapter == 0:
        continue
    text_file = f'chapter{chapter}'

    list_of_files = os.listdir()
    if text_file in list_of_files:
        print(f'{text_file} has already been created')
        continue

    result = requests.get(
        f'https://wuxiaworld.site/novel/book-name-completed/chapter-{chapter}/')

    soup = BeautifulSoup(result.text, 'lxml')
    data = ''
    text = ''
    for data in soup.find_all("p"):

        text += data.get_text() + ' '
        # print(data.get_text())
        if 'Fin.' in data.get_text():
            break
        if '/After Stories Complete.' in data.get_text():
            end_of_book = True
            break

    file = open(text_file, "w+", encoding='utf-8')
    file.write(text)
    file.close()

    if end_of_book:
        break
