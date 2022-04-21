import json
from os import path
from pathlib import Path
from urllib.parse import quote_plus
import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
from aiogram import Bot, Dispatcher, types
from aiogram.dispatcher import FSMContext


def find_city_id(a):
    with open('goroda_1.txt', encoding="utf-8") as f:
        goroda = f.read()
    b = goroda.split(a)[0].split('"id"')[-1].split('"parent_id"')[0]
    return re.findall('(\d+)', b)[0]


def find_resume(gorod, text, experience, gender, salary_from, salary_to):
    my_list = list()
    gorod = find_city_id(gorod)
    gender = "unknown" # male or female or unknown
    if gender == "Женский":
        gender = "female"
    elif gender == "Мужской":
        gender = "male"
    else:
        gender = "unknown"
    if int(experience) >= 6:
        experience = "moreThan6"
    elif 6 > int(experience) >= 3:
        experience = "between3And6"
    elif 3 > int(experience) > 0:
        experience = "between1And3"
    else:
        experience = "noExperience"
    text = quote_plus(text.lower())
    url = "https://hh.ru/search/"

    url += "resume?area=" + gorod + "&label=only_with_salary&experience=" + experience + "&relocation=living_or_relocation&salary_from=" + salary_from +"&salary_to=" + salary_to + "&gender=" + gender + "&text=" + text + "&logic=normal&pos=full_text&exp_period=all_time&st=resumeSearch&search_period=0"
    rx = "//h1/span"

    headers = {
      'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36', }

    print(url)
    r = requests.get(url, headers=headers) #отправляем HTTP запрос и получаем результат
    soup = BeautifulSoup(r.text, features="lxml") #Отправляем полученную страницу в библиотеку для парсинга
    tables=soup.find_all('div', {'class': 'resume-search-item__header'}) #Получаем все таблицы с вопросами
    n = 10
    for item in tables:
        if n != 0:
          a = "https://hh.ru" + item.find('a').get('href').strip()
          new_url = "https://hh.ru" + item.find('a').get('href').strip()
          r = requests.get(new_url, headers=headers)  # отправляем HTTP запрос и получаем результат
          soup = BeautifulSoup(r.text, features="lxml")  # Отправляем полученную страницу в библиотеку для парсинга
          text_block = soup.find('div', {'class': 'resume-block-container', 'data-qa': "resume-block-skills-content"})
          try:
              b = str(text_block).split('"resume-block-skills-content">')[1].split('</div>')[0]
          except:
              b = "Не указано"
          print('\n' + a + '\n' + b)

          my_list.append('\n' + a + '\n' + b)
          n -= 1
        else:
            break
    return my_list







