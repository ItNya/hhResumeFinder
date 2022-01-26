import json
from os import path
from pathlib import Path
from urllib.parse import quote_plus

import requests
from bs4 import BeautifulSoup
import requests
from bs4 import BeautifulSoup
import pandas as pd

with open('goroda_blyat.txt', encoding="utf-8") as f:
    goroda = list(f)


gorod = '1'
text = input('Профешн')
experience = int(input("Опыт работы"))
salary_to = input("Зп от")
salary_from = input("Зп до")
if experience >= 6:
    experience = "moreThan6"
elif 6 > experience >= 3:
    experience = "between3And6"
elif 3 > experience > 0:
    experience = "between1And3"
elif experience == 0:
    experience = "noExperience"



text = quote_plus(text.lower())
url = "https://hh.ru/search/"

url += "resume?area=" + gorod + "&label=only_with_salary&experience=" + experience + "&relocation=living_or_relocation&salary_from=" + salary_from +"&salary_to=" + salary_to + "&gender=unknown&text=" + text + "&logic=normal&pos=full_text&exp_period=all_time&st=resumeSearch&search_period=0"
rx = "//h1/span"

headers = {
  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36', }

print(url)
r = requests.get(url, headers=headers) #отправляем HTTP запрос и получаем результат
soup = BeautifulSoup(r.text, features="lxml") #Отправляем полученную страницу в библиотеку для парсинга
tables=soup.find_all('div', {'class': 'resume-search-item__header'}) #Получаем все таблицы с вопросами
my_file = open("output.txt", "w", encoding="utf-8")
n = 10
for item in tables:
    if n != 0:
      a = "https://hh.ru" + item.find('a').get('href').strip()
      print(a)
      new_url = "https://hh.ru" + item.find('a').get('href').strip()
      r = requests.get(new_url, headers=headers)  # отправляем HTTP запрос и получаем результат
      soup = BeautifulSoup(r.text, features="lxml")  # Отправляем полученную страницу в библиотеку для парсинга
      text_block = soup.find('div', {'class': 'resume-block-container', 'data-qa': "resume-block-skills-content"})
      try:
          b = str(text_block).split('"resume-block-skills-content">')[1].split('</div>')[0]
      except:
          b = "Не указано"
      print(b)
      my_file.write('\n' + '\n' + '\n' +a + '\n' + b)
      n -= 1


my_file.close()




