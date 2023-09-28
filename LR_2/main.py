from requests_html import HTMLSession
from bs4 import BeautifulSoup
import re
import sys

session = HTMLSession()

output_text = ""
# Поиск по названию
name = input('Введите название дорамы латиницей (например: nachalo, luchshie dni, mest nevesty):')
name = name.split()
name = '_'.join(name)

url=f'https://doramatv.live/{name}'

r = session.get(url)
soup = BeautifulSoup(r.text, 'lxml')

#инфо по дораме
names = r.html.find('.names', first=True)
if names:
    output_text+=f'Информация о дораме:   "{names.text}": '+'\n'

    #фильм или сериал
    info_1=r.html.find('div.subject-meta > p')
    for x in info_1[:2]:
        list_1=[]
        list_1.append(x.text)
        output_text += ' '.join(list_1) + '\n'

    #основная ифно
    info5=r.html.find('p.elementList')
    for x in info5:
        list_1=[]
        list_1.append(x.text)
        output_text += ' '.join(list_1) + '\n'

    #описание
    about = r.html.find('.manga-description', first=True)
    output_text += "Описание: " + about.text + '\n'

    #рейтинг
    info = soup.find('div', class_="mt-2 ml-1 additional-rates")
    titlesA = info.find_all('i')
    nums=info.find_all('div', class_="compact-rate")
    nums_parsed = list()
    titles_parsed = list()
    for num in nums:
        if 'title' in num.attrs.keys():
            nums_parsed.append(num['title'])
    for title in titlesA:
        if 'title' in title.attrs.keys():
            titles_parsed.append(title['title'])
    output_text+=str("Рейтинг: \n")
    for i in range(0, len(titles_parsed)):
        output_text+='   '+titles_parsed[i] + ": " +nums_parsed[i]+'\n'


    title=names = r.html.find('.name', first=True)
    #сохранить в файл
    original_stdout = sys.stdout
    with open(f'{title.text}.txt', 'w') as f:
        sys.stdout = f
        print(output_text)
        sys.stdout = original_stdout
else: print('Такой дорамы нет :(')





